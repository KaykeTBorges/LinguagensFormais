import re
import urllib.request

def validar_url(url):
    padrao = r"^https://pt\.wikipedia\.org/wiki/.*"
    # o \. tira o superpoder do dot, que é aceitar qualquer tipo de caracter
    # o asterisco seria mais ou menos o fecho de Kleene
    if re.match(padrao, url):
        return True
    else:
        return False

while(True):
    link = input("Digite o link do artigo do wikipedia: ")
    if validar_url(link):
        print("URL válido e checado!")
        break
    else:
        print("URL inválida")

requisicao = urllib.request.Request(
    link, 
    headers={'User-Agent': 'Mozilla/5.0'}
)

with urllib.request.urlopen(requisicao) as resposta:
    html_conteudo = resposta.read().decode('utf-8')

print("html baixado com sucesso")

# Padrão para capturar os tópicos do índice da Wikipédia:
# 1. Procura a classe 'vector-toc-text' como âncora, onde vão estar todos os títulos
# 2. <span.*?>.*?</span> : Localiza e ignora o primeiro span (o número da seção)
# 3. \s* : remove quebras de linha e espaços extras
# 4. <span>(.*?)</span> : Captura apenas o texto dentro do segundo span (o nome do tópico)
# o que foi digitado dentro do parênteses é o que ele vai pegar e retornar como o padrão
padrao_limpo = r'class="vector-toc-text".*?<span.*?>.*?</span>\s*<span>(.*?)</span>'

# O re.DOTALL é fundamental para ignorar as quebras de linha
topicos = re.findall(padrao_limpo, html_conteudo, re.DOTALL)

for t in topicos:
    print(f"- {t}")