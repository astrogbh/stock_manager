import streamlit as st
import re
from backend import (
    validar_login_cliente,
    validar_login_funcionario,
    cadastrar_cliente,
    listar_produtos,
    buscar_produto,
    criar_pedido,
    adicionar_item_pedido,
    atualizar_estoque,
    produtos_estoque_baixo,
    total_vendido,
    listar_pedidos,
    validar_nome,
    validar_cpf,
    validar_email,
    validar_telefone,
    atualizar_cliente,
    listar_categorias,
    listar_funcionarios,
    produtos_mais_vendidos,
    total_produtos
)

# Inicialização das variáveis de sessão
if "page" not in st.session_state:
    st.session_state.page = "escolha"
if "acesso" not in st.session_state:
    st.session_state.acesso = None
if "id_funcionario" not in st.session_state:
    st.session_state.id_funcionario = None
if "nome_funcionario" not in st.session_state:
    st.session_state.nome_funcionario = None
if "page" not in st.session_state:
    st.session_state.page = "login"

# Configuração da página
st.set_page_config(page_title="Sistema de Estoque", layout="wide")

# Definição das telas
def tela_escolha_login():
    st.title("Bem-vindo ao Sistema de Estoque!")

    st.subheader("Materiais mais vendidos")

    produtos = produtos_mais_vendidos()

    if produtos:
        for nome, total in produtos:
            st.write(f"🔹 {nome} - {total} unidades vendidas")
    else:
        st.info("Ainda não há vendas registradas.")

    st.write("---")

    tipo = st.radio(
        "Escolha uma opção:",
        ["Cliente", "Funcionário"]
    )

    if st.button("Continuar"):
        if tipo == "Cliente":
            st.session_state.page = "login_cliente"
        else:
            st.session_state.page = "login_funcionario"

        st.rerun()

def tela_login_cliente():
    st.title("Login do Cliente")

    cpf = st.text_input("CPF")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        user = validar_login_cliente(cpf, senha)

        if user:
            st.session_state.id_cliente = user[0]
            st.session_state.nome_cliente = user[1]
            st.session_state.page = "produtos_cliente"
            st.rerun()
        else:
            st.error("CPF ou senha incorretos")

    st.write("---")
    st.write("Ainda não tem conta?")

    if st.button("Criar cadastro"):
        st.session_state.page = "cadastrar_cliente_publico"
        st.rerun()

    if st.button("Voltar"):
        st.session_state.page = "escolha"
        st.rerun()

def tela_home_cliente():
    st.title(f"Olá, {st.session_state.nome_cliente}!")

    st.write("Escolha uma opção no menu ao lado.")

def tela_login_funcionario():
    st.title("Login do Funcionário")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        from backend import validar_login_funcionario
        resultado = validar_login_funcionario(usuario, senha)

        if resultado:   
            id_funcionario, nome, acesso = resultado
            st.session_state.id_funcionario = id_funcionario
            st.session_state.nome_funcionario = nome
            st.session_state.acesso = acesso

            st.session_state.page = "produtos_funcionario"
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")

    if st.button("Voltar"):
        st.session_state.page = "escolha"
        st.rerun()

def tela_cadastro_cliente():
    st.title("Cadastro de Cliente")

    nome = st.text_input("Nome completo")
    cpf = st.text_input("CPF (somente números)")
    telefone = st.text_input("Telefone (somente números)")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    endereco = st.text_input("Endereço")

    if st.button("Cadastrar Cliente"):

        if len(nome.strip()) < 3:
            st.error("Nome deve ter pelo menos 3 caracteres.")
            return
        cpf_limpo = cpf.replace(".", "").replace("-", "")
        if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
            st.error("CPF inválido! Digite apenas números (11 dígitos).")
            return
        if not telefone.isdigit():
            st.error("Telefone deve conter apenas números.")
            return
        regex_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(regex_email, email):
            st.error("Email inválido!")
            return
        if len(senha) < 6:
            st.error("A senha deve ter no mínimo 6 caracteres.")
            return
        if len(endereco.strip()) < 3:
            st.error("Endereço inválido.")
            return

        if len(senha) < 8:
            st.error("A senha deve possuir pelo menos 8 caracteres.")

        else:
            cadastrar_cliente(nome, cpf, telefone, email, senha, endereco)
            st.success("Cliente cadastrado com sucesso!")

    if st.button("Ir para Produtos"):
        st.session_state.page = "produtos"
        st.rerun()

