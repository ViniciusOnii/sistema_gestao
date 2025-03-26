# Sistema de Gestão de Vendas - Documentação

## Visão Geral
Este projeto implementa um sistema de gestão de vendas utilizando Python e MongoDB, focando no gerenciamento eficiente de produtos, categorias, fornecedores, funcionários, vendas e faturamento. A interface gráfica é construída com `tkinter`, utilizando também as bibliotecas `pymongo` para comunicação com o banco de dados e `PIL` (Pillow) para manipulação de imagens.

## Estrutura do Projeto
O projeto é organizado da seguinte forma:

- **bill/**: Armazena faturas geradas durante as vendas.
- **images/**: Contém imagens usadas na interface gráfica.
- **billing.py**: Gerencia o faturamento e cria relatórios financeiros.
- **category.py**: Criação e edição de categorias de produtos.
- **create_db.py**: Inicializa o banco de dados MongoDB.
- **dashboard.py**: Interface para análise de dados de vendas.
- **employee.py**: Cadastro e gerenciamento de funcionários.
- **products.py**: Cadastro e controle de produtos.
- **sales.py**: Registro de vendas com integração ao faturamento.
- **supplier.py**: Gerenciamento de fornecedores e atualização de estoque.

## Funcionalidades Principais
- Cadastro e gerenciamento de produtos, categorias, fornecedores e funcionários.
- Registro de vendas e emissão de faturas.
- Visualização de dashboards analíticos.
- Criação automatizada e configuração do banco de dados MongoDB.
- Interface gráfica amigável construída com `tkinter`.

## Requisitos para Execução
1. **Instalação do Python:** Certifique-se de ter o Python 3.x instalado no seu sistema. Caso não tenha, baixe em [python.org](https://www.python.org/downloads/).

2. **Instalação do MongoDB:** Baixe e instale o MongoDB Community Server em [mongodb.com](https://www.mongodb.com/try/download/community). Certifique-se de iniciar o serviço MongoDB.

3. **Instalação das Bibliotecas:** Abra o terminal na pasta do projeto e execute:
```
pip install pymongo pillow bson
```
Obs.: O `tkinter` já vem integrado ao Python em muitas distribuições.

## Configuração de Login e Senha
- Para acessar a área do dashboard, é necessário realizar login.
- As credenciais padrão configuradas são:
  - **Usuário:** Leo
  - **Senha:** 123
- Caso deseje alterar o login e senha, abra o código no módulo de autenticação e ajuste as variáveis correspondentes.

## Passo a Passo para Execução
1. Certifique-se de que o MongoDB esteja ativo e em execução.
2. No terminal, navegue até o diretório raiz do projeto.
3. Configure o banco de dados inicializando o script:
```
python create_db.py
```
4. Inicie o módulo `dashboard.py` para acessar a interface gráfica:
```
python dashboard.py
```
5. Na tela de login, insira o usuário e senha padrão ou utilize credenciais personalizadas.

## Para Entender melhor como funciona o projeto ver esse video.



Se acontecer algum problema ao rodar o código, como erro de importação de bibliotecas, uma boa prática é criar um ambiente virtual para organizar as dependências do projeto. Aqui está um passo a passo simples:

🔧 Passo 1: Criar um Ambiente Virtual
Abra o terminal na pasta do seu projeto.

Digite o comando abaixo para criar o ambiente virtual:

bash/cmd
Copiar
Editar
python -m venv venv
Aqui, venv é o nome do ambiente virtual. Você pode escolher outro nome, se preferir.

🟦 Passo 2: Ativar o Ambiente Virtual
Windows:

bash/cmd
Copiar
Editar
venv\Scripts\activate
Mac ou Linux:

bash/cmd
Copiar
Editar
source venv/bin/activate
Você verá o nome do ambiente ((venv)) no início da linha do terminal, indicando que está ativo.

📂 Passo 3: Instalar as Bibliotecas
Com o ambiente virtual ativo, instale as bibliotecas do requirements.txt:

bash/cmd
Copiar
Editar
pip install pymongo pillow bson
Isso garante que todas as dependências sejam instaladas corretamente.


##Partes do Projeto:
##Dashboard.py
![image](https://github.com/user-attachments/assets/d17f8727-facc-470a-84e3-13ab7c8fa63e)
![image](https://github.com/user-attachments/assets/8fb418e4-c544-4d89-bc38-c300502da849)

Parte Principal do Sistema onde você vai conseguir acessar as outras abas

##Employee.py
![image](https://github.com/user-attachments/assets/a32f3165-a99b-491e-a1d4-4fb821696cba)
Onde você irá cadastrar os dados do cliente ou funcionario cadastrando suas informações


##Suplier.py
![image](https://github.com/user-attachments/assets/a4a1bbb3-81e8-433c-b578-ed14d04fd4eb)
Onde você ira cadastrar os fornecedores 


#Cateogry.py
![image](https://github.com/user-attachments/assets/4dbfa2b6-7c1c-4f8f-a993-267b0386f256)
Onde irá colocar as categorias do seu produto ou qualquer coisa do tipo.

##Products.py
![image](https://github.com/user-attachments/assets/ca768dc7-235b-4f91-a45d-a08a58e07253)
#Onde irá adicionar seus produtos ao banco de dados para vender

##Billing.py
![image](https://github.com/user-attachments/assets/f0c2d548-b824-4745-85ce-aeff419731f0)
Onde você ira adicionar os produtos que você quer comprar, que está no banco de dados.

##Sales.py
![image](https://github.com/user-attachments/assets/c9fd4428-da1a-43c3-af2a-f1d29b52b3c5)
#Onde você irá ver as vendas




