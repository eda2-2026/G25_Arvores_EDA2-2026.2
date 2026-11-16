class No:
    def __init__(self, chave):
        self.chave = chave
        
        self.right = None
        self.left = None
        self.pai = None
        
class Arvore:
    def __init__(self):
        self.root = None
        self.no_atual = None
        self.no_prox = None
    
        
    def compara(self, no_atual: No, no_novo:No):
            if(no_atual.chave > no_novo.chave ):
                if(no_atual.left == None):
                    no_novo.pai = no_atual 
                    no_atual.left = no_novo
                    return
                else: 
                    self.compara(no_atual.left, no_novo)
            elif(no_atual.chave <= no_novo.chave ):
                if(no_atual.right == None):
                    no_novo.pai = no_atual
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

    #-------------------------------------------------------
    
    def busca(self, no_atual: No, valor):
                if(no_atual == None):
                    print ("Dado inexistente")
                    return False
                elif(no_atual.chave > valor):
                    if(no_atual.left == None):
                        print ("Dado inexistente")
                        return False
                    else: 
                        return self.busca(no_atual.left, valor)
                elif(no_atual.chave < valor):
                    if(no_atual.right == None):
                        print ("Dado inexistente")
                        return False
                    return self.busca(no_atual.right, valor)
                else:
                    print("Encontrado")
                    return no_atual             
                return None    
    
    def minimo(self, no):
        while no.left != None:
            no = no.left

        return no
    
    def transplantar(self, antigo, novo):

        if antigo.pai == None:
            self.root = novo

        elif antigo == antigo.pai.left:
            antigo.pai.left = novo

        else:
            antigo.pai.right = novo

        if novo != None:
            novo.pai = antigo.pai
    
    def delete(self, valor):

        no = self.busca(self.root, valor)

        if no == False or no == None:
            return False

        # Não possui filho esquerdo
        if no.left == None:
            self.transplantar(no, no.right)

        # Não possui filho direito
        elif no.right == None:
            self.transplantar(no, no.left)

        # Possui dois filhos
        else:

            sucessor = self.minimo(no.right)

            if sucessor.pai != no:

                self.transplantar(sucessor, sucessor.right)

                sucessor.right = no.right
                sucessor.right.pai = sucessor

            self.transplantar(no, sucessor)

            sucessor.left = no.left
            sucessor.left.pai = sucessor

        return True
    
    #---------------------------------------------------------------------------------                            

    def left_rotate(self, node):
        pass

    def right_rotate(self, node):
        pass

    