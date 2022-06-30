import threading
import numpy as np
import pygame as pg
import sys, time



class Ambiente():
    def __init__(self):
        
        self.locais = np.loadtxt("localizações.txt")
        self.ambiente = np.loadtxt("ambiente.txt")
        self.custos = np.zeros((42,42))
        self.itens = [20,10,8,6,4]
        
        #cores 
        self.green = 25
        self.blue = 2
        self.orange = 80
        self.brown = 40

        for i in range(42):
            for j in range(42):
                #print("oi")
                if self.ambiente[i,j] == 1:
                    self.ambiente[i,j] = 40 #self.brown
                    self.custos[i,j] = 5
                elif self.ambiente[i,j] == 2:
                    self.ambiente[i,j] = 2 #self.blue
                    self.custos[i,j] = 10
                elif self.ambiente[i,j] == 3:
                    self.ambiente[i,j] =  80 #self.orange
                    self.custos[i,j] = 15 
                elif self.ambiente[i,j] == 0:
                    self.ambiente[i,j] = 25 #self.green  
                    self.custos[i,j] = 1
                elif self.ambiente[i,j] == 2000:
                    self.ambiente[i,j] = 0  #preto, obstáculo
                    self.custos[i,j] = 2000  

        self.ambiente[int(self.locais[1,0]), int(self.locais[1,1]) ] = 0#110 #fábrica 1
        self.ambiente[int(self.locais[2,0]), int(self.locais[2,1]) ] = 0#120 #fábrica 2
        self.ambiente[int(self.locais[3,0]), int(self.locais[3,1]) ] = 0#330 #fábrica 3
        self.ambiente[int(self.locais[4,0]), int(self.locais[4,1]) ] = 0#140 #fábrica 4   

        for item in self.itens:
            i=0
            while i < item:
                x = np.random.randint(0,42)
                y = np.random.randint(0,42)
                if self.ambiente[x,y] == 25:
                    self.ambiente[x,y] = item
                    i=i+1

class Robo():
    def __init__(self,raio, grid,coord,custos):
        self.grid = grid #ambiente
        self.raio = raio   
        self.r_ = 9#self._calc_r_()
        self.coord_atual = [coord[0],coord[1]]
        self.custos = custos

        self.baterias = 0
        self.solda = 0
        self.sucçao = 0 
        self.refri = 0
        self.pneu = 0

        self.last_coord = [self.coord_atual[0],self.coord_atual[1]] #[x,y]
        self.last_color = self.grid[self.last_coord[0],self.last_coord[1]] #25
        
        self.grid[self.coord_atual[0],self.coord_atual[1]] = 1000 #robo
        
    def neighbors(self,radius, row_number, column_number):
        a = self.grid
        return [[a[i][j] if  i >= 0 and i < len(a) and j >= 0 and j < len(a[0]) else 0
                for j in range(column_number-1-radius, column_number+radius)]
                    for i in range(row_number-1-radius, row_number+radius)]

    def vizinhos(self, vet, x,y):
        n = self.r_
        #print(n)
        vet = np.roll(np.roll(vet, shift=-x+1, axis=0), shift=-y+1, axis=1)

        #print('\n', (vet[:n,:n]))
        return vet[:9,:9]

    def run(self):
        self.andar()
        return self.grid
    
    def andar(self):
        grid = self.grid
        
        
        #vet = self.vizinhos(self.grid, self.coord_atual[0],self.coord_atual[1])
        #print(vet)
        
        
        #print(self.neighbors(1,self.coord_atual[0],self.coord_atual[1]))
        self.grid[self.coord_atual[0],self.coord_atual[1]] = self.last_color #volta a cor originial
        
        vet = (self.neighbors(4,self.coord_atual[0],self.coord_atual[1]))
        for a in vet:
            for i in a:
                if ((i == 20) or (i==10)  or (i==8 ) or (i==6) or (i==4)):
                    print("oi")
        #tres células de deslocamento se era o [5,5], passou a ser o [2,2]
        self.coord_atual[0] = self.coord_atual[0]+1
        self.coord_atual[1] = self.coord_atual[1]
               
        self.last_color = self.grid[self.coord_atual[0],self.coord_atual[1]]

        if (self.is_item(grid[self.coord_atual[0],self.coord_atual[1]])):
            self.last_color = 25

        self.grid[self.coord_atual[0],self.coord_atual[1]] = 1000 #muda robo de lugar
      
        #print(self.custos[self.coord_atual[0],self.coord_atual[1]])
        
        return 

    def a_star(self):
        pass
        
    def is_item(self, item):
        if (item==20):
            self.baterias=self.baterias+1
            print("pegou bateria - total:", self.baterias)
            return True
        if (item==10): 
            self.solda=self.solda+1
            print("pegou solda - total:", self.solda)
            return True
        if (item==8):
            self.sucçao=self.sucçao+1
            print("pegou sucçao - total:", self.sucçao)
            return True
        if (item==6): 
            self.refri=self.refri+1
            print("pegou refri - total:", self.refri)
            return True
        if (item==4):
            self.pneu=self.pneu+1
            print("pegou pneu - total:", self.pneu)
            return True
            

    def pegar(self):
        pass

    def _calc_r_(self):
        self.r_ = 1
        for i in range(self.raio):
            self.r_ = self.r_ + 2

 
class Acao():
    def __init__(self,raio,ambiente,coord,custos,sleep):
        self.size = 42
        self.raio = raio
        self.ambiente = ambiente
        self.coord = [int(coord[0,0]),int(coord[0,1])]
        self.custos = custos
        self.sleep = sleep
        self.pecas = [20,10,8,6,4] #peças
        self.lista = list()

        #print(self.ambiente)

        #self.distribui(self.ambiente, self.pecas)
        self.cria_robo(self.raio, self.ambiente,self.coord,self.custos)

       
    
    def distribui(self, ambiente, pecas):
        #solta as peças no ambiente
        pass

    def cria_robo(self,raio,ambiente,coord,custos):
        robo = Robo(raio, ambiente,coord,custos)
        self.lista.append(robo)
    
    def inicio(self):
        #time.sleep(self.sleep)
        for robo in self.lista:
            for i in range (0,10):
                self.ambiente = robo.run()                   
                self.run()

    def matriz(self):
        ret = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                ret[i,j] = self.ambiente[i,j]
        #print(ret)
        return ret
              

    def run(self):
            time.sleep(0.5) 
            pg.init()
            tela = pg.display.set_mode((900, 900))
            tela.set_alpha(None)
            #print(np.count_nonzero(self.grid != None))
            #t = threading.Thread(target=self.inicio)
            #t.daemon=True
            #t.start()

            #while True:
            for e in pg.event.get():
                if e.type == pg.QUIT: sys.exit()
            vetor = self.matriz() #self.matriz()
            superficie = pg.surfarray.make_surface(vetor)
            new_superficie = pg.transform.scale(superficie, (900,900))
                
            new_superficie = pg.transform.flip(new_superficie, True, False)  
            new_superficie = pg.transform.rotate(new_superficie,90)
                
            tela.blit(new_superficie, (0,0))
            pg.display.flip()

if __name__ == "__main__":
    ambiente = Ambiente()
    start = Acao(raio=4,ambiente=ambiente.ambiente,coord=ambiente.locais,custos=ambiente.custos,sleep=1)
    start.inicio()
    