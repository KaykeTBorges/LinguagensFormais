from glc import AnalisadorExpressão

def main():
    entrada = input("Digite a expressão: ")
    analisador = AnalisadorExpressão(entrada)

    try:
        arvore = analisador.rodar()
        print("Estrutura Sintática")
        print(arvore)
    except Exception as e:
        print(f"Falha na análise: {e}")

if __name__ == "__main__":
    main()