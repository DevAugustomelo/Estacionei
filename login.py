from PyQt5 import uic, QtWidgets
import sqlite3
from datetime import datetime


def data_str(x, y):
    une_str = x + ' ' + y
    data_atual = datetime.now()
    entrada = data_atual.strptime(une_str, "%d/%m/%Y %H:%M:%S")
    return entrada


def data():
    data_atual = datetime.now()
    data_formatada = data_atual.strftime('%d/%m/%Y')
    return data_formatada


def hora():
    data_atual = datetime.now()
    hora_formatada = data_atual.strftime('%H:%M:%S')
    return hora_formatada


def placa_padrao(placa):

    import string

    letras = list(string.ascii_uppercase)
    letras = letras[0:10]

    a = placa[0:3].isalpha()
    b = placa[3:7].isdigit()
    c = placa[3].isdigit() and placa[4].isalpha() and placa[5:7].isdigit()

    if a and b:
        return "clássico"

    elif a and c and placa[4] in letras:
        return "Mercosul"
    else:
        return "fora do padrão"


def validar():
    Login.lbl_erro.setText("")
    usuario = Login.line_user.text().strip()
    senha = Login.line_senha.text()
    conexao_banco = sqlite3.connect('dados_estacionei.db')
    cursor = conexao_banco.cursor()

    cursor.execute("SELECT login FROM dados WHERE login = '{}'".format(usuario))
    login_bd = cursor.fetchall()
    conexao_banco.close()

    if len(login_bd) < 1:
        Login.lbl_erro.setText("!Login não cadastrado!")
    else:
        conexao_banco = sqlite3.connect('dados_estacionei.db')
        cursor = conexao_banco.cursor()
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
    banco = sqlite3.connect('dados_estacionei.db')
    cursor = banco.cursor()
    cursor.execute("SELECT nome FROM dados WHERE nome = '{}'".format(nome))
    nome_bd = cursor.fetchall()


    if nome == "" or login == "" or senha == "" or repetir_senha == "":
        Cadastro.lbl_erro.setText("* Todos os campos são obrigatórios")

    elif len(nome_bd) > 0 and nome == nome_bd[0][0]:
        Cadastro.lbl_erro.setText("* Usuário já está cadastrado.")

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
    placa = Gestor.line_placa_entrada.text().upper()
    data_entrada = data()
    hora_entrada = hora()

    banco = sqlite3.connect('dados_estacionei.db')
    cursor = banco.cursor()
    cursor.execute("SELECT Placa FROM entrada WHERE Placa = '{}'".format(placa))
    placa_bd = cursor.fetchall()

    banco.close()

    if len(placa) != 7:
        Gestor.lbl_erro.setText("* Verifique a quantidade de Caracteres.")

    elif placa_padrao(placa) == "fora do padrão":
        Gestor.lbl_erro.setText("!Fora do padrão Clássico ou Mercosul")

    elif placa_bd != [] and placa == placa_bd[0][0]:
        Gestor.lbl_erro.setText("* !Esta placa já existe!")

    else:
        try:
            banco = sqlite3.connect('dados_estacionei.db')
            cursor = banco.cursor()
            cursor.execute(f"INSERT INTO entrada Values('{placa}','{data_entrada}', '{hora_entrada}')")
            banco.commit()
            banco.close()
            Gestor.lbl_erro.setText("<< Dados inseridos com sucesso >>")

            Gestor.lbl_data.setText(data())
            Gestor.lbl_hora.setText(hora())
            Gestor.line_placa_entrada.setText("")
        except Exception as erro:
            print("Erro Inesperado: ", erro)


