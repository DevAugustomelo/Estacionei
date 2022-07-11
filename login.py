from PyQt5 import uic, QtWidgets
import sqlite3
from datetime import datetime



data_atual = datetime.now()


def data():
    data_formatada = data_atual.strftime('%d/%m/%Y')
    return data_formatada


def hora():
    hora_formatada = data_atual.strftime('%H:%M:%S')
    return hora_formatada


def validar():
    Login.lbl_erro.setText("")
    usuario = Login.line_user.text()
    senha = Login.line_senha.text()
    conexao_banco = sqlite3.connect('dados_clientes.db')
    cursor = conexao_banco.cursor()

    cursor.execute("SELECT login FROM dados WHERE senha = '{}'".format(senha))
    login_bd = cursor.fetchall()
    conexao_banco.close()

    if usuario != login_bd[0][0]:
        Login.lbl_erro.setText("Login não cadastrado!")
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
            Login.lbl_erro.setText("Dados inválidos!!!!")




def logout():
    Gestor.close()
    Login.show()


def exibe_cadastro():
    Cadastro.show()


def cadastrar():
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
            conexao_banco = sqlite3.connect('dados_clientes.db')
            cursor = conexao_banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS dados(nome text, login text, senha text)")
            cursor.execute("INSERT INTO dados Values ('"+nome+"', '"+login+"', '"+senha+"')")

            conexao_banco.commit()
            conexao_banco.close()
            Cadastro.lbl_erro.setText("Usuário cadastrado com sucesso!")

        except sqlite3.Error as erro:
            print('Erro na inserção de dados: ', erro)

    else:
        Cadastro.lbl_erro.setText("As senhas digitadas são distintas!")


app = QtWidgets.QApplication([])

Login = uic.loadUi("Login.ui")
Gestor = uic.loadUi("Gestor.ui")
Cadastro = uic.loadUi("Cadastro.ui")



Login.btn_entrar.clicked.connect(validar)                    # Chama a função validar ao Clicar
Login.line_senha.returnPressed.connect(validar)              # Chama a função validar ao pressionar enter
Login.btn_cadastro.clicked.connect(exibe_cadastro)
Cadastro.btn_cadastrar.clicked.connect(cadastrar)
Gestor.pushButton_2.clicked.connect(logout)
Login.line_senha.setEchoMode(QtWidgets.QLineEdit.Password)   # define formato visualização protegida no campo senha

Gestor.lbl_data.setText(data())
Gestor.lbl_hora.setText(hora())

Login.show()
app.exec()









