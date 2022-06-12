import matplotlib.pyplot as plt
import pymysql.cursors


conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

autentico = False


def logarCadastrar(decidir):

    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False
    if decisao == 1:
        nome = input('\ndigite um nome\n')
        senha = input('\ndigite uma senha\n')



        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            print('email ou senha errado')



    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input('\ndigite um nome\n')
        senha = input('\ndigite uma senha\n')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1




        if usuarioExistente == 1:
            print('usuario ou senha ja existente')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros (nome, senha, nivel) values (%s, %s, %s)', (nome, senha, 1))
                    conexao.commit()
                print('usuario cadastrado com sucesso')
            except:
                print('erro ao se cadastrar')

    return autenticado, usuarioMaster

def cadastrarProdutos():
    nome = input('\ndigite o nome do produto\n')
    ingredientes = input('\ndigite os ingredientes do produtos\n')
    grupo = input('\ndigite o grupo pertencente a esse produto\n')
    preco = float(input('\ndigite o preço do produto \n'))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos (nome, ingredientes, grupo, preco) values (%s, %s, %s, %s)', (nome, ingredientes, grupo, preco))
            conexao.commit()
            print('produto cadastrado com sucesso')
    except:
        print('erro ao inserir os produtos no banco de dados')

def listarProdutos():
    produtos = []

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()
    except:
        print('erro ao conectar ao banco de dados')

    for i in produtosCadastrados:
        produtos.append(i)

    if len(produtos) != 0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('nenhum produto cadastrado')

def excluirProdutos():
    idDeletar = int(input('\ndigite o id refere ao produto que deseja apagar\n'))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('delete from produtos where id = {}'.format(idDeletar))
    except:
        print('erro ao excluir o produto')

def listarPedidos():
    pedidos = []
    decision = 0

    while decision != 2:
        pedidos.clear()

        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listaPedidos = cursor.fetchall()
        except:
            print('erro no banco de dados')


        for i in listaPedidos:
            pedidos.append(i)

        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('nenhum pedido foi feito')

        decision = int(input('\ndigite 1 para dar um produto como entregue e 2 para voltar\n'))

        if decision == 1:
            idDeletar = int(input('\ndigite o id do pedido entregue\n'))

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('delete from pedidos where id = {}'.format(idDeletar))
                    print('produto dado como entregue')
            except:
                print('erro ao dar o pedido como entregue')

def gerarEstatistica():

    nomeProdutos = []
    nomeProdutos.clear()

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except:
        print('erro ao fazer consulta no banco de dados')

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticaVendido')
            vendido = cursor.fetchall()
    except:
        print('erro ao fazer a consulta no banco de dados')


    estado = int(input('\ndigite 0 para sair, 1 para pesquisar por nome e 2 para pesquisar por grupo\n'))

    if estado == 1:
        decisao3 = int(input('\ndigite 1 para pesquisar por dinheiro e 2 por quantidade unitaria\n'))
        if decisao3 == 1:

            for i in produtos:
                nomeProdutos.append(i['nome'])

            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor+1)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('quantidade vendida em reais')
            plt.xlabel('produtos')
            plt.show()
        if decisao3 ==2:
            grupoUnico = []
            grupoUnico.clear()

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('erro na consulta')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select *from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()

            except:
                print('erro na consulta')

            for i in grupo:
                grupoUnico.append(i['nome'])

            grupoUnico = sorted(set(grupoUnico))

            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['nome']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)

            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('quantidade unitaria vendida')
            plt.xlabel('produtos')
            plt.show()

    elif estado == 2:
        decisao3 = int(input('\ndigite 1 para pesquisar por dinheiro e 2 por quantidade unitaria\n'))
        if decisao3 == 1:

            for i in produtos:
                nomeProdutos.append(i['grupo'])

            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['grupo'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('quantidade vendida em reais')
            plt.xlabel('produtos')
            plt.show()

        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('erro na consulta')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select *from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()

            except:
                print('erro na consulta')

            for i in grupo:
                grupoUnico.append(i['grupo'])

            grupoUnico = sorted(set(grupoUnico))

            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['grupo']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)

            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('quantidade unitaria vendida')
            plt.xlabel('produtos')
            plt.show()







while not autentico:

    decisao = int(input('\nDigite 1 para logar e 2 para se cadastrar\n'))


    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()
    except:
        print('erro no banco de dados')

    autentico, usuarioSupremo = logarCadastrar(decisao)


if autentico:
    print('autenticado')

    if usuarioSupremo == True:
        decisaoUsuario = 1

        while decisaoUsuario != 0:
            decisaoUsuario = int(input('\ndigite  0 para sair, 1 para cadastrar produtos, 2 para listar produtos cadastrados, 3 para listar os pedidos, 4 para visualizar as estatisticas\n'))

            if decisaoUsuario == 1:
                cadastrarProdutos()
            elif decisaoUsuario ==2:
                listarProdutos()

                delete = int(input('\ndigite 1 para excluir um produto e 2 para sair\n'))
                if delete == 1:
                    excluirProdutos()
            elif decisaoUsuario ==3:
                listarPedidos()
            elif decisaoUsuario ==4:
                gerarEstatistica()
