import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = " ",
    database = "willis"
)
cursor = mydb.cursor()
tabela_user = """
CREATE TABLE IF NOT EXISTS usuario_senha(
id INT AUTO_INCREMENT,
usuario VARCHAR(13) NOT NULL UNIQUE,
senha VARCHAR(13) NOT NULL,
nome_exebicao VARCHAR(13),
PRIMARY KEY(id)
)
"""
criando_tabela = cursor.execute(tabela_user)
def fazer_login():
     while True:
        try:
            usuario = input("Usuario : ").strip()
            while usuario == '':
                usuario = input("Não pode deixar esse campo em branco \nUsuario: ")
            senha = input("Senha: ").strip()
            while senha == '':
                senha = input("Não pode deixar esse campo em branco \nSenha: ")
        except Exception as e:
            print("Erro ", e)
        return usuario,senha

def cadastrando():
    while True:
        try:
            print("Cadastrando usuario\nSo é permitido apenas 12 caracteres")
            usuario = input("Usuario: ").strip()
            while usuario == '':
                usuario = input("Não pode deixar esse campo em branco \nUsuario: ")
            while len(usuario) > 12:
                usuario = input("Digite apenas 12 caracteres. \nUsuario: ").strip()
            senha = input("Senha: ").strip()
            while senha == '':
                senha = input("Não pode deixar esse campo em branco \nSenha: ")
            while len(senha) > 12:
                senha = input("Digite apenas 12 caracteres. \nSenha: ").strip()
            confi_senha = input("Confirmar senha: ")
            while confi_senha == '':
                confi_senha = input("Não pode deixar esse campo em branco \nConfirmar senha: ")
            while senha != confi_senha:
                senha = input("Senhas diferentes \nSenha: ")
                confi_senha = input("Confirmar senha: ")
            nome_exebicao = input("Digite um nome de exibição: ").strip()
            while nome_exebicao == '':
                nome_exebicao = input("Não pode deixar esse campo em branco \nDigite um nome de exibição: ").strip()
            while len(nome_exebicao) > 12:
                nome_exebicao = input("Digite apenas 12 caracteres. \nDigite um nome de exibição: ").strip()

        except Exception as e:
            print("Erro ", e)
        return [usuario,senha,nome_exebicao]

def conectando():
    while True:
        try:
            conectar = int(input("Selecione uma das opções: \n[1]Para login. \n[2]Para criar uma nova conta\n>>>"))
            while conectar not in [1,2]:
                conectar = int(input("\033[31mOpção invalida\033[0m\nSelecione uma das opções: \n[1]Para login. \n[2]Para criar uma nova conta\n>>> "))
        except  ValueError:
            print("\033[31mOpção invalida\033[0m]")
        return conectar
    
conf_opcao = conectando()
if conf_opcao == 1:
    login = fazer_login()
    usuario = login[0]
    senha = login[1]
    query = "SELECT * FROM usuario_senha WHERE usuario = %s"
    cursor.execute(query,(usuario,))
    consulta = cursor.fetchone()
    if consulta:
        if consulta[2]== senha:
            print(f"Bem vindo {consulta[3]}")
        else:
            print("Senha incorreto.")
    else:
        print("Usuario inexistente.")

elif conf_opcao == 2:
    cadastro = cadastrando()
    query = """
INSERT INTO usuario_senha(usuario,senha,nome_exebicao)
VALUES(%s,%s,%s)
"""
    valores = (cadastro[0],cadastro[1],cadastro[2])
    try:
        cursor.execute(query,valores)
        mydb.commit()
        print(f"{cadastro[2]} cadastrado com sucesso")
    except mysql.connector.Error as e:
        print("Erro ao cadastrar o usuario",e)
        mydb.rollback()
    
cursor.close()
mydb.close()