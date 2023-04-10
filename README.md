# site-teste
Este repositório traz alguns projetos inspirados no Master em Jornalismo de Dados do Insper. 
Aqui teremos:
- Bot do telegram que responde sobre o orçamento da prefeitura de São Paulo por região;
- Um raspador de notícias de um site que arquiva as últimas atualizações em um planilha;
- Criador de um banco de dados sobre leis sancionadas na Grande São Paulo. 

**1) Orçamendômetro (Bot do Telegram) para Agência Mural**
Este robô foi criado para a disciplina de Algoritmos da Automação. Trata-se de um reposítório baseado em uma apuração sobre cada uma das subprefeituras, feito com uma apuração que raspou os dados da execução orçamentária da prefeitura e separou quanto foi gasto em cada região. 

Inicialmente, quem acessa o robô pode ter acesso a quatro opções: 
/a) A subprefeitura que mais gastou do que estava previsto
/b) A subprefeitura que gastou menos do que estava previsto
/c) A região da cidade que teve o menor gasto por habitante
/d) Quero saber de todas as regiões.

Os usuários que acessam a quarta opção, recebem a opção de acessar todas as 32 regiões ou uma reportagem completa sobre o tema. 
Também separamos uma opção, para quem clicar na reportagem completa, de acessar outras informações sobre o site da Agência Mural, veículo que publicou a história, como cadastrar o email para a newsletter. 

As respostas do menu foram baseadas em textos criados automaticamente, após a apuração anterior feita na base de dados da prefeitura. 

O objetivo do robô é disponibilizar informações com base na região de cada usuário, bem como receber dados sobre as regiões de maior interesse e também para fidelizar os usuários apresentando a Agência Mural. 
Também se trata de um experimento de apresentar uma notícia num formato distinto do convencional. 

**2) Raspador Mural**
Este código foi desenvolvido para raspar as últimas notícias da Agência Mural e assim automatizar uma planilha com as últimas informações do que foi publicado. 
Esse trabalho foi dividido em duas partes: Mural e Webstories, pois os webs apresentavam um código distinto na página. 

**3) Observatório de Leis da Grande SP**
Este trabalho foi desenvolvimento para o PROJETO EXPERIMENTAL do curso. Trata-se de unificar um banco de dados que traga as últimas leis sancionadas na Grande São Paulo nas principais cidades. 
O objetivo é servir de ferramenta para repórteres acompanharem quando as leis mais recentes publicadas e servir como base para pautas. 




