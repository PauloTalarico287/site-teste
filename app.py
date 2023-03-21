import requests
import os
from flask import Flask
from tchan import ChannelScraper

TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
app = Flask(__name__)

menu = """
<a href="/">Página Inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a> | <a href="/promocoes">Promoções</a>
<br>
"""

@app.route("/")
def hello_world():
  return menu + "Olá, mundo! Esse é meu site. (Paulo Talarico)"

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return "Mensagem enviada."

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato"

@app.route("/promocoes")
def promocoes():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/promocoeseachadinhos">@promocoeseachadinhos</a>:
  <br>
  <ul>
  """
  for promocao in ultimas_promocoes():
    conteudo += f"<li>{promocao}</li>"
  return conteudo + "</ul>"
