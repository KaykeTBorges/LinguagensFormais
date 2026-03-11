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
    
def extrair_titulos(html):
    # Padrão para capturar os tópicos do índice da Wikipédia:
    # 1. Procura a classe 'vector-toc-text' como âncora, onde vão estar todos os títulos
    # 2. <span.*?>.*?</span> -> Localiza e ignora o primeiro span (o número da seção)
    # 3. \s* -> remove quebras de linha e espaços extras
    # 4. <span>(.*?)</span> -> Captura apenas o texto dentro do segundo span (o nome do tópico)
    # o que foi digitado dentro do parênteses é o que ele vai pegar e retornar como o padrão
    padrao_titulos = r'class="vector-toc-text".*?<span.*?>.*?</span>\s*<span>(.*?)</span>'

    # O re.DOTALL é fundamental para ignorar as quebras de linha
    titulos = re.findall(padrao_titulos, html, re.DOTALL)

    print("\nTITULOS DO ARTIGO WIKI")
    for t in titulos:
        print(f"- {t}")

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
