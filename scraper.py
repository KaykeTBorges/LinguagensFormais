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
    
def requisicao(url):
    requisicao = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
    )

    with urllib.request.urlopen(requisicao) as resposta:
            html_conteudo = resposta.read().decode('utf-8')
    return html_conteudo
    
# Captura de TITULO
def extrair_topicos(html):
    # Padrão para capturar os tópicos do índice da Wikipédia:
    # 1. Procura a classe 'vector-toc-text' como âncora, onde vão estar todos os títulos
    # 2. <span.*?>.*?</span> -> Localiza e ignora o primeiro span (o número da seção)
    # 3. \s* -> remove quebras de linha e espaços extras
    # 4. <span>(.*?)</span> -> Captura apenas o texto dentro do segundo span (o nome do tópico)
    # o que foi digitado dentro do parênteses é o que ele vai pegar e retornar como o padrão
    padrao_topicos = r'class="vector-toc-text".*?<span.*?>.*?</span>\s*<span>(.*?)</span>'

    # O re.DOTALL é fundamental para ignorar as quebras de linha
    topicos = re.findall(padrao_topicos, html, re.DOTALL)

    print("\nTÓPICOS DO ARTIGO WIKI")
    for t in topicos:
        print(f"- {t}")

# Captura de LINKS
def extrair_links(html):
    # os links se encontram em href
    # href="/wiki/[^":?#]+" -> Garante que o link é para um artigo (sem imagens ou seções)
    # .*? -> Pula qualquer atributo extra no meio
    # title="([^"]+)" -> Grupo de captura: pega o nome limpo/acentuado da página

    padrao_links = r'href="/wiki/[^":?#]+".*?title="([^"]+)"'
    links = re.findall(padrao_links, html)

    # Tudo o que for interface ou página de sistema entra aqui
    lista_negra = [
        "Editar", "Ver a página", "Ajuda", "Wikimedia", 
        "Categoria", "Ficheiro", "Especial"
    ]
    
    # limpeza filtra mantendo apenas o que não contém os termos da lista negra
    links_limpo = []
    for l in links:
        # Se nenhuma palavra da lista negra estiver no título, adiciona
        if not any(termo in l for termo in lista_negra):
            links_limpo.append(l)

    links = sorted(set(links_limpo))

    print("\nLINKS DO ARTIGO WIKI")
    for l in links_limpo:
        print(f"- {l}")

# CAPTURA DE NOMES DE IMAGENS
def extrair_imagens(html):
    # Padrão de captura de imagens:
    # 1. src= procura pontos no HTML onde estão os links (src = source).
    # 2. ((?:https:)? permite que o protocolo seja capturado ou não
    # 3. //upload\.wikimedia\.org/ captura apenas imagens hospedadas nos servidores Wikipedia.
    # 4. [^"]+ captura qualquer caractere até encontra aspas duplas EXCETO as próprias aspas duplas.
    # 5. \. (?:jpg|jpeg|png|gif|svg) garante que o padrão termine com uma extensão de arquivo do tipo imagem, 
    # podendo ser JPG, JPEG, PNG, GIF e SVG.
    padrao_imagens = r'src="((?:https:)?//upload\.wikimedia\.org/[^"]+\.(?:jpg|jpeg|png|gif|svg))"'

    links_imagens = re.findall(padrao_imagens, html)

    
    nomes_imagens= []
    for img in links_imagens:
        nome = img.split('/')[-1] # pega apenas a ultima parte do link
        nome = unquote(nome) # traduz simbolos especiais de URLs para a lingua natural.
        nome = re.sub(r'^\d+px-', '', nome) # tira (se houver) o prefixo de tamanho, comum em imagens hospedadas na Wikipédia
        nomes_imagens.append(nome) # guarda apenas o nome da imagem na lista

    print("IMAGENS DO ARTIGO WIKI")
    for img in nomes_imagens:
        print(f"NOME DA IMAGEM:- {img}\nLINK: {links_imagens[nomes_imagens.index(img)]}")