def tela_produtos():
    st.title("Produtos disponíveis")

    produtos = listar_produtos()

    if not produtos:
        st.warning("Nenhum produto encontrado no estoque.")
        return

    # Mostrar tabela de produtos
    st.subheader("Lista de Produtos")
    

    for prod in produtos:
        id_produto, nome, desc, qtd, preco = prod

        with st.container(border=True):
            st.write(f"**{nome}**")
            st.write(f"Descrição: {desc}")
            st.write(f"Quantidade em estoque: {qtd}")
            st.write(f"Preço: R$ {preco}")

            if st.button(f"Adicionar ao carrinho - {id_produto}"):
                if "carrinho" not in st.session_state:
                    st.session_state.carrinho = []

                st.session_state.carrinho.append({
                    "id": id_produto,
                    "nome": nome,
                    "preco": preco
                })

                st.success(f"{nome} adicionado ao carrinho!")

    st.write("---")
    if st.button("Ver Carrinho"):
        st.session_state.page = "carrinho"
        st.rerun()

def tela_carrinho():
    st.title("Carrinho")

    if "carrinho" not in st.session_state or len(st.session_state.carrinho) == 0:
        st.warning("Seu carrinho está vazio.")
        return

    total = 0
    itens_remover = []

    st.subheader("Itens no Carrinho")

    for idx, item in enumerate(st.session_state.carrinho):
        nome = item["nome"]
        preco = float(item["valor"])
        qtd = int(item["quantidade"])

        with st.container(border=True):

            st.write(f"**{nome}** — R$ {preco:.2f}")

            nova_qtd = st.number_input(
                f"Quantidade de {nome}",
                min_value=1,
                max_value=99,
                value=qtd,
                key=f"qtd_carrinho_{idx}"
            )

            st.session_state.carrinho[idx]["quantidade"] = nova_qtd

            if st.button(f"Remover", key=f"remover_{idx}"):
                itens_remover.append(idx)

        total += preco * nova_qtd

    for idx in sorted(itens_remover, reverse=True):
        st.session_state.carrinho.pop(idx)

        st.subheader(f"Total: R$ {total:.2f}")
        confirmar = st.checkbox("Confirmo que desejo finalizar este pedido")

    if st.button("Finalizar Pedido"):
        from backend import criar_pedido, adicionar_item_pedido, atualizar_estoque

        id_cliente = st.session_state.id_cliente  
        id_pedido = criar_pedido(id_cliente, total)

        for item in st.session_state.carrinho:
            adicionar_item_pedido(
                id_pedido=id_pedido,
                id_produto=item["id_produto"],
                quantidade=item["quantidade"],
                preco_unitario=item["valor"]
            )
            atualizar_estoque(item["id_produto"], item["quantidade"])

        st.session_state.carrinho = []
        st.session_state.page = "pedido_finalizado"
        st.rerun()

def tela_pedido_finalizado():
    st.title("Pedido Finalizado!")

    st.success("Seu pedido foi registrado com sucesso.")

    st.write("O que deseja fazer agora?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Continuar comprando"):
            st.session_state.page = "produtos_cliente"
            st.rerun()

    with col2:
        if st.button("Sair da conta"):
            st.session_state.clear()
            st.rerun()

