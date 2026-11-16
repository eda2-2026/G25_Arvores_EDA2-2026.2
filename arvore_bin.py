class No:
    def __init__(self, jogador, gols):
        self.jogador = jogador
        self.gols = gols

        self.right = None
        self.left = None
        self.pai = None
        
class Arvore:
    def __init__(self):
        self.root = None
        self.no_atual = None
        self.no_prox = None
    
        
    def compara(self, no_atual: No, no_novo:No):
            if(no_atual.gols > no_novo.gols ):
                if(no_atual.left == None):
                    no_novo.pai = no_atual 
                    no_atual.left = no_novo
                    return
                else: 
                    self.compara(no_atual.left, no_novo)
            elif(no_atual.gols <= no_novo.gols ):
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
                elif(no_atual.gols > valor):
                    if(no_atual.left == None):
                        print ("Dado inexistente")
                        return False
                    else: 
                        return self.busca(no_atual.left, valor)
                elif(no_atual.gols < valor):
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

        self.remover_no(no)
        return True

    def remover_no(self, no):

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

    def buscar_jogador(self, no_atual, nome):
        if no_atual == None:
            return None
        if no_atual.jogador == nome:
            return no_atual

        achou = self.buscar_jogador(no_atual.left, nome)
        if achou != None:
            return achou
        return self.buscar_jogador(no_atual.right, nome)

    def remover_jogador(self, nome):
        no = self.buscar_jogador(self.root, nome)
        if no == None:
            return False
        self.remover_no(no)
        return True

    def para_dict(self):
        return self._no_para_dict(self.root)

    def _no_para_dict(self, no):
        if no == None:
            return None
        return {
            "jogador": no.jogador,
            "gols": no.gols,
            "left": self._no_para_dict(no.left),
            "right": self._no_para_dict(no.right),
        }
    
    #---------------------------------------------------------------------------------                            

    def left_rotate(self, node):
        # y sobe e node vira filho esquerdo de y
        y = node.right

        if y == None:
            return False

        node.right = y.left

        if y.left != None:
            y.left.pai = node

        y.pai = node.pai

        if node.pai == None:
            self.root = y
        elif node == node.pai.left:
            node.pai.left = y
        else:
            node.pai.right = y

        y.left = node
        node.pai = y
        return True

    def right_rotate(self, node):
        # x sobe e node vira filho direito de x
        x = node.left

        if x == None:
            return False

        node.left = x.right

        if x.right != None:
            x.right.pai = node

        x.pai = node.pai

        if node.pai == None:
            self.root = x
        elif node == node.pai.right:
            node.pai.right = x
        else:
            node.pai.left = x

        x.right = node
        node.pai = x
        return True

    
