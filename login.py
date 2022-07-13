from PyQt5 import uic, QtWidgets
import sqlite3
from datetime import datetime






def data():
    data_atual = datetime.now()
    data_formatada = data_atual.strftime('%d/%m/%Y')
    return data_formatada


def hora():
    data_atual = datetime.now()
    hora_formatada = data_atual.strftime('%H:%M:%S')
    return hora_formatada


def formatar(x):
    lista = []
    lista.append(x)
    tupla = tuple(lista)
    lista2 = []
    lista2.append(tupla)
    return lista2


def validar():
    Login.lbl_erro.setText("")
    usuario = Login.line_user.text()
    senha = Login.line_senha.text()
    conexao_banco = sqlite3.connect('dados_estacionei.db')
    cursor = conexao_banco.cursor()

    cursor.execute("SELECT login FROM dados WHERE login = '{}'".format(usuario))
    login = cursor.fetchall()
    formatar(usuario)

    if  formatar(usuario) != login:

        Login.lbl_erro.setText("!Login não cadastrado!")
    else:
        cursor.execute("SELECT senha FROM dados WHERE login = '{}'".format(usuario))
        senha_bd = cursor.fetchall()
        conexao_banco.close()

        if senha == senha_bd[0][0]:
            Login.close()
            Gestor.show()
            # Limpa os campos após inserir os dados
            Login.line_user.setText("")
            Login.line_senha.setText("")
        else:
            Login.lbl_erro.setText("!Senha incorreta!")




def logout():
    Gestor.close()
    Login.show()


def exibe_cadastro():
    Cadastro.show()


def cadastrar():
    Cadastro.lbl_erro.setText("")
    nome = Cadastro.line_nome.text()
    login = Cadastro.line_login.text()
    senha = Cadastro.line_senha.text()
    repetir_senha = Cadastro.line_senha_2.text()

    # condicional para cadastrar no banco de dados

    if nome == "" or login == "" or senha == "" or repetir_senha == "":
        Cadastro.lbl_erro.setText("* Todos os campos são obrigatórios")


    # condicional e criação do banco de dados
    elif senha == repetir_senha:
        try:
            conexao_banco = sqlite3.connect('dados_estacionei.db')
            cursor = conexao_banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS dados(nome text, login text, senha text)")
            cursor.execute(f"INSERT INTO dados Values ('{nome}', '{login}', '{senha}')")

            conexao_banco.commit()
            conexao_banco.close()
            Cadastro.line_nome.setText("")
            Cadastro.line_login.setText("")
            Cadastro.line_senha.setText("")
            Cadastro.line_senha_2.setText("")
            Cadastro.lbl_erro.setText("<< Usuário cadastrado com sucesso >>")

        except sqlite3.Error as erro:
            Cadastro.lbl_erro.setText('!Erro na inserção de dados: ', erro)

    else:
        Cadastro.lbl_erro.setText("!As senhas digitadas são distintas!")



def banco_entrada():
    placa = Gestor.line_placa_entrada.text()
    data_entrada = data()
    hora_entrada = hora()

    if placa == "":
        Gestor.lbl_erro.setText("* Digite a Placa antes de confirmar")

    else:
        try:
            banco = sqlite3.connect('dados_estacionei.db')
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS entrada (Placa text, DataEntrada text, HoraEntrada text)")
            cursor.execute(f"INSERT INTO entrada Values('{placa}','{data_entrada}', '{hora_entrada}')")
            banco.commit()
            banco.close()
            Gestor.line_placa_entrada.setText("")
            Gestor.lbl_data.setText(data())
            Gestor.lbl_hora.setText(hora())

            Gestor.lbl_erro.setText("<< Dados inseridos com sucesso >>")

        except sqlite3.Error as erro:
            Gestor.lbl_erro.setText("!Ocorreu um erro inesperado!", erro)


def consulta():
    banco = sqlite3.connect('dados_estacionei.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM entrada")
    busca = cursor.fetchall()    # Retorna os dados em formato de matriz
    Gestor.tabela_consulta.setRowCount(len(busca))  # Cria linhas de acordo com a quantidade de registros no banco
    Gestor.tabela_consulta.setColumnCount(3)        # Cria a quantidade de colunas que será exibida

    # Percorre a matriz da busca e organiza a forma que o resultado é exibido

    for x in range(0, len(busca)):
        for k in range(0, 3): # 3 sendo a quantidade de colunas
            Gestor.tabela_consulta.setItem(x, k, QtWidgets.QTableWidgetItem(str(busca[x][k])))

    banco.close()


def historico():
    pass



app = QtWidgets.QApplication([])

Login = uic.loadUi("Login.ui")
Gestor = uic.loadUi("Gestor.ui")
Cadastro = uic.loadUi("Cadastro.ui")



Login.btn_entrar.clicked.connect(validar)                    # Chama a função validar ao Clicar
Login.line_senha.returnPressed.connect(validar)              # Chama a função validar ao pressionar enter
Login.btn_cadastro.clicked.connect(exibe_cadastro)

Cadastro.btn_cadastrar.clicked.connect(cadastrar)

Gestor.pushButton_2.clicked.connect(logout)
Gestor.btn_ok_entrada.clicked.connect(banco_entrada)
Gestor.btn_atualizar.clicked.connect(consulta)
Gestor.btn_atualizar2.clicked.connect(historico)



Login.line_senha.setEchoMode(QtWidgets.QLineEdit.Password)   # define formato visualização protegida no campo senha



Login.show()
app.exec()


