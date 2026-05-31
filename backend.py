import mysql.connector
import streamlit as st
import re

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='22222121',
        database='projeto_final_bd'
    )

def validar_login_cliente(cpf, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    cpf_limpo = cpf.replace(".", "").replace("-", "")

    sql = """
    SELECT id_cliente, nome_cliente
    FROM tbl_clientes
    WHERE REPLACE(REPLACE(cpf_cliente, '.', ''), '-', '') = %s
    AND senha_cliente = %s
    """
    
    cursor.execute(sql, (cpf_limpo, senha))
    resultado = cursor.fetchone()

    conexao.close()
    return resultado

def validar_login_funcionario(usuario, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_funcionario, nome_funcionario, acesso_gestor
    FROM tbl_funcionarios
    WHERE login_funcionario = %s AND senha_funcionario = %s
    """

    cursor.execute(sql, (usuario, senha))
    resultado = cursor.fetchone()

    conexao.close()
    return resultado

def cadastrar_cliente(nome, cpf, telefone, email, senha, endereco):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_clientes 
    (nome_cliente, cpf_cliente, telefone_cliente, email_cliente, senha_cliente, endereco_cliente)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    valores = (nome, cpf, telefone, email, senha, endereco)

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT p.id_produto, p.nome_produto, p.desc_produto, p.valor_produto, p.qtd_produto, c.nome_categoria
    FROM tbl_estoque_produtos p
    JOIN tbl_categorias c ON c.id_categoria = p.fk_tbl_categorias_id_categoria

    """

    cursor.execute(sql)
    produtos = cursor.fetchall()
    conexao.close()

    return produtos

def buscar_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_produto, nome_produto, desc_produto, qtd_produto, valor_produto
    FROM tbl_estoque_produtos
    WHERE id_produto = %s
    """

    cursor.execute(sql, (id_produto,))
    produto = cursor.fetchone()
    conexao.close()

    return produto

def criar_pedido(id_cliente, valor_total):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_pedidos (data_pedido, valor_pedido, fk_tbl_clientes_id_cliente)
    VALUES (NOW(), %s, %s)
    """

    cursor.execute(sql, (valor_total, id_cliente))
    conexao.commit()

    cursor.execute("SELECT LAST_INSERT_ID()")
    id_pedido = cursor.fetchone()[0]

    conexao.close()
    return id_pedido

def adicionar_item_pedido(id_pedido, id_produto, quantidade, preco_unitario):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_itens_pedido_estoque_pedido
    (qtd_item_pedido, preco_unitario_item_pedido, fk_tbl_estoque_produtos_id_produto, fk_tbl_pedidos_id_pedido)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (quantidade, preco_unitario, id_produto, id_pedido))
    conexao.commit()
    conexao.close()

def atualizar_estoque(id_produto, quantidade_solicitada):
    conexao = conectar()
    cursor = conexao.cursor()

    # Pegar quantidade atual
    cursor.execute("""
    SELECT qtd_produto FROM tbl_estoque_produtos WHERE id_produto = %s
    """, (id_produto,))
    qtd_atual = cursor.fetchone()[0]

    nova_qtd = qtd_atual - quantidade_solicitada

    cursor.execute("""
    UPDATE tbl_estoque_produtos
    SET qtd_produto = %s
    WHERE id_produto = %s
    """, (nova_qtd, id_produto))

    conexao.commit()
    conexao.close()

def produtos_estoque_baixo():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT nome_produto, qtd_produto, qtd_minima_produto
    FROM tbl_estoque_produtos
    WHERE qtd_produto <= qtd_minima_produto
    """

    cursor.execute(sql)
    dados = cursor.fetchall()
    conexao.close()
    return dados

def total_vendido():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT SUM(valor_pedido) FROM tbl_pedidos"
    cursor.execute(sql)
    valor = cursor.fetchone()[0] or 0
    conexao.close()
    return valor

def listar_pedidos():

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT p.id_pedido, p.data_pedido, p.valor_pedido, c.nome_cliente
    FROM tbl_pedidos p
    JOIN tbl_clientes c 
        ON c.id_cliente = p.fk_tbl_clientes_id_cliente
    ORDER BY p.data_pedido DESC
    """

    cursor.execute(sql)
    pedidos = cursor.fetchall()
    conexao.close()

    return pedidos

def cadastrar_produto(nome, descricao, quantidade, valor, minimo, id_funcionario, id_categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_estoque_produtos
    (nome_produto, desc_produto, qtd_produto, valor_produto, qtd_minima_produto,
     fk_tbl_funcionarios_id_funcionario, fk_tbl_categorias_id_categoria)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, descricao, quantidade, valor, minimo, id_funcionario, id_categoria))
    conexao.commit()
    conexao.close()

    return True

