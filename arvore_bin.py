class No:
    def __init__(self, chave):
        self.chave = chave
        
        self.right = None
        self.left = None
        
class Arvore:
    def __init__(self):
        self.root = None
        self.no_atual = None
        self.no_prox = None
    
        
    def compara(self, no_atual: No, no_novo:No):
            if(no_atual.chave > no_novo.chave ):
                if(no_atual.left == None):
                    no_atual.left = no_novo
                    return
                else: 
                    self.compara(no_atual.left, no_novo)
            elif(no_atual.chave <= no_novo.chave ):
                if(no_atual.right == None):
                    no_atual.right = no_novo
                    return
                self.compara(no_atual.right, no_novo)          
            return          
        
    def insert(self, no : No):
        if(self.root == None ):
            self.root = no
            return
        else:
            self.compara(self.root, no)
        return    
        
arvore = Arvore()

for valor in [30, 20, 40, 10, 25, 35, 50]:
    arvore.insert(No(valor))            
    
print(arvore.root.chave)
print(arvore.root.right.chave)
print(arvore.root.left.chave)
print(arvore.root.left.left.chave)
print(arvore.root.left.right.chave)
    