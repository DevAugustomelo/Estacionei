from PyQt5 import uic, QtWidgets
import sqlite3


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
            Tela03.show()
        else:
            Login.lbl_erro.setText("Dados inválidos!!!!")


def logout():
    Tela03.close()
    Login.show()


def exibe_cadastro():
    Cadastro.show()


def cadastrar():
    nome = Cadastro.line_nome.text()
    login = Cadastro.line_login.text()
    senha = Cadastro.line_senha.text()
    repetir_senha = Cadastro.line_senha_2.text()

    # condicional para cadastrar no banco de dados

    if senha == repetir_senha:
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
Tela03 = uic.loadUi("Tela03.ui")
Cadastro = uic.loadUi("Cadastro.ui")

Login.btn_entrar.clicked.connect(validar)
Login.btn_cadastro.clicked.connect(exibe_cadastro)
Cadastro.btn_cadastrar.clicked.connect(cadastrar)
Tela03.pushButton_2.clicked.connect(logout)
Login.line_senha.setEchoMode(QtWidgets.QLineEdit.Password)

Login.show()
app.exec()









