from flask import Flask, render_template, redirect, request, flash, session, send_from_directory
import pyodbc
import json
import ast
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "Da"


logado = False

@app.route('/')
def home():
    global logado
    logado = False

    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado == True:
        with open('usuario.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)

        return render_template('adm.html', usuarios=usuarios)
    if logado == False:
        return redirect('/')


@app.route('/usuario')
def usuario():
    if logado == True:
        arquivo = []
        for documento in os.listdir('Pasta_Arquivos'):
            arquivo.append(documento)
        return render_template("usuario.html", Pasta_Arquivos=arquivo)
    else:
        flash('Você precisa fazer login')
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():

    global logado

    with open('usuario.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)

        cont = 0
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        id = request.form.get('id')

        if nome == 'adm' and senha == '000':
            logado = True
            return redirect('/adm')

        for usuario in usuarios:
            cont += 1

            if usuario['nome'] == nome and usuario['senha'] == senha:
                logado = True
                # Armazena todas as informações do usuário na sessão
                session['usuario'] = usuario
                return redirect('/usuario')

            if cont >= len(usuarios):

                flash('Usuário ou senha inválidos')
                return redirect('/')

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    id = request.form.get('id')
    user = [
        {
            "nome": nome,
            "senha": senha,
            "id": id
        }
    ]
    with open('usuario.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)

    usuarioNovo = usuarios + user

    with open('usuario.json', 'w') as gravarTemp:
        json.dump(usuarioNovo, gravarTemp, indent=4)

    flash(f'{nome} Cadastrado')
    return redirect('/adm')


@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('usuarioExcluir')
    usuario_Dict = ast.literal_eval(usuario) #transformar para dicionario
    nome = usuario_Dict['nome']
    with open('usuario.json') as usuariosTemp:
        usuario_JSON = json.load(usuariosTemp)
        for i in usuario_JSON:
            if i == usuario_Dict:
                usuario_JSON.remove(usuario_Dict)
                with open('usuario.json', 'w') as usuarioExcluir:
                    json.dump(usuario_JSON, usuarioExcluir, indent=4)

    flash(f'{nome} Excluido')
    return redirect('/adm')


@app.route("/upload", methods=['POST'])
def upload():
    global logado
    logado = True

    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace(" ", "")
    arquivo.save(os.path.join('Pasta_Arquivos', nome_arquivo))
    flash('Arquivo Enviado')

    return redirect('/adm')

@app.route('/download', methods=['POST'])
def download():
    nome_Arquivo = request.form.get('arquivos_Download')

    return send_from_directory('Pasta_Arquivos', nome_Arquivo, as_attachment=True)


# Para rodar funcionar e acessar o site * in: __nome do cod__ no caso main.py
if __name__ in "__main__":
     app.run(debug=True)


# continuar pelo video 14





