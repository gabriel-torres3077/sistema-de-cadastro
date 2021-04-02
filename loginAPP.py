import mysql.connector
import re
import smtplib

#definir banco de dados para conectar
mydb = mysql.connector.connect(
  host="HOST SQL",
  user="USUARIO SQL",
  password="SENHA SQL"
)
mycursor = mydb.cursor()
mycursor.execute("USE users")

#CARACTERES REJEITADOS EM EMAILS
regect = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def send_email(user, email):
    #MENSAGEM PARA ENVIO
    subject = 'App para cadastro de contas usando Python, MySQL e SMTP'
    menssage = 'Ola {}, sua conta foi criada com sucesso!'.format(user)
    msg = ("Subject: {}\n\n{}".format(subject, menssage)).encode('utf-8')
    #CONTA BASE PARA ENVIAR A MENSAGEM
    From = "EMAIL SEM @gmail/ @hotmail(ex: meuemail)"
    password = "SENHA"
    #DIFINIR CONTA PARA RECEBER A MENSAGEM(USUÁRIO)
    To = email
    #CRIAR INSTANCIA DO SERVIDOR
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(From, password)
    #ENVIAR EMAIL
    server.sendmail(From, To, msg)
    server.quit()


def create_account(): #criar conta nova
    new_user = str(input('Ensira o nome do usuário: '))
    new_password = str(input('Ensira sua senha: '))
    new_email = str(input('Ensira seu email: '))
    #validar email
    if (re.search(regect, new_email)):
        #buscar Valores repitidos no banco de dados
        userCheck = "SELECT * FROM usuarios WHERE login = '{}'".format(new_email)
        mycursor.execute(userCheck)
        user = mycursor.fetchall()
        if user == []:
            # Criar novo usuário
            insert_into = "INSERT INTO usuarios (id, login, password, email) VALUES (default, %s, %s, %s)"
            values = (new_user, new_password, new_email)
            mycursor.execute(insert_into, values)
            send_email(new_user, new_email)
            return print('Conta cadastrada com sucesso!')
        else:
            return print('Ja existe um usuarios cadastrado com esse email!')

    else:
        return print('Email Inválido, tente novamente')


create_account()
