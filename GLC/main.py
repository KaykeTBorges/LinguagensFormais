from glc import AnalisadorExpressão

def main():
    entrada = input("Digite a expressão: ")
    analisador = AnalisadorExpressão(entrada)
    resultado = analisador.rodar()

    if resultado != "Erro":
        with open("GLC/saida_sintatica.txt", "w", encoding="utf-8") as arquivo_txt:
            analisador.imprimir_em_arquivo(resultado, arquivo_txt)

        print("Análise concluída! A árvore foi salva em 'saida_sintatica.txt'.")

    else:
        print("Erro de sintaxe na expressão.")

if __name__ == "__main__":
    main()