def tela_pedidos():
    st.title("Pedidos")

    pedidos = listar_pedidos()

    if not pedidos:
        st.info("Nenhum pedido encontrado.")
        return

    for p in pedidos:
        id_pedido, data, valor, cliente = p
        with st.container(border=True):
            st.write(f"**ID:** {id_pedido}")
            st.write(f"Cliente: {cliente}")
            st.write(f"Data: {data}")
            st.write(f"Total: R$ {valor}")

def tela_gestor():
    st.title("Painel do Gestor")

    st.subheader("Produtos com estoque baixo")
    baixos = produtos_estoque_baixo()

    if baixos:
        for prod in baixos:
            nome, qtd, min_qtd = prod
            st.write(f"**{nome}** — {qtd}/{min_qtd}")
    else:
        st.success("Nenhum produto abaixo do estoque mínimo!")

    st.write("---")
    st.subheader("Total vendido")
    st.metric("Total em vendas", f"R$ {total_vendido()}")
    st.metric(
    "Produtos cadastrados",
    total_produtos()
)

def tela_cadastro_produto():
    st.title("Cadastrar Produto")

    nome = st.text_input("Nome do Produto")
    desc = st.text_area("Descrição")
    qtd = st.number_input("Quantidade em Estoque", min_value=0)
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    minimo = st.number_input("Quantidade mínima", min_value=0)

    id_categoria = st.number_input("ID da Categoria", min_value=1)

    if st.button("Cadastrar"):
        from backend import cadastrar_produto

        if valor < 0:
            st.error("O valor do produto não pode ser negativo.")
        elif quantidade < 0:
            st.error("A quantidade não pode ser negativa.")
        else:
            cadastrar_produto(...)

        cadastrar_produto(
            nome,
            desc,
            qtd,
            valor,
            minimo,
            st.session_state.id_funcionario,
            id_categoria
        )

        st.success("Produto cadastrado com sucesso!")

def tela_produtos_cliente():
    from backend import listar_produtos
    st.title("Produtos")

    busca = st.text_input("Pesquisar por nome ou categoria:")

    produtos = listar_produtos()

    if busca:
        busca_lower = busca.lower()
        produtos = [
            p for p in produtos
            if busca_lower in p[1].lower() or busca_lower in p[5].lower()
        ]

    if not produtos:
        st.info("Nenhum produto encontrado.")
        return

    for prod in produtos:
        id_produto, nome, desc, valor, qtd, categoria = prod

        qtd = int(float(qtd)) if qtd else 0

        with st.container(border=True):
            st.subheader(nome)
            st.write(desc)
            st.write(f"**Categoria:** {categoria}")
            st.write(f"Preço: R$ {valor:.2f}")
            st.write(f"Disponível: {qtd}")

            if qtd == 0:
                st.warning("Produto esgotado!")
                continue

            qtd_escolhida = st.number_input(
                f"Adicionar quantidade:",
                min_value=1,
                max_value=qtd,
                key=f"qtd_{id_produto}"
            )

            if st.button(f"Adicionar ao carrinho", key=f"btn_{id_produto}"):
                if "carrinho" not in st.session_state:
                    st.session_state.carrinho = []

                st.session_state.carrinho.append({
                    "id_produto": id_produto,
                    "nome": nome,
                    "quantidade": qtd_escolhida,
                    "valor": valor
                })

                st.success(f"{nome} adicionado ao carrinho!")
                st.rerun()

def tela_produtos_funcionario():
    from backend import listar_produtos, listar_categorias

    st.title("Gerenciar Produtos")

    produtos = listar_produtos()
    categorias = listar_categorias()
    mapa_categorias = {cat[0]: cat[1] for cat in categorias}

    for prod in produtos:
        id_prod, nome, desc, valor, qtd, categoria = prod

        with st.container(border=True):
            st.subheader(nome)
            st.write(desc)
            st.write(f"Preço: R$ {valor:.2f}")
            st.write(f"Quantidade: {qtd}")
            st.write(f"Categoria: **{categoria}**")

            if st.button("Editar", key=f"editar_{id_prod}"):
                st.session_state.produto_editar = id_prod
                st.session_state.page = "editar_produto"
                st.rerun()

