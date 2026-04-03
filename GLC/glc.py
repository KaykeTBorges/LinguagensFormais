class AnalisadorExpressão:
    def __init__(self, texto):
        self.entrada = texto.replace(" ", "")
        self.posicao = 0

    def atual_caractere(self):
        if self.posicao < len(self.entrada):
            return self.entrada[self.posicao]
        else:
            return None
        
    def consumir(self, esperado):
        atual = self.atual_caractere()
        if atual == esperado:
            self.posicao += 1
            return atual
        else:
            return "Erro"
        
    def analisarOp(self):
        op = self.atual_caractere()
        if op in ['+', '-', '*', '/']:
            return self.consumir(op)
        else:
            return "Erro"
        
    def analisarE(self):
        e = self.atual_caractere()
        
        if e == 'a':
            return self.consumir('a')
        
        elif e == '(':
            p_dir = self.consumir('(')

            e1 = self.analisarE()
            op = self.analisarOp()
            e2 = self.analisarE()

            p_esq = self.consumir(')')

            return [p_dir, e1, op, e2, p_esq]
        
        else:
            return "Erro"
        
    def rodar(self):
        resultado = self.analisarE()

        if self.posicao < len(self.entrada):
            return "Erro"
        
        return resultado
    
    def imprimir_em_arquivo(self, no, arquivo, nivel=0):
        indentacao = "    " * nivel
        if isinstance(no, list):
            arquivo.write(f"{indentacao}Nó (E -> (E Op E)):\n")
            for filho in no:
                self.imprimir_em_arquivo(filho, arquivo, nivel + 1)
        else:
            # Escreve os terminais: a, +, -, *, /, (, )
            arquivo.write(f"{indentacao}Terminal: {no}\n")