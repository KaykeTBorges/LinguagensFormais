from scraper import *

while(True):
        link = input("Digite o link do artigo do wikipedia: ")
        if validar_url(link):
            print("URL válido e checado!")
            break
        else:
            print("URL inválida")

html = requisicao(link)

extrair_topicos(html)

extrair_links(html)

extrair_imagens(html)

print("Tudo salvo nos seus respectivos arquivos!")

