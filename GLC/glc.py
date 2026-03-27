class AnalisadorExpressão:
    def __init__(self, texto):
        self.entrada = texto.replace(" ", "")
        self.posicao = 0

    def proximo_caratere(self):
        if self.posicao < len(self.entrada):
            return self.entrada[self.posicao]
        else:
            return None
        
    def consumir(self, esperado):
        atual = self.proximo_caratere(self)
        if atual == esperado:
            self.posicao += 1
            return atual
        else:
            return "Erro"
        
    def analisarOp(self):
        op = self.proximo_caratere()
        if op in ['+', '-', '*', '/']:
            return self.consumir(op)
        else:
            return "Erro"
        
    def analisarE(self):
        e = self.proximo_caratere()
        
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