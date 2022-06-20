   
import threading
from matplotlib.pyplot import grid
import numpy as np
import time
import pygame as pg
import sys
from scipy.spatial.distance import euclidean
import math

class Dados():
    def __init__(self):
        self.locais = np.loadtxt("localizações.txt")
        self.ambiente = np.loadtxt("ambiente.txt")

        for i in range(42):
            for j in range(42):
                #print("oi")
                if self.ambiente[i,j] == 1:
                    self.ambiente[i,j] = 40 #self.brown
                elif self.ambiente[i,j] == 2:
                    self.ambiente[i,j] = 2 #self.blue
                elif self.ambiente[i,j] == 3:
                    self.ambiente[i,j] =  80 #self.orange 
                elif self.ambiente[i,j] == 0:
                    self.ambiente[i,j] = 25 #self.green      

        self.ambiente[int(self.locais[1,0]), int(self.locais[1,1]) ] = 110 #fábrica 1
        self.ambiente[int(self.locais[2,0]), int(self.locais[2,1]) ] = 120 #fábrica 2
        self.ambiente[int(self.locais[3,0]), int(self.locais[3,1]) ] = 330 #fábrica 3
        self.ambiente[int(self.locais[4,0]), int(self.locais[4,1]) ] = 140 #fábrica 4  
        

class Formiga():
    def __init__(self, x,y,raio_visao, grid,its):
        self.grid = grid
        self.raio_visao = raio_visao
        self.x = x
        self.y = y
        self.itera = its
        
        self.carregando = False
        self.data = None
        
        self.max_step_size  = self.grid.shape[0]//2 +1 #int((20*n_dados)**0.5)


    def posicao(self):
        #print("passo",self.max_step_size, self.grid.shape[0])
        tam_passo = np.random.randint(1, self.max_step_size)
        tam_grid = self.grid.shape[0]
        x = self.x + np.random.randint(-1 * tam_passo, 1*tam_passo+1) #np.random.randint(-1,2)
        y = self.y + np.random.randint(-1 * tam_passo, 1*tam_passo+1) #np.random.randint(-1,2)

        #print(x,y)
        if x < 0: x = tam_grid + x# x=0 #x+1 #if x < 0: 
        if x >= tam_grid: x = x - tam_grid#if x >= tam_grid: x=(tam_grid-1) #x-1 
        if y < 0: y = tam_grid + y#if y < 0: y=0 #y+1 
        if y >= tam_grid: y = y - tam_grid#if y >= tam_grid: y=(tam_grid-1) #y-1 
                   
        return x,y
    
    def vizinhos(self, vet, x,y, n=3):
        #print(vet)
        vet = np.roll(np.roll(vet, shift=-x+1, axis=0), shift=-y+1, axis=1)

        #print(vet[:n,:n])
        return vet[:n,:n]
    
    def media(self, som_dist):
        soma = 0
        if self.carregando:
            centro = self.data[0:-1]
        else:
            centro = self.grid[self.x, self.y][0:-1]
        
        for i in range(som_dist.shape[0]):
            for j in range(som_dist.shape[0]):
                conta = 0
                if som_dist[i,j] != None:
                    conta = 1 - (euclidean(centro, som_dist[i,j][0:-1]))/((self.alpha))
                soma += conta
        fi = soma/(self.r_**2)
        if fi > 0: return fi
        else: return 0
        
        
    ''' Normalizes the _avg_similarity function '''
    def _sigmoid(self, c, x):
        return ((1-np.exp(-(c*x)))/(1+np.exp(-(c*x))))
    
    def pegar(self):
        som_dist = self.vizinhos(self.grid, self.x, self.y, self.r_ )

        f = (self.media(som_dist))
        #print("f do pegar= ",f)  
        
        sig = self._sigmoid(self.raio_visao*10,f)
        probP = 1 - sig
  

        if ((probP)  >= (np.random.uniform(0.0, 1.0))):            
            self.carregando = True
            self.data = self.grid[self.x, self.y]
            self.grid[self.x, self.y] = None
            return True
        return False

    def largar(self):
        som_dist = self.vizinhos(self.grid, self.x, self.y, self.r_ )
        #print("f do largar= ",f)  
        f = (self.media(som_dist))
        probL = self._sigmoid(self.raio_visao*10, f)
        

        if (probL >= (np.random.uniform(0.0, 1.0))):            
            self.carregando = False
            self.grid[self.x, self.y] = self.data
            self.data = None
            return True
        return False
           
    def run(self):
        self.andar()
        if self.itera <=0 and self.carregando:
            while self.carregando:
                self.andar()
    
    def andar(self):
        grid = self.grid
        x,y = self.x, self.y
        
        if grid[x,y] == None:
            if self.carregando:
                self.largar()
        elif grid[x,y] != None:
            if not self.carregando:
                self.pegar()

        self.x, self.y = self.posicao()
        self.itera -= 1


    def get_carregando(self):
        return self.carregando




        

class AntProgram():
    def __init__(self, grid, dados, raio_visao, num, itr, tam,sleep=0):
        self.size = int(grid)
        self.raio_visao = raio_visao
        self.num = num
        self.itr = itr
        self.tam = tam
        self.dados = dados
        
        self.lista = list()
        self.sleep = sleep

        self.grid = np.empty((self.size, self.size), dtype=np.object_)
        self.distribui(self.grid, self.dados)
     
        
        self.cria_formigas(1, self.raio_visao, self.grid, self.itr // self.num)
    

    def distribui(self,grid,dados):
        grid = self.dados
        # for a in dados:
        #     i = np.random.randint(0, self.size)
        #     j = np.random.randint(0, self.size)
        #     while grid[i,j] != None:
        #         i = np.random.randint(0, self.size)
        #         j = np.random.randint(0, self.size)
        #     grid[i,j] = a
        #print(self.grid)

      

    def cria_formigas(self, num, raio_visao, grid, its):
        for i in range(num):
            x = np.random.randint(0,self.size-1)
            y = np.random.randint(0,self.size-1)
            formiga = Formiga(x,y,raio_visao, grid,its)
            self.lista.append(formiga)

    def inicio(self):
        time.sleep(self.sleep)
        for i in range(self.itr // self.num):
            for formiga in self.lista:
                formiga.run()
        l = list()
        for formiga in self.lista:
            l.append(formiga.get_carregando())
        print(l)

    def matriz(self):
        ret = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                #print("oi")
                if self.grid[i,j] != None:
                    #print("oi")
                    data = self.grid[i,j]
                    ret[i,j] = data[-1] #50 #cor dos dados
                else:
                    ret[i,j] = self.grid[i,j]
        return ret
        

    def run(self):
        pg.init()
        tela = pg.display.set_mode((self.tam, self.tam))
        tela.set_alpha(None)
        #print(np.count_nonzero(self.grid != None))
        t = threading.Thread(target=self.inicio)
        t.daemon=True
        t.start()

        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT: sys.exit()
            vetor = self.matriz()
            formigueiro = pg.surfarray.make_surface(vetor)
            n_formigueiro = pg.transform.scale(formigueiro, (self.tam, self.tam))
            tela.blit(n_formigueiro, (0,0))
            pg.display.flip()


if __name__ == "__main__":
    dados = Dados()
    
    program = AntProgram(grid=42, dados=dados.ambiente, raio_visao=4, num=20, itr=5*10**6, tam=900,sleep=2)
    program.run()


