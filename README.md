# Stock Manager Darcan

Sistema de gerenciamento de estoque desenvolvido para uma loja de materiais de construção fictícia chamada **Darcan**.

O projeto foi desenvolvido em **Python**, utilizando **Streamlit** para a interface gráfica e **MySQL** para armazenamento dos dados.

---

## Funcionalidades

### Cliente
- Cadastro de clientes
- Login utilizando CPF e senha
- Consulta de produtos disponíveis
- Adição de produtos ao carrinho
- Realização de pedidos
- Visualização do histórico de pedidos
- Atualização de dados cadastrais

### Funcionário
- Login administrativo
- Cadastro de produtos
- Edição de produtos
- Consulta de pedidos realizados

### Gestor
- Cadastro de funcionários
- Edição de funcionários
- Consulta de estoque baixo
- Visualização do total de vendas
- Acompanhamento de métricas do sistema

---

## Tecnologias Utilizadas

- Python
- Streamlit
- MySQL
- Git
- GitHub Projects (Kanban)

---

## Estrutura do Projeto

```text
Stock_Manager/
│
├── app.py
├── backend.py
├── banco.sql
├── README.md
└── assets/
```

---

## Requisitos

- Python 3.10 ou superior
- MySQL Server
- Streamlit

Instalação das dependências:

```bash
pip install streamlit mysql-connector-python
```

---

## Como Executar

### 1. Importar o banco de dados

Importe o arquivo SQL fornecido para o MySQL.

### 2. Configurar a conexão

No arquivo `backend.py`, configure:

```python
host='localhost'
user='root'
password='sua_senha'
database='projeto_final_bd'
```

### 3. Executar o projeto

```bash
streamlit run app.py
```

---

## Metodologia Utilizada

O projeto foi desenvolvido utilizando a metodologia ágil **Kanban**, por meio do GitHub Projects.

As atividades foram organizadas em colunas:

- Backlog
- In Progress
- In Review
- Done

Essa abordagem permitiu acompanhar o progresso das funcionalidades, correções e melhorias realizadas durante o desenvolvimento.

---

## Mudança de Escopo

Durante o desenvolvimento foi identificada uma oportunidade de melhorar a experiência do usuário na página inicial do sistema.

Inicialmente, a tela de entrada apresentava apenas as opções de acesso para clientes e funcionários. Como evolução do projeto, foi implementada a exibição dos **materiais mais vendidos** logo na página inicial.

### Objetivos da mudança

- Tornar a interface mais informativa
- Destacar produtos de maior relevância comercial
- Melhorar a experiência do usuário
- Aproximar o sistema de aplicações comerciais reais

A funcionalidade foi implementada através da análise dos pedidos registrados no banco de dados, permitindo identificar e exibir automaticamente os produtos mais vendidos.

---

## Melhorias Realizadas

Durante o desenvolvimento também foram implementadas melhorias de manutenção, usabilidade e segurança, incluindo:

- Correção de bugs na edição de produtos
- Refatoração de código e remoção de conexões desnecessárias
- Validação de dados de entrada
- Exibição de métricas administrativas
- Melhorias na navegação da interface

---

## Autor

**Gabriel V.**
Curso de Ciência da Computação
