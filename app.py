import datetime
import gspread
import json
import pandas as pd
import requests
import os
import sendgrid
from bs4 import BeautifulSoup
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from tchan import ChannelScraper

SENDGRID_KEY = os.environ["SENDGRID_KEY"]
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

planilha2=api.open_by_key("18cS8RByMKoDUdjlYZQx3j6_uHPOwGbT2w-wqVVhb9Dg")
sheet_novo = planilha2.worksheet("Teste - Publicações no site")

planilha3=api.open_by_key("1HFKm-eINHeoCkYnqsKsc1elEuSRKIh9Q8MoJbkySES4")
sheet_leis = planilha3.worksheet("Página3")

app = Flask(__name__)

menu = """
<a href="/">Página Inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a> | <a href="/promocoes">Promoções</a>
<br>
"""

@app.route("/")
def hello_world():
  return menu + "Olá, mundo! Esse é meu site. (Paulo Talarico)"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato"

@app.route("/telegram-bot", methods=['POST'])
def telegram_bot():
  update = request.json
  message = update["message"]["text"]
  chat_id = update["message"]["chat"]["id"]
  datahora = str(datetime.datetime.fromtimestamp(update["message"]["date"]))
  first_name = update["message"]["from"]["first_name"]    
  if message == "/start":
    texto_resposta = "Olá! Seja bem-vinda(o) ao Orçamendômetro SP, produzido pela Agência Mural.\nAqui você poderá saber quanto a Prefeitura de São Paulo investiu na sua região.\nClique em /menu para começar:" 
  elif message =="/menu":
    texto_resposta = "Clique na opção que você gostaria de saber:\n/a) A subprefeitura que mais gastou do que estava previsto\n/b) A subprefeitura que gastou menos do que estava previsto\n/c) A região da cidade que teve o menor gasto por habitante\n/d) Quero saber de todas as regiões."
  elif message == "/a": 
    texto_resposta = "A Subprefeitura de Parelheiros, no extremo sul, teve o maior gasto entre as administrações. Foram R$ 120 milhões, cerca de R$ 727 por habitante. Clique em /menu para voltar ao começo ou na letra /d para saber de todas as subprefeituras."
  elif message == "/b":
    texto_resposta = "A Subprefeitura de Sapopemba, na zona leste de São Paulo, gastou apenas R$ 6 de cada R$ 10 previstos para 2022. Foram R$ 27 milhões, quando a previsão era de R$ 45 mi. Clique em /menu para voltar ao começo ou na letra /d para saber de todas as subprefeituras."
  elif message == "/c": 
    texto_resposta = "A Subprefeitura do Campo Limpo, na zona sul, gastou R$ 63,18 por habitante em 2022, aponta levantamento da Agência Mural. Em comparação, Parelheiros teve despesas de R$ 727 por morador. Clique em /menu para voltar ao começo ou na letra /d para saber de todas as subprefeituras."
  elif message == "/d":
    texto_resposta = "Clique no número da subprefeitura que gostaria de saber quanto foi gasto:\n/0) Reportagem completa sobre toda a cidade,\n/1) Aricanduva/Formosa/Carrão,\n/2) Butantã,\n/3) Campo Limpo,\n/4) Capela do Socorro,\n/5) Casa Verde/Cachoeirinha,\n/6) Cidade Ademar,\n/7) Cidade Tiradentes,\n/8) Guaianases,\n/9) Vila Prudente,\n/10) Ermelino Matarazzo,\n/11) Freguesia/Brasilândia,\n/12) Ipiranga,\n/13) Itaim Paulista,\n/14) Itaquera,\n/15) Jabaquara,\n/16) Jaçanã/Tremembé,\n/17) Lapa,\n/18) M'Boi Mirim,\n/19) Mooca,\n/20) Parelheiros,\n/21) Penha,\n/22) Perus/Anhanguera,\n/23) Pinheiros,\n/24) Pirituba/Jaraguá,\n/25) Santana/Tucuruvi,\n/26) Santo Amaro,\n/27) São Mateus,\n/28) São Miguel Paulista,\n/29) Sapopemba,\n/30) Sé,\n/31) Vila Maria/Vila Guilherme,\n/32) Vila Mariana."
  elif message == "/1":
    texto_resposta = "A Subprefeitura Aricanduva/Formosa/Carrão gastou R$ 36.568.830,66 em serviços públicos ao longo de 2022. O valor corresponde a 84.05% do planejado para o ano, quando o orçamento previsto era de R$ 43.509.416,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa."
  elif message == "/2":
    texto_resposta ='A Subprefeitura Butantã gastou R$ 36.921.397,88 em serviços públicos ao longo de 2022. O valor corresponde a 92.25% do planejado para o ano, quando o orçamento previsto era de R$ 40.023.094,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/3":
    texto_resposta ='A Subprefeitura Campo Limpo gastou R$ 44.291.072,27 em serviços públicos ao longo de 2022. O valor corresponde a 85.26% do planejado para o ano, quando o orçamento previsto era de R$ 51.949.802,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/4":
    texto_resposta ='A Subprefeitura Capela do Socorro gastou R$ 50.382.105,53 em serviços públicos ao longo de 2022. O valor corresponde a 98.06% do planejado para o ano, quando o orçamento previsto era de R$ 51.377.912,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa..'
  elif message == "/5":
    texto_resposta = 'A Subprefeitura Casa Verde/Cachoeirinha gastou R$ 33.866.963,54 em serviços públicos ao longo de 2022. O valor corresponde a 68.34% do planejado para o ano, quando o orçamento previsto era de R$ 49.559.237,00. Confira mais sobre a região: https://bit.ly/3zayIy5. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa..'
  elif message == "/6":
    texto_resposta = 'A Subprefeitura Cidade Ademar gastou R$ 52.077.759,71 em serviços públicos ao longo de 2022. O valor corresponde a 115.51% do planejado para o ano, quando o orçamento previsto era de R$ 45.085.343,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/7":
    texto_resposta = 'A Subprefeitura Cidade Tiradentes gastou R$ 25.784.337,67 em serviços públicos ao longo de 2022. O valor corresponde a 76.54% do planejado para o ano, quando o orçamento previsto era de R$ 33.685.683,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/8":
    texto_resposta = 'A Subprefeitura de Guaianases gastou R$ 45.959.773,16 em serviços públicos ao longo de 2022. O valor corresponde a 91.63% do planejado para o ano, quando o orçamento previsto era de R$ 50.159.302,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/9":
    texto_resposta = 'A Subprefeitura de Vila Prudente gastou R$ 27.274.641,73 em serviços públicos ao longo de 2022. O valor corresponde a 77.33% do planejado para o ano, quando o orçamento previsto era de R$ 35.268.391,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/10":
    texto_resposta = 'A Subprefeitura Ermelino Matarazzo gastou R$ 30.024.575,42 em serviços públicos ao longo de 2022. O valor corresponde a 95.00% do planejado para o ano, quando o orçamento previsto era de R$ 31.606.121,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/11":
    texto_resposta = 'A Subprefeitura Freguesia/Brasilândia gastou R$ 37.355.664,82 em serviços públicos ao longo de 2022. O valor corresponde a 102.29% do planejado para o ano, quando o orçamento previsto era de R$ 36.520.179,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/12":
    texto_resposta = 'A Subprefeitura Ipiranga gastou R$ 34.993.820,19 em serviços públicos ao longo de 2022. O valor corresponde a 89.45% do planejado para o ano, quando o orçamento previsto era de R$ 39.122.951,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'     
  elif message == "/13":
    texto_resposta = 'A Subprefeitura Itaim Paulista gastou R$ 33.278.381,84 em serviços públicos ao longo de 2022. O valor corresponde a 62.03% do planejado para o ano, quando o orçamento previsto era de R$ 53.647.372,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/14":
    texto_resposta = 'A Subprefeitura Itaquera gastou R$ 39.302.438,70 em serviços públicos ao longo de 2022. O valor corresponde a 81.65% do planejado para o ano, quando o orçamento previsto era de R$ 48.132.695,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/15":
    texto_resposta ='A Subprefeitura Jabaquara gastou R$ 31.578.621,35 em serviços públicos ao longo de 2022. O valor corresponde a 91.42% do planejado para o ano, quando o orçamento previsto era de R$ 34.542.799,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/16":
    texto_resposta = 'A Subprefeitura Jaçanã/Tremembé gastou R$ 39.500.406,95 em serviços públicos ao longo de 2022. O valor corresponde a 106.74% do planejado para o ano, quando o orçamento previsto era de R$ 37.004.697,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/17":
    texto_resposta = 'A Subprefeitura Lapa gastou R$ 37.044.176,24 em serviços públicos ao longo de 2022. O valor corresponde a 80.87% do planejado para o ano, quando o orçamento previsto era de R$ 45.809.043,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/18":
    texto_resposta = "A Subprefeitura M'Boi Mirim gastou R$ 75.591.793,20 em serviços públicos ao longo de 2022. O valor corresponde a 139.87% do planejado para o ano, quando o orçamento previsto era de R$ 54.042.969,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa."
  elif message == "/19":
    texto_resposta ='A Subprefeitura Mooca gastou R$ 45.192.067,02 em serviços públicos ao longo de 2022. O valor corresponde a 105.21% do planejado para o ano, quando o orçamento previsto era de R$ 42.954.814,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/20":
    texto_resposta ='A Subprefeitura Parelheiros gastou R$ 120.585.653,38 em serviços públicos ao longo de 2022. O valor corresponde a 144.64% do planejado para o ano, quando o orçamento previsto era de R$ 83.368.309,00. Confira mais sobre a região: https://bit.ly/3lKBas2. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/21":
    texto_resposta ='A Subprefeitura Penha gastou R$ 46.803.990,78 em serviços públicos ao longo de 2022. O valor corresponde a 115.23% do planejado para o ano, quando o orçamento previsto era de R$ 40.616.502,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/22":
    texto_resposta ='A Subprefeitura Perus/Anhanguera gastou R$ 36.003.708,90 em serviços públicos ao longo de 2022. O valor corresponde a 120.48% do planejado para o ano, quando o orçamento previsto era de R$ 29.883.048,00. Confira mais sobre a região: https://bit.ly/3zayIy5. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/23":
    texto_resposta ='A Subprefeitura Pinheiros gastou R$ 39.657.330,86 em serviços públicos ao longo de 2022. O valor corresponde a 93.18% do planejado para o ano, quando o orçamento previsto era de R$ 42.559.302,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/24":
    texto_resposta ='A Subprefeitura Pirituba/Jaraguá gastou R$ 36.756.827,44 em serviços públicos ao longo de 2022. O valor corresponde a 89.97% do planejado para o ano, quando o orçamento previsto era de R$ 40.854.599,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/25":
    texto_resposta ='A Subprefeitura Santana/Tucuruvi gastou R$ 32.648.015,27 em serviços públicos ao longo de 2022. O valor corresponde a 88.48% do planejado para o ano, quando o orçamento previsto era de R$ 36.898.614,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/26":
    texto_resposta ='A Subprefeitura Santo Amaro gastou R$ 34.411.349,99 em serviços públicos ao longo de 2022. O valor corresponde a 85.62% do planejado para o ano, quando o orçamento previsto era de R$ 40.192.751,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/27":
    texto_resposta = 'A Subprefeitura São Mateus gastou R$ 52.985.212,73 em serviços públicos ao longo de 2022. O valor corresponde a 96.89% do planejado para o ano, quando o orçamento previsto era de R$ 54.683.813,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/28":
    texto_resposta ='A Subprefeitura São Miguel Paulista gastou R$ 45.504.087,19 em serviços públicos ao longo de 2022. O valor corresponde a 96.96% do planejado para o ano, quando o orçamento previsto era de R$ 46.929.108,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/29":
    texto_resposta = "A Subprefeitura Sapopemba gastou R$ 27.852.938,60 em serviços públicos ao longo de 2022. O valor corresponde a 60.70% do planejado para o ano, quando o orçamento previsto era de R$ 45.884.095,00. Confira mais sobre a região aqui: https://bit.ly/40CTfqy. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa."
  elif message == "/30":
    texto_resposta ='A Subprefeitura Sé gastou R$ 104.587.793,67 em serviços públicos ao longo de 2022. O valor corresponde a 98.93% do planejado para o ano, quando o orçamento previsto era de R$ 105.719.708,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/31":
    texto_resposta = 'A Subprefeitura Vila Maria/Vila Guilherme gastou R$ 27.269.037,81 em serviços públicos ao longo de 2022. O valor corresponde a 70.28% do planejado para o ano, quando o orçamento previsto era de R$ 38.799.179,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/32":
    texto_resposta ='A Subprefeitura Vila Mariana gastou R$ 50.278.531,66 em serviços públicos ao longo de 2022. O valor corresponde a 112.90% do planejado para o ano, quando o orçamento previsto era de R$ 44.534.373,00. Se quiser saber de outra região, clique em /d ou em /0 para acessar a reportagem completa.'
  elif message == "/0":
    texto_resposta ='Confira como a maioria das subprefeituras não realizou os serviços que estavam previstos no orçamento: https://bit.ly/3KcAlR1'
  else:
    texto_resposta = "Acho que digitou errado! Clique em /menu para voltar ao começo ou para outras informações sobre a cidade de São Paulo e a região metropolitana, acesse o site da Agência Mural: agenciamural.org.br"
  nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
  requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  #sheet.update("A1", update_id)
  sheet2.append_row([datahora, first_name, chat_id, message])  
  #sheet3.append_rows(mensagens)
  return "ok"

