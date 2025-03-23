import pymongo
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

class POS:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema POS")
        self.root.geometry("800x600")

        # Conectar ao MongoDB
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["estoque"]
            self.collection = self.db["produtos"]
            self.vendas = self.db["vendas"]
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao MongoDB.\n{e}")
            return

        # Criar índice para busca otimizada
        self.collection.create_index([("nome", pymongo.TEXT)])

        # Variáveis do Produto
        self.var_produto = StringVar()
        self.var_preco = StringVar()
        self.var_quantidade = StringVar(value="1")
        self.total_valor = DoubleVar(value=0.0)
        self.carrinho = []

        # Frame de Busca
        frame_busca = Frame(self.root, bd=2, relief=RIDGE, padx=10, pady=10)
        frame_busca.place(x=10, y=10, width=780, height=80)

        Label(frame_busca, text="Buscar Produto:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_busca = Entry(frame_busca, textvariable=self.var_produto, width=30)
        self.entry_busca.grid(row=0, column=1, padx=5, pady=5)
        Button(frame_busca, text="Buscar", command=self.buscar_produto).grid(row=0, column=2, padx=5, pady=5)

        # Lista de Produtos Encontrados
        self.tree = ttk.Treeview(self.root, columns=("nome", "preco"), show='headings', height=5)
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço")
        self.tree.column("nome", width=200)
        self.tree.column("preco", width=100)
        self.tree.bind("<Double-1>", self.selecionar_produto)
        self.tree.place(x=10, y=100, width=780, height=150)

        # Campos do Carrinho
        frame_produto = Frame(self.root, bd=2, relief=RIDGE, padx=10, pady=10)
        frame_produto.place(x=10, y=260, width=780, height=100)

        Label(frame_produto, text="Produto:").grid(row=0, column=0, padx=5, pady=5)
        Entry(frame_produto, textvariable=self.var_produto, state="readonly", width=30).grid(row=0, column=1, padx=5, pady=5)

        Label(frame_produto, text="Preço:").grid(row=0, column=2, padx=5, pady=5)
        Entry(frame_produto, textvariable=self.var_preco, state="readonly", width=10).grid(row=0, column=3, padx=5, pady=5)

        Label(frame_produto, text="Quantidade:").grid(row=0, column=4, padx=5, pady=5)
        Entry(frame_produto, textvariable=self.var_quantidade, width=5).grid(row=0, column=5, padx=5, pady=5)

        Button(frame_produto, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho).grid(row=0, column=6, padx=10, pady=5)

        # Tabela do Carrinho
        self.cart_table = ttk.Treeview(self.root, columns=("nome", "preco", "quantidade"), show='headings', height=8)
        self.cart_table.heading("nome", text="Nome")
        self.cart_table.heading("preco", text="Preço")
        self.cart_table.heading("quantidade", text="Quantidade")
        self.cart_table.place(x=10, y=370, width=780, height=150)

        # Total e Botões do Carrinho
        frame_total = Frame(self.root, bd=2, relief=RIDGE)
        frame_total.place(x=10, y=530, width=780, height=50)

        Label(frame_total, text="Total: R$", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        Label(frame_total, textvariable=self.total_valor, font=("Arial", 12, "bold"), fg="green").pack(side=LEFT)

        Button(frame_total, text="Limpar Carrinho", command=self.limpar_carrinho).pack(side=LEFT, padx=10)
        Button(frame_total, text="Finalizar Compra", command=self.finalizar_compra).pack(side=LEFT, padx=10)

    def buscar_produto(self):
        self.tree.delete(*self.tree.get_children())
        nome_produto = self.var_produto.get()
        resultados = self.collection.find({"nome": {"$regex": nome_produto, "$options": "i"}})
        for produto in resultados:
            self.tree.insert("", END, values=(produto["nome"], produto["preco"]))

    def selecionar_produto(self, event):
        item = self.tree.focus()
        valores = self.tree.item(item, "values")
        if valores:
            self.var_produto.set(valores[0])
            self.var_preco.set(valores[1])

    def adicionar_ao_carrinho(self):
        nome = self.var_produto.get()
        preco = float(self.var_preco.get())
        quantidade = int(self.var_quantidade.get())
        if nome and quantidade > 0:
            self.carrinho.append((nome, preco, quantidade))
            self.atualizar_carrinho()

    def atualizar_carrinho(self):
        self.cart_table.delete(*self.cart_table.get_children())
        total = sum(item[1] * item[2] for item in self.carrinho)
        self.total_valor.set(total)

    def limpar_carrinho(self):
        self.carrinho.clear()
        self.atualizar_carrinho()

    def emitir_nota(self, cliente, telefone, nota_fiscal, data, produto, quantidade, preco, desconto):
        import os
        if not os.path.exists('bill'):
            os.makedirs('bill')
        total = quantidade * preco
        valor_desconto = total * (desconto / 100)
        net_pay = total - valor_desconto

        nota = f"""
        ============================================
                      XYZ-Inventory
        Phone No. 98725***** , Delhi-125001
        ============================================
        Cliente: {cliente}
        Telefone: {telefone}
        Nota Fiscal: {nota_fiscal}      Data: {data}
        --------------------------------------------
        Produto       QTD       Preço
        --------------------------------------------
        {produto}          {quantidade}         R$ {preco:.2f}
        --------------------------------------------
        Valor Total: R$ {total:.2f}
        Desconto: R$ {valor_desconto:.2f}
        Valor Líquido: R$ {net_pay:.2f}
        ============================================
        """
                    # Salvar a nota fiscal como arquivo txt na pasta 'bill'
        with open(f'bill/nota_{nota_fiscal}.txt', 'w', encoding='utf-8', errors='replace') as file:
            file.write(nota)
        messagebox.showinfo("Nota Fiscal", nota)

    def finalizar_compra(self):
        self.emitir_nota("Cliente Exemplo", "(11) 99999-9999", "12345", datetime.now().strftime("%Y-%m-%d"), self.var_produto.get(), int(self.var_quantidade.get()), float(self.var_preco.get()), 10)

if __name__ == "__main__":
    root = Tk()
    app = POS(root)
    root.mainloop()
