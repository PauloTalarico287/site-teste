import gspread
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as fobj:
  fobj.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta) # sheets.new
planilha = api.open_by_key("1Bk0tYfWtQCWZBlWxUtfXcca9iP5NuTXEI1mg_JC3JUo")
sheet = planilha.worksheet("Página1")
sheet2= planilha.worksheet("Página2")
sheet3= planilha.worksheet("Página3")

planilha2=api.open_by_key("1cmT3CmymxcIDi2dxHa8nuI-S7d-AUYbd9C7-gcQ7YhY")
sheet_novo = planilha2.worksheet("Página1")

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
  scraper = ChannelScraper()
  contador = 0
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    conteudo += f"<li>{message.created_at} {texto}</li>"
    if contador == 10:
      break
  return conteudo + "</ul>"

@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["Paulo", "Talarico", "a partir do Flasck"])
  return "Planilha escrita!"

#@app.route("/telegram-bot", methods=["POST"])
#def telegram_bot():
  #update = request.json
  #chat_id = update["message"]["chat"]["id"]
  #message = update["message"]["text"]
  #nova_mensagem = {"chat_id": chat_id, "text": message}
  #requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)

  
@app.route("/telegram-bot", methods=['POST'])
def telegram_bot():
  update = request.json
  message = update["message"]["text"]
  chat_id = update["message"]["chat"]["id"]
  if message == "/start":
    texto_resposta = "Olá! Seja bem-vinda(o) ao Orçamendômetro SP, produzido pela Agência Mural.\nAqui você poderá saber quanto a Prefeitura de São Paulo investiu na sua região. Digite o número da subprefeitura que gostaria de saber a execução orçamentária:\n0) Toda a cidade, \n1) Aricanduva/Formosa/Carrão,\n2) Butantã,\n3) Campo Limpo,\n4) Capela do Socorro,\n5) Casa Verde/Cachoeirinha,\n6) Cidade Ademar,\n7) Cidade Tiradentes,\n8) Guaianases,\n9) Vila Prudente,\n10) Ermelino Matarazzo,\n11) Freguesia/Brasilândia,\n12) Ipiranga,\n13) Itaim Paulista,\n14) Itaquera,\n15) Jabaquara,\n16) Jaçanã/Tremembé,\n17) Lapa,\n18) M'Boi Mirim,\n19) Mooca,\n20) Parelheiros,\n21) Penha,\n22) Perus/Anhanguera,\n23) Pinheiros,\n24) Pirituba/Jaraguá,\n25) Santana/Tucuruvi,\n26) Santo Amaro,\n27) São Mateus,\n28) São Miguel Paulista,\n29) Sapopemba,\n30) Sé,\n31) Vila Maria/Vila Guilherme,\n32) Vila Mariana."
  elif message == "Olá":
    texto_resposta = "Olá! Seja bem-vinda(o) ao Orçamendômetro SP, produzido pela Agência Mural.\nAqui você poderá saber quanto a Prefeitura de São Paulo investiu na sua região. Digite o número da subprefeitura que gostaria de saber a execução orçamentária:\n1) Aricanduva/Formosa/Carrão,\n2) Butantã,\n3) Campo Limpo,\n4) Capela do Socorro,\n5) Casa Verde/Cachoeirinha,\n6) Cidade Ademar,\n7) Cidade Tiradentes,\n8) Guaianases,\n9) Vila Prudente,\n10) Ermelino Matarazzo,\n11) Freguesia/Brasilândia,\n12) Ipiranga,\n13) Itaim Paulista,\n14) Itaquera,\n15) Jabaquara,\n16) Jaçanã/Tremembé,\n17) Lapa,\n18) M'Boi Mirim,\n19) Mooca,\n20) Parelheiros,\n21) Penha,\n22) Perus/Anhanguera,\n23) Pinheiros,\n24) Pirituba/Jaraguá,\n25) Santana/Tucuruvi,\n26) Santo Amaro,\n27) São Mateus,\n28) São Miguel Paulista,\n29) Sapopemba,\n30) Sé,\n31) Vila Maria/Vila Guilherme,\n32) Vila Mariana,\n0)Reportagem completa."
  elif message == "1":
    texto_resposta = "A Subprefeitura Aricanduva/Formosa/Carrão gastou R$ 36.568.830,66 em serviços públicos ao longo de 2022. O valor corresponde a 84.05% do planejado para o ano, quando o orçamento previsto era de R$ 43.509.416,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa."
  elif message == "2":
    texto_resposta ='A Subprefeitura Butantã gastou R$ 36.921.397,88 em serviços públicos ao longo de 2022. O valor corresponde a 92.25% do planejado para o ano, quando o orçamento previsto era de R$ 40.023.094,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "3":
    texto_resposta ='A Subprefeitura Campo Limpo gastou R$ 44.291.072,27 em serviços públicos ao longo de 2022. O valor corresponde a 85.26% do planejado para o ano, quando o orçamento previsto era de R$ 51.949.802,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "4":
    texto_resposta ='A Subprefeitura Capela do Socorro gastou R$ 50.382.105,53 em serviços públicos ao longo de 2022. O valor corresponde a 98.06% do planejado para o ano, quando o orçamento previsto era de R$ 51.377.912,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "5":
    texto_resposta = 'A Subprefeitura Casa Verde/Cachoeirinha gastou R$ 33.866.963,54 em serviços públicos ao longo de 2022. O valor corresponde a 68.34% do planejado para o ano, quando o orçamento previsto era de R$ 49.559.237,00. Confira mais sobre a região: https://bit.ly/3zayIy5. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "6":
    texto_resposta = 'A Subprefeitura Cidade Ademar gastou R$ 52.077.759,71 em serviços públicos ao longo de 2022. O valor corresponde a 115.51% do planejado para o ano, quando o orçamento previsto era de R$ 45.085.343,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "7":
    texto_resposta = 'A Subprefeitura Cidade Tiradentes gastou R$ 25.784.337,67 em serviços públicos ao longo de 2022. O valor corresponde a 76.54% do planejado para o ano, quando o orçamento previsto era de R$ 33.685.683,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "8":
    texto_resposta = 'A Subprefeitura de Guaianases gastou R$ 45.959.773,16 em serviços públicos ao longo de 2022. O valor corresponde a 91.63% do planejado para o ano, quando o orçamento previsto era de R$ 50.159.302,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "9":
    texto_resposta = 'A Subprefeitura de Vila Prudente gastou R$ 27.274.641,73 em serviços públicos ao longo de 2022. O valor corresponde a 77.33% do planejado para o ano, quando o orçamento previsto era de R$ 35.268.391,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "10":
    texto_resposta = 'A Subprefeitura Ermelino Matarazzo gastou R$ 30.024.575,42 em serviços públicos ao longo de 2022. O valor corresponde a 95.00% do planejado para o ano, quando o orçamento previsto era de R$ 31.606.121,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "11":
    texto_resposta = 'A Subprefeitura Freguesia/Brasilândia gastou R$ 37.355.664,82 em serviços públicos ao longo de 2022. O valor corresponde a 102.29% do planejado para o ano, quando o orçamento previsto era de R$ 36.520.179,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "12":
    texto_resposta = 'A Subprefeitura Ipiranga gastou R$ 34.993.820,19 em serviços públicos ao longo de 2022. O valor corresponde a 89.45% do planejado para o ano, quando o orçamento previsto era de R$ 39.122.951,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "13":
    texto_resposta = 'A Subprefeitura Itaim Paulista gastou R$ 33.278.381,84 em serviços públicos ao longo de 2022. O valor corresponde a 62.03% do planejado para o ano, quando o orçamento previsto era de R$ 53.647.372,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "14":
    texto_resposta = 'A Subprefeitura Itaquera gastou R$ 39.302.438,70 em serviços públicos ao longo de 2022. O valor corresponde a 81.65% do planejado para o ano, quando o orçamento previsto era de R$ 48.132.695,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "15":
    texto_resposta ='A Subprefeitura Jabaquara gastou R$ 31.578.621,35 em serviços públicos ao longo de 2022. O valor corresponde a 91.42% do planejado para o ano, quando o orçamento previsto era de R$ 34.542.799,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "16":
    texto_resposta = 'A Subprefeitura Jaçanã/Tremembé gastou R$ 39.500.406,95 em serviços públicos ao longo de 2022. O valor corresponde a 106.74% do planejado para o ano, quando o orçamento previsto era de R$ 37.004.697,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "17":
    texto_resposta = 'A Subprefeitura Lapa gastou R$ 37.044.176,24 em serviços públicos ao longo de 2022. O valor corresponde a 80.87% do planejado para o ano, quando o orçamento previsto era de R$ 45.809.043,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "18":
    texto_resposta = "A Subprefeitura M'Boi Mirim gastou R$ 75.591.793,20 em serviços públicos ao longo de 2022. O valor corresponde a 139.87% do planejado para o ano, quando o orçamento previsto era de R$ 54.042.969,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa."
  elif message == "19":
    texto_resposta ='A Subprefeitura Mooca gastou R$ 45.192.067,02 em serviços públicos ao longo de 2022. O valor corresponde a 105.21% do planejado para o ano, quando o orçamento previsto era de R$ 42.954.814,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "20":
    texto_resposta ='A Subprefeitura Parelheiros gastou R$ 120.585.653,38 em serviços públicos ao longo de 2022. O valor corresponde a 144.64% do planejado para o ano, quando o orçamento previsto era de R$ 83.368.309,00. Confira mais sobre a região: https://bit.ly/3lKBas2. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "21":
    texto_resposta ='A Subprefeitura Penha gastou R$ 46.803.990,78 em serviços públicos ao longo de 2022. O valor corresponde a 115.23% do planejado para o ano, quando o orçamento previsto era de R$ 40.616.502,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "22":
    texto_resposta ='A Subprefeitura Perus/Anhanguera gastou R$ 36.003.708,90 em serviços públicos ao longo de 2022. O valor corresponde a 120.48% do planejado para o ano, quando o orçamento previsto era de R$ 29.883.048,00. Confira mais sobre a região: https://bit.ly/3zayIy5. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "23":
    texto_resposta ='A Subprefeitura Pinheiros gastou R$ 39.657.330,86 em serviços públicos ao longo de 2022. O valor corresponde a 93.18% do planejado para o ano, quando o orçamento previsto era de R$ 42.559.302,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "24":
    texto_resposta ='A Subprefeitura Pirituba/Jaraguá gastou R$ 36.756.827,44 em serviços públicos ao longo de 2022. O valor corresponde a 89.97% do planejado para o ano, quando o orçamento previsto era de R$ 40.854.599,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "25":
    texto_resposta ='A Subprefeitura Santana/Tucuruvi gastou R$ 32.648.015,27 em serviços públicos ao longo de 2022. O valor corresponde a 88.48% do planejado para o ano, quando o orçamento previsto era de R$ 36.898.614,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "26":
    texto_resposta ='A Subprefeitura Santo Amaro gastou R$ 34.411.349,99 em serviços públicos ao longo de 2022. O valor corresponde a 85.62% do planejado para o ano, quando o orçamento previsto era de R$ 40.192.751,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "27":
    texto_resposta = 'A Subprefeitura São Mateus gastou R$ 52.985.212,73 em serviços públicos ao longo de 2022. O valor corresponde a 96.89% do planejado para o ano, quando o orçamento previsto era de R$ 54.683.813,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "28":
    texto_resposta ='A Subprefeitura São Miguel Paulista gastou R$ 45.504.087,19 em serviços públicos ao longo de 2022. O valor corresponde a 96.96% do planejado para o ano, quando o orçamento previsto era de R$ 46.929.108,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "29":
    texto_resposta = "A Subprefeitura Sapopemba gastou R$ 27.852.938,60 em serviços públicos ao longo de 2022. O valor corresponde a 60.70% do planejado para o ano, quando o orçamento previsto era de R$ 45.884.095,00. Confira mais sobre a região aqui: https://bit.ly/40CTfqy. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa."
  elif message == "30":
    texto_resposta ='A Subprefeitura Sé gastou R$ 104.587.793,67 em serviços públicos ao longo de 2022. O valor corresponde a 98.93% do planejado para o ano, quando o orçamento previsto era de R$ 105.719.708,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "31":
    texto_resposta = 'A Subprefeitura Vila Maria/Vila Guilherme gastou R$ 27.269.037,81 em serviços públicos ao longo de 2022. O valor corresponde a 70.28% do planejado para o ano, quando o orçamento previsto era de R$ 38.799.179,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "32":
    texto_resposta ='A Subprefeitura Vila Mariana gastou R$ 50.278.531,66 em serviços públicos ao longo de 2022. O valor corresponde a 112.90% do planejado para o ano, quando o orçamento previsto era de R$ 44.534.373,00. Se quiser saber de outra região digite o número correspondente à subprefeitura ou digite 0 se quiser acessar a reportagem completa.'
  elif message == "0":
    texto_resposta ='Confira como a maioria das subprefeituras não realizou os serviços que estavam previstos no orçamento: https://bit.ly/3KcAlR1'
  else:
    texto_resposta = "Não entendi! Para outras informações sobre a cidade de São Paulo, acesse o site da Agência Mural: agenciamural.org.br"
  nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
  requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  return "ok"

@app.route("/mural")
def mural():
  link='https://www.agenciamural.org.br/noticias/'
  requisicao=requests.get(link)
  html=BeautifulSoup(requisicao.content)
  noticias=html.find_all('div',{'class':'texto mt-1'})
  for link in noticias:
    Publicacoes = []
    Autor_e_Data= link.find('span',{'class':'detalhes mt-1 d-block'}).text
    Título = link.find('h2',{"class":"m-0 mt-1"}).text
    Linha_Fina = link.find('p',{"class":"linha-fina m-0 mt-1"}).text
    URL=link.find('a').get('href')
    valores = sheet_novo.col_values(4)
    if URL not in valores:
      Publicacoes.append([Autor_e_Data, Título, Linha_Fina, URL])
      df=pd.DataFrame(Publicacoes, columns=['Autor_e_Data', 'Título', 'Linha_Fina', 'URL'])
      sheet_novo.append_rows(Publicacoes)
      return "Atualizado" 