@app.route("/mural")
def mural():
    link = 'https://www.agenciamural.org.br/noticias/'
    requisicao = requests.get(link)
    html = BeautifulSoup(requisicao.content)
    noticias = html.find_all('div', {'class': 'texto mt-1'})
    Publicacoes = []
    for link in noticias:
        Autor_e_Data = link.find('span', {'class': 'detalhes mt-1 d-block'}).text
        Título = link.find('h2', {"class": "m-0 mt-1"}).text
        Linha_Fina = link.find('p', {"class": "linha-fina m-0 mt-1"}).text
        URL = link.find('a').get('href')
        valores = sheet_novo.col_values(4)
        if URL not in valores:
            Publicacoes.append([Autor_e_Data, Título, Linha_Fina, URL])

    df = pd.DataFrame(Publicacoes, columns=['Autor_e_Data', 'Título', 'Linha_Fina', 'URL'])
    sheet_novo.append_rows(Publicacoes)
    
    if len(Publicacoes) > 0:
        return "Novas notícias atualizadas"
    else:
        return "Já atualizamos as últimas notícias"

@app.route("/webstories")
def webstories():
  link='https://www.agenciamural.org.br/noticias/'
  requisicao=requests.get(link)
  html=BeautifulSoup(requisicao.content)
  webstories = html.find_all('div', {'class':'col pb-4 text-center'})
  Publicacoes = []
  for link in webstories:
    URL= link.find("a").get("href")
    Autor = 'Da Redação'
    Titulo='Novo webstory'
    Descricao='Reportagem em formato de webstory da Agência Mural'
    valores = sheet_novo.col_values(4)
    if URL not in valores:
      Publicacoes.append([Autor, Titulo, Descricao, URL])
      df = pd.DataFrame(Publicacoes, columns=['Autor_e_Data', 'Título', 'Linha_Fina', 'URL'])
      sheet_novo.append_rows(Publicacoes)   
      return "Nova notícia atualizada"
    else:
      return "Já atualizamos as últimas notícias"          
  
    