def banco_saida():
    placa = Gestor.line_placa_saida.text().upper()
    data_saida = data()
    hora_saida = hora()

    banco = sqlite3.connect('dados_estacionei.db')
    cursor = banco.cursor()

    cursor.execute("SELECT Placa FROM entrada WHERE Placa = '{}'".format(placa))
    placa_bd = cursor.fetchall()
    banco.close()

    if placa == "":
        Gestor.lbl_erro_2.setText("* Digite a Placa antes de confirmar")

    elif len(placa_bd) < 1:
        Gestor.lbl_erro_2.setText("!Placa não cadastrada!")


    else:
        try:
            banco = sqlite3.connect('dados_estacionei.db')
            cursor = banco.cursor()

            cursor.execute("SELECT DataEntrada FROM entrada WHERE Placa = '{}'".format(placa))
            data_entrada_bd = cursor.fetchall()
            data_str_bd = data_entrada_bd[0][0]

            cursor.execute("SELECT HoraEntrada FROM entrada WHERE Placa = '{}'".format(placa))
            hora_entrada_bd = cursor.fetchall()
            hora_str_bd = hora_entrada_bd[0][0]

            d_entrada = data_str(data_str_bd, hora_str_bd)
            d_saida = data_str(data_saida, hora_saida)
            permanencia = d_saida - d_entrada


            cursor.execute("CREATE TABLE IF NOT EXISTS saida (Placa text, DataEntrada text, HoraEntrada text, DataSaida text, HoraSaida text, Permanencia text)")
            cursor.execute(f"INSERT INTO saida Values('{placa}', '{data_str_bd}', '{hora_str_bd}', '{data_saida}', '{hora_saida}', '{permanencia}')")
            cursor.execute("DELETE from entrada WHERE Placa = '{}'".format(placa))

            banco.commit()
            banco.close()
            Gestor.lbl_data_entrada.setText(data_str_bd)
            Gestor.lbl_hora_entrada.setText(hora_str_bd)
            Gestor.line_placa_saida.setText("")
            Gestor.lbl_data_saida.setText(data())
            Gestor.lbl_hora_saida.setText(hora())

            Gestor.lbl_erro_2.setText("<< Atualizado com sucesso >>")

        except Exception as erro:
            Gestor.lbl_erro_2.setText("!Esta Placa não teve entrada!")


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
    banco = sqlite3.connect('dados_estacionei.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM saida")
    busca = cursor.fetchall()  # Retorna os dados em formato de matriz
    Gestor.tabela_historico.setRowCount(len(busca))  # Cria linhas de acordo com a quantidade de registros no banco
    Gestor.tabela_historico.setColumnCount(6)  # Cria a quantidade de colunas que será exibida

    # Percorre a matriz da busca e organiza a forma que o resultado é exibido

    for x in range(0, len(busca)):
        for k in range(0, 6):  # 6 sendo a quantidade de colunas
            Gestor.tabela_historico.setItem(x, k, QtWidgets.QTableWidgetItem(str(busca[x][k])))

    banco.close()


def deletar():
    banco = sqlite3.connect('dados_estacionei.db')
    cursor = banco.cursor()

    cursor.execute("DELETE from saida")

    cursor.execute("SELECT * FROM saida")
    busca = cursor.fetchall()  # Retorna os dados em formato de matriz
    Gestor.tabela_historico.setRowCount(len(busca))  # Cria linhas de acordo com a quantidade de registros no banco
    Gestor.tabela_historico.setColumnCount(6)  # Cria a quantidade de colunas que será exibida

    # Percorre a matriz da busca e organiza a forma que o resultado é exibido

    for x in range(0, len(busca)):
        for k in range(0, 6):  # 6 sendo a quantidade de colunas
            Gestor.tabela_historico.setItem(x, k, QtWidgets.QTableWidgetItem(str(busca[x][k])))
    banco.commit()
    banco.close()


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
Gestor.btn_ok_saida.clicked.connect(banco_saida)
Gestor.btn_limpar.clicked.connect(deletar)
Gestor.btn_atualizar.clicked.connect(consulta)
Gestor.btn_atualizar2.clicked.connect(historico)



Login.line_senha.setEchoMode(QtWidgets.QLineEdit.Password)   # define formato visualização protegida no campo senha



Login.show()
app.exec()