def tela_meus_pedidos():
    st.title("Meus Pedidos")

    from backend import listar_pedidos_cliente, listar_itens_pedido

    id_cliente = st.session_state.id_cliente
    pedidos = listar_pedidos_cliente(id_cliente)

    if not pedidos:
        st.info("Você ainda não fez nenhum pedido.")
        return

    for pedido in pedidos:
        id_pedido, data, valor = pedido

        with st.container(border=True):
            st.subheader(f"Pedido #{id_pedido}")
            st.write(f"Data: {data}")
            st.write(f"Total: R$ {valor:.2f}")

            itens = listar_itens_pedido(id_pedido)

            st.write("### Itens:")
            for item in itens:
                nome, qtd, preco = item
                st.write(f"- **{nome}** — {qtd}x — R$ {preco:.2f}")

def tela_cadastro_publico():
    st.title("Criar Conta")

    nome = st.text_input("Nome completo")
    cpf = st.text_input("CPF")
    telefone = st.text_input("Telefone")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    endereco = st.text_input("Endereço")

    if st.button("Cadastrar"):
        if nome and cpf and telefone and email and senha and endereco:
            cadastrar_cliente(nome, cpf, telefone, email, senha, endereco)
            st.success("Conta criada com sucesso! Agora faça login.")
            st.session_state.page = "login_cliente"
            st.rerun()
        else:
            st.error("Preencha todos os campos.")

    if st.button("Voltar"):
        st.session_state.page = "login_cliente"
        st.rerun()

def tela_editar_produto():
    from backend import listar_produtos, listar_categorias, editar_produto

    st.title("Editar Produto")

    # Garantir que existe produto selecionado
    id_produto = st.session_state.get("produto_editar")

    if id_produto is None:
        st.error("Nenhum produto selecionado para edição.")
        return

    # Converter para int para evitar erro de comparação
    id_produto = int(id_produto)

    produtos = listar_produtos()
    categorias = listar_categorias()

    # Buscar o produto certo
    prod = next((p for p in produtos if int(p[0]) == id_produto), None)

    if prod is None:
        st.error("Produto não encontrado.")
        return

    if valor < 0:
        st.error("O valor do produto não pode ser negativo.")
    elif quantidade < 0:
        st.error("A quantidade não pode ser negativa.")
    else:
        editar_produto(...)
    
    _, nome_at, desc_at, valor_at, qtd_at, categoria_at = prod

    nome = st.text_input("Nome", value=nome_at)
    desc = st.text_area("Descrição", value=desc_at)
    qtd = st.number_input("Quantidade", min_value=0, value=int(qtd_at))
    valor = st.number_input("Valor (R$)", min_value=0.0, value=float(valor_at))
    minimo = st.number_input("Quantidade mínima", min_value=0, value=1)

    mapa_cat = {c[0]: c[1] for c in categorias}

    categoria = st.selectbox(
        "Categoria",
        options=list(mapa_cat.keys()),
        format_func=lambda x: mapa_cat[x]
    )

    if st.button("Salvar Alterações"):
        editar_produto(id_produto, nome, desc, qtd, valor, minimo, categoria)
        st.success("Produto atualizado com sucesso!")
        st.session_state.page = "produtos_funcionario"
        del st.session_state.produto_editar
        st.rerun()

    if st.button("Voltar"):
        st.session_state.page = "produtos_funcionario"
        del st.session_state.produto_editar
        st.rerun()