def listar_pedidos_cliente(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT p.id_pedido, p.data_pedido, p.valor_pedido
    FROM tbl_pedidos p
    WHERE p.fk_tbl_clientes_id_cliente = %s
    ORDER BY p.data_pedido DESC
    """
    cursor.execute(sql, (id_cliente,))
    pedidos = cursor.fetchall()

    conexao.close()
    return pedidos

def listar_itens_pedido(id_pedido):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT pr.nome_produto, ip.qtd_item_pedido, ip.preco_unitario_item_pedido
    FROM tbl_itens_pedido_estoque_pedido ip
    JOIN tbl_estoque_produtos pr 
        ON pr.id_produto = ip.fk_tbl_estoque_produtos_id_produto
    WHERE ip.fk_tbl_pedidos_id_pedido = %s
    """
    cursor.execute(sql, (id_pedido,))
    itens = cursor.fetchall()

    conexao.close()
    return itens

def atualizar_produto(id_produto, nome, desc, qtd, preco):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_estoque_produtos
    SET nome_produto=%s, desc_produto=%s, qtd_produto=%s, valor_produto=%s
    WHERE id_produto=%s
    """

    cursor.execute(sql, (nome, desc, qtd, preco, id_produto))
    conexao.commit()
    conexao.close()

def buscar_cliente(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT nome_cliente, cpf_cliente, telefone_cliente, email_cliente, endereco_cliente
    FROM tbl_clientes
    WHERE id_cliente = %s
    """
    cursor.execute(sql, (id_cliente,))
    dados = cursor.fetchone()

    conexao.close()
    return dados

def atualizar_cliente(id_cliente, nome, cpf, telefone, email, endereco):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_clientes
    SET nome_cliente=%s, cpf_cliente=%s, telefone_cliente=%s,
        email_cliente=%s, endereco_cliente=%s
    WHERE id_cliente=%s
    """
    cursor.execute(sql, (nome, cpf, telefone, email, endereco, id_cliente))
    conexao.commit()
    conexao.close()

def validar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")

    if len(cpf) != 11 or not cpf.isdigit():
        return False

    if cpf in [c*11 for c in "0123456789"]:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{d1}{d2}"

def validar_email(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email) is not None

def validar_telefone(tel):
    tel = tel.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    return tel.isdigit() and 10 <= len(tel) <= 11

def validar_nome(nome):
    nome = nome.strip()
    return len(nome) >= 3 and any(c.isalpha() for c in nome)

def listar_categorias():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categorias")
    categorias = cursor.fetchall()

    conexao.close()
    return categorias

def editar_produto(id_produto, nome, descricao, quantidade, valor, minimo, id_categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_estoque_produtos
    SET nome_produto=%s, desc_produto=%s, qtd_produto=%s,
        valor_produto=%s, qtd_minima_produto=%s, fk_tbl_categorias_id_categoria=%s
    WHERE id_produto=%s
    """

    cursor.execute(sql, (nome, descricao, quantidade, valor, minimo, id_categoria, id_produto))
    conexao.commit()
    conexao.close()

def listar_funcionarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_funcionario, nome_funcionario, login_funcionario, acesso_gestor
        FROM tbl_funcionarios
    """)
    
    funcionarios = cursor.fetchall()
    conexao.close()
    return funcionarios

def cadastrar_funcionario(nome, usuario, senha, acesso):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO tbl_funcionarios (nome_funcionario, usuario_funcionario, senha_funcionario, acesso)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (nome, usuario, senha, acesso))
        conexao.commit()
        conexao.close()
        return True, None  # Sucesso

    except mysql.connector.DataError as e:
        # Erro de tamanho excedido (ex: nome muito longo)
        return False, "Nome muito grande. Use no máximo 100 caracteres."

    except Exception as e:
        # Qualquer outro erro
        return False, "Erro ao cadastrar funcionário."

def buscar_funcionario(id_func):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_funcionario, nome_funcionario, login_funcionario, senha_funcionario, acesso_gestor
    FROM tbl_funcionarios
    WHERE id_funcionario = %s
    """
    cursor.execute(sql, (id_func,))
    dados = cursor.fetchone()

    conexao.close()
    return dados

def editar_funcionario(id_func, nome, usuario, senha, acesso):
    
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_funcionarios
    SET nome_funcionario=%s,
        login_funcionario=%s,
        senha_funcionario=%s,
        acesso_gestor=%s
    WHERE id_funcionario=%s
    """

    cursor.execute(sql, (nome, usuario, senha, acesso, id_func))
    conexao.commit()
    conexao.close()

def produtos_mais_vendidos(limite=5):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT
        p.nome_produto,
        SUM(ip.qtd_item_pedido) AS total_vendido
    FROM tbl_itens_pedido_estoque_pedido ip
    JOIN tbl_estoque_produtos p
        ON p.id_produto = ip.fk_tbl_estoque_produtos_id_produto
    GROUP BY p.id_produto, p.nome_produto
    ORDER BY total_vendido DESC
    LIMIT %s
    """

    cursor.execute(sql, (limite,))
    produtos = cursor.fetchall()

    conexao.close()
    return produtos
