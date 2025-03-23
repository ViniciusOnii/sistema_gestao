import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
from pymongo import MongoClient

class ProductManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Estoque")

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["estoque"]
        self.collection = self.db["produtos"]

        self.entries = {}
        self.dropdown_vars = {}
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        labels = ["Categoria", "Fornecedor", "Nome", "Preço", "Quantidade", "Status"]

        for idx, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=idx, column=0, padx=10, pady=5)

            if label in ["Categoria", "Fornecedor"]:
                self.dropdown_vars[label.lower()] = StringVar(self.root)
                self.dropdown_vars[label.lower()].set("Selecione")
                dropdown = OptionMenu(self.root, self.dropdown_vars[label.lower()], *self.get_options(label.lower()))
                dropdown.grid(row=idx, column=1, padx=10, pady=5)
            elif label == "Status":
                self.entries[label.lower()] = StringVar(self.root)
                self.entries[label.lower()].set("ativo")
                status_menu = OptionMenu(self.root, self.entries[label.lower()], "ativo", "desativado")
                status_menu.grid(row=idx, column=1, padx=10, pady=5)
            else:
                entry = tk.Entry(self.root)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                self.entries[label.lower()] = entry

        tk.Button(self.root, text="Adicionar Produto", command=self.add_product).grid(row=7, column=0, pady=10)
        tk.Button(self.root, text="Atualizar Produto", command=self.update_product).grid(row=7, column=1, pady=10)
        tk.Button(self.root, text="Excluir Produto", command=self.delete_product).grid(row=7, column=2, pady=10)

        self.product_listbox = tk.Listbox(self.root, width=80)
        self.product_listbox.grid(row=8, column=0, columnspan=3, padx=10, pady=10)
        self.product_listbox.bind("<<ListboxSelect>>", self.select_product)

    def get_options(self, field):
        options = self.collection.distinct(field)
        return options if options else ["Nenhum"]

    def load_products(self):
        self.product_listbox.delete(0, tk.END)
        products = self.collection.find()

        for product in products:
            display = f"{product['categoria']} - {product['fornecedor']} - {product['nome']} - R$ {product['preco']} - {product['quantidade']} un - {product['status']}"
            self.product_listbox.insert(tk.END, display)

    def add_product(self):
        try:
            product = {
                "categoria": self.dropdown_vars["categoria"].get(),
                "fornecedor": self.dropdown_vars["fornecedor"].get(),
                "nome": self.entries["nome"].get(),
                "preco": float(self.entries["preço"].get()),
                "quantidade": int(self.entries["quantidade"].get()),
                "status": self.entries["status"].get()
            }

            if "Selecione" in [product["categoria"], product["fornecedor"]] or not all(product.values()):
                messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")
                return

            self.collection.insert_one(product)
            self.load_products()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            self.clear_fields()

        except ValueError:
            messagebox.showerror("Erro", "Verifique os valores de preço e quantidade.")

    def update_product(self):
        try:
            selected = self.product_listbox.get(tk.ACTIVE)
            if not selected:
                messagebox.showwarning("Atenção", "Selecione um produto para atualizar.")
                return

            nome = selected.split(" - ")[2]
            updated_data = {
                "categoria": self.dropdown_vars["categoria"].get(),
                "fornecedor": self.dropdown_vars["fornecedor"].get(),
                "nome": self.entries["nome"].get(),
                "preco": float(self.entries["preço"].get()),
                "quantidade": int(self.entries["quantidade"].get()),
                "status": self.entries["status"].get()
            }

            if "Selecione" in [updated_data["categoria"], updated_data["fornecedor"]] or not all(updated_data.values()):
                messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")
                return

            self.collection.update_one({"nome": nome}, {"$set": updated_data})
            self.load_products()
            messagebox.showinfo("Sucesso", "Produto atualizado!")

        except ValueError:
            messagebox.showerror("Erro", "Verifique os valores de preço e quantidade.")

    def delete_product(self):
        selected = self.product_listbox.get(tk.ACTIVE)
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um produto para excluir.")
            return

        nome = selected.split(" - ")[2]
        self.collection.delete_one({"nome": nome})
        self.load_products()
        messagebox.showinfo("Sucesso", "Produto excluído!")

    def select_product(self, event):
        try:
            selected = self.product_listbox.get(self.product_listbox.curselection())
            nome = selected.split(" - ")[2]
            product = self.collection.find_one({"nome": nome})

            for key in self.entries:
                if key == "status":
                    self.entries[key].set(product[key])
                else:
                    self.entries[key].delete(0, tk.END)
                    self.entries[key].insert(0, str(product[key]))

            for key in self.dropdown_vars:
                self.dropdown_vars[key].set(product[key])

        except IndexError:
            pass

    def clear_fields(self):
        for entry in self.entries.values():
            if isinstance(entry, StringVar):
                entry.set("ativo")
            else:
                entry.delete(0, tk.END)
        for var in self.dropdown_vars.values():
            var.set("Selecione")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductManager(root)
    root.mainloop()
