
class No:
    RED = 'RED'
    BLACK = 'BLACK'
    
    def __init__(self, key, nome, time):
        self.key = key #key é quantidade de gols e id respectivamente
        self.nome = nome
        self.time = time

        
        
        self.cor = No.RED
        
        self.left = None
        self.right = None
        self.parent = None
        
jogador = No(key=(-30,1), nome='Neymar', time="Santos")
jogador2 = No(key=(-15,2), nome='Pedro', time="Flamengo")
jogador2.parent = jogador
jogador3 = No(key=(-25,3), nome='Tiquinho', time="Botafogo")
jogador3.parent = jogador


class ArvoreRedBlack:
    def __init__(self):
        self.root = None
        
    def insert(self, no : No):
        if self.root == None:
            self.root = no
        elif self.root.key[0] < no.key[0]:
            self.root.right = no
            
        else: self.root.left = no
        
    
    def delete(self, key):
        pass

    def search(self, key):
        pass

    def left_rotate(self, node):
        pass

    def right_rotate(self, node):
        pass

    def fix_insert(self, node):
        pass

    def fix_delete(self, node):
        pass        
                

    
    


        