def tela_info_cliente():
    st.title("Minha Conta")

    from backend import buscar_cliente, atualizar_cliente

    id_cliente = st.session_state.id_cliente
    dados = buscar_cliente(id_cliente)

    if not dados:
        st.error("Não foi possível carregar seus dados.")
        return

    nome, cpf, telefone, email, endereco = dados

    st.subheader("Suas informações")

    nome_novo = st.text_input("Nome", nome)
    cpf_novo = st.text_input("CPF", cpf)
    telefone_novo = st.text_input("Telefone", telefone)
    email_novo = st.text_input("Email", email)
    endereco_novo = st.text_input("Endereço", endereco)

    if st.button("Salvar alterações"):

        if not validar_nome(nome_novo):
            st.error("Nome inválido.")
            return

        if not validar_cpf(cpf_novo):
            st.error("CPF inválido.")
            return

        if not validar_email(email_novo):
            st.error("Email inválido.")
            return

        if not validar_telefone(telefone_novo):
            st.error("Telefone inválido.")
            return

        atualizar_cliente(
            id_cliente,
            nome_novo,
            cpf_novo,
            telefone_novo,
            email_novo,
            endereco_novo
        )

        st.success("Informações atualizadas!")
        st.rerun()

def tela_gestao_funcionarios():
    st.title("Gerenciar Funcionários")

    from backend import listar_funcionarios, cadastrar_funcionario

    st.subheader("Cadastrar novo funcionário")

    nome = st.text_input("Nome completo")
    usuario = st.text_input("Usuário de login")
    senha = st.text_input("Senha", type="password")
    acesso = st.selectbox(
        "Nível de acesso",
        [0, 1],
        format_func=lambda x: "Gestor" if x == 1 else "Funcionário"
    )

    if st.button("Cadastrar", key="cad_func"):

        # validação de campos vazios
        if not (nome and usuario and senha):
            st.error("Preencha todos os campos.")
            return

        if len(nome) > 20:
            st.error("O nome é muito longo. Use no máximo 20 caracteres.")
            return

        ok, msg = cadastrar_funcionario(nome, usuario, senha, acesso)

        if ok:
            st.success("Funcionário cadastrado com sucesso!")
            st.rerun()
        else:
            st.error(msg)

    st.write("---")
    st.subheader("Funcionários cadastrados")

    funcionarios = listar_funcionarios()

    for f in funcionarios:
        fid, nomef, usuariof, acessof = f

        col1, col2, col3, col4 = st.columns([3, 3, 2, 2])

        col1.write(f"**{nomef}**")
        col2.write(usuariof)
        col3.write("Gestor" if acessof == 1 else "Funcionário")

        if col4.button("Editar", key=f"editar_func_{fid}"):
            st.session_state.func_editando = fid
            st.session_state.page = "editar_funcionario"
            st.rerun()

def tela_editar_funcionario():
    from backend import buscar_funcionario, editar_funcionario

    id_func = st.session_state.func_editando
    func = buscar_funcionario(id_func)

    if not func:
        st.error("Funcionário não encontrado.")
        return

    _, nome_atual, user_atual, senha_atual, acesso_atual = func

    st.title("Editar Funcionário")

    nome = st.text_input("Nome", value=nome_atual)
    usuario = st.text_input("Usuário", value=user_atual)
    senha = st.text_input("Senha", value=senha_atual, type="password")
    acesso = st.selectbox(
        "Nível de acesso",
        [0, 1],
        index=1 if acesso_atual == 1 else 0,
        format_func=lambda x: "Gestor" if x == 1 else "Funcionário"
    )

    if st.button("Salvar"):
        editar_funcionario(id_func, nome, usuario, senha, acesso)
        st.success("Alterações salvas!")
        st.session_state.page = "gestao_func"
        st.rerun()

    if st.button("Voltar"):
        st.session_state.page = "gestao_func"
        st.rerun()

# Controle de páginas
if "page" not in st.session_state:
    st.session_state.page = "login"

