import re
import urllib.request
from urllib.parse import unquote

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


# CAPTURA DE NOMES DE IMAGENS

# Padrão de captura de imagens:
# 1. src= procura pontos no HTML onde estão os links (src = source).
# 2. ((?:https:)? permite que o protocolo seja capturado ou não
# 3. //upload\.wikimedia\.org/ captura apenas imagens hospedadas nos servidores Wikipedia.
# 4. [^"]+ captura qualquer caractere até encontra aspas duplas EXCETO as próprias aspas duplas.
# 5. \. (?:jpg|jpeg|png|gif|svg) garante que o padrão termine com uma extensão de arquivo do tipo imagem, podendo ser JPG, JPEG, PNG, GIF e SVG.
padrao_imagens = r'src="((?:https:)?//upload\.wikimedia\.org/[^"]+\.(?:jpg|jpeg|png|gif|svg))"'

links_imagens = re.findall(padrao_imagens, html_conteudo)

 
nomes_imagens= []
for img in links_imagens:
    nome = img.split('/')[-1] # pega apenas a ultima parte do link
    nome = unquote(nome) # traduz simbolos especiais de URLs para a lingua natural.
    nome = re.sub(r'^\d+px-', '', nome) # tira (se houver) o prefixo de tamanho, comum em imagens hospedadas na Wikipédia
    nomes_imagens.append(nome) # guarda apenas o nome da imagem na lista

print("----------------- NOME DAS IMAGENS -------------------")
for img in nomes_imagens:
    print(f"- {img}")