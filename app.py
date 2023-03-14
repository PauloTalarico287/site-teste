from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "Olá, mundo! Esse é meu site. (Paulo Talarico)"

@app.route("/sobre")
def sobre():
  return "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return "Aqui vai o conteúdo da página Contato"