# Barra lateral de navegação
with st.sidebar:
    st.header("Menu")

    if st.session_state.page == "escolha":
        st.write("### Loja de Materiais Darcan")
        st.write("""
    Bem-vindo ao nosso site!  
    Aqui você encontra:
    - Tijolos  
    - Madeiras  
    - Materiais elétricos  
    - Materiais hidráulicos  
    - Tintas e acabamento  

    Faça login para continuar!
        """)
    
    if st.session_state.page in ["login_cliente"]:
        st.write("### Loja de Materiais Darcan")
        st.write("- Aproveite nossa variedade de produtos!")
        st.write("- Faça login ou cria uma conta agora mesmo!")
        st.write("---")

    if st.session_state.page in ["login_funcionario"]:
        st.write("### Loja de Materiais Darcan")
        st.write("#### Sistema de Gestão de Estoque")
        st.write("- Gerencie o estoque e pedidos da loja.")
        st.write("- Faça login para continuar.")
        st.write("---")

    if st.session_state.page in ["cadastrar_cliente_publico"]:
        st.write("### Cadastro de Cliente")
        st.write("- Cria sua conta para aproveitar nossos produtos!")
        st.write("- Preencha o formulário ao lado.")
        st.write("---")

    # Cliente logado
    if st.session_state.get("id_cliente"):

        qtd_carrinho = len(st.session_state.get("carrinho", []))

        if st.button("Minha Conta"):
            st.session_state.page = "info_cliente"
            st.rerun()

        if st.button("Meus pedidos"):
            st.session_state.page = "meus_pedidos"
            st.rerun()

        if st.button(f"Carrinho ({qtd_carrinho})"):
            st.session_state.page = "carrinho"
            st.rerun()

        if st.button("Produtos"):
            st.session_state.page = "produtos_cliente"
            st.rerun()
        
        if st.button("Sair"):
            st.session_state.clear()
            st.rerun()

    # Funcionário logado
    elif st.session_state.get("id_funcionario"):

        if st.button("Gerenciar Produtos"):
            st.session_state.page = "produtos_funcionario"
            st.rerun()

        if st.button("Cadastrar Produto"):
            st.session_state.page = "cadastro_produto"
            st.rerun()

        if st.session_state.acesso == 1:
            if st.button("Painel do Gestor"):
                st.session_state.page = "gestor"
                st.rerun()

            if st.button("Funcionários"):
                st.session_state.page = "gestao_func"
                st.rerun()

        if st.button("Pedidos"):
            st.session_state.page = "pedidos"
            st.rerun()

        if st.button("Sair"):
            st.session_state.clear()
            st.rerun()

# Renderizar página atual
if st.session_state.page == "login":
    tela_login_funcionario()
elif st.session_state.page == "cadastro_cliente":
    tela_cadastro_cliente()
elif st.session_state.page == "produtos":
    tela_produtos()
elif st.session_state.page == "carrinho":
    tela_carrinho()
elif st.session_state.page == "pedidos":
    tela_pedidos()
elif st.session_state.page == "gestor":
    tela_gestor()
elif st.session_state.page == "escolha":
    tela_escolha_login()
elif st.session_state.page == "login_cliente":
    tela_login_cliente()
elif st.session_state.page == "login_funcionario":
    tela_login_funcionario()
elif st.session_state.page == "home_cliente":
    tela_home_cliente()
elif st.session_state.page == "cadastro_produto":
    tela_cadastro_produto()
elif st.session_state.page == "produtos_cliente":
    tela_produtos_cliente()
elif st.session_state.page == "carrinho":
    tela_carrinho()
elif st.session_state.page == "meus_pedidos":
    tela_meus_pedidos()
elif st.session_state.page == "cadastrar_cliente_publico":
    tela_cadastro_publico()
elif st.session_state.page == "produtos_funcionario":
    tela_produtos_funcionario()
elif st.session_state.page == "editar_produto":
    tela_editar_produto()
elif st.session_state.page == "info_cliente":
    tela_info_cliente()    
elif st.session_state.page == "gestao_func":
    tela_gestao_funcionarios()
elif st.session_state.page == "editar_produto":
    tela_editar_produto()
elif st.session_state.page == "editar_funcionario":
    tela_editar_funcionario()
elif st.session_state.page == "pedido_finalizado":
    tela_pedido_finalizado()