@app.route("/leis")
def coleta():
  try:
    osasco='https://leismunicipais.com.br/legislacao-municipal/5123/leis-de-osasco/?q='
    guarulhos='https://leismunicipais.com.br/legislacao-municipal/4862/leis-de-guarulhos?q='
    sao_bernardo='https://leismunicipais.com.br/legislacao-municipal/5280/leis-de-sao-bernardo-do-campo?q='
    diadema='https://leismunicipais.com.br/legislacao-municipal/4888/leis-de-diadema?q='
    barueri='https://leismunicipais.com.br/legislacao-municipal/4798/leis-de-barueri?q='
    suzano='https://leismunicipais.com.br/legislacao-municipal/5321/leis-de-suzano?q='
    itaquaquecetuba='https://leismunicipais.com.br/legislacao-municipal/5000/leis-de-itaquaquecetuba?q='
    taboao_da_serra='https://leismunicipais.com.br/legislacao-municipal/5324/leis-de-taboao-da-serra?q='
    carapicuiba='https://leismunicipais.com.br/legislacao-municipal/4855/leis-de-carapicuiba?q='
    cotia='https://leismunicipais.com.br/legislacao-municipal/4880/leis-de-cotia?q='
    cidades=[osasco, guarulhos, sao_bernardo, carapicuiba, taboao_da_serra, cotia, itaquaquecetuba, suzano, diadema, barueri]
    leis_cidades=[]
    for cidade in cidades:
      requisicao=requests.get(cidade)
      html=BeautifulSoup(requisicao.content)
      leis = html.find_all('li',{'class':'item item-result index-leismunicipais'})
      Cidade=html.find('title').text
      for law in leis:
        Título = law.find('h3',{'class':'title'}).text.replace("Norma em vigor", "").strip()
        Descrição = law.find('p',{'class':'description'}).text.strip()
        Link = f"https://leismunicipais.com.br{law.find('a').get('href')}"
        leis_cidades.append([Cidade, Título, Descrição, Link])

    df = pd.DataFrame(leis_cidades, columns=['Cidade','Título', 'Descrição', 'Link'])

    valores = sheet_leis.col_values(4)
    novos_links = [link for link in df['Link'] if link not in valores]
    if novos_links:
      novos_dados = df[df['Link'].isin(novos_links)]
      sheet_leis.append_rows(novos_dados.values.tolist())
      return "Leis atualizadas"
    else:
      return "Já atualizamos as últimas leis"
    
  except Exception as e:
    print(f"Erro na coleta: {e}")
    return 'Erro na coleta'
  
@app.route('/bot-diario', methods=["POST"])
def bot_diario():
    leis_ja_enviadas = sheet_leis.col_values(4) # supondo que essa é a coluna com as URLs
    novas_leis = []
    for raspada in leis_ja_enviadas:
        if raspada not in leis_ja_enviadas:
            novas_leis.append(raspadas)
    if novas_leis:
        enviar_mensagem(novas_leis)
        
        message = Mail(
          from_email='paulo@agenciamural.org.br',
          to_emails='paulotbastos@hotmail.com',
          subject='Leis atualizadas',
          html_content=f'Seguem as útimas leis: {novas_leis}'
        )
        sg = SendGridAPIClient(key)
        response = sg.send(message)
      
     return "ok"
        
