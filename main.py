from scraper import *

while(True):
        link = input("Digite o link do artigo do wikipedia: ")
        if validar_url(link):
            print("URL válido e checado!")
            break
        else:
            print("URL inválida")

html = requisicao(link)

extrair_titulos(html)

extrair_links(html)

extrair_imagens(html)

