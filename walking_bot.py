# -*- coding: utf-8 -*-  
from cProfile import run
import threading
#from matplotlib.pyplot import grid
import numpy as np
import time
import pygame as pg
import sys
from scipy.spatial.distance import euclidean
import math

''''''
class Ambiente():
    def __init__(self, diretorio, diretorio2):
        self.dados = np.loadtxt(diretorio) #leitura do ambiente
        self.locais = np.loadtxt(diretorio2) #leitura das posições das fábricas e robô  
        
        self.itens = [20,10,8,6,4] #itens
        
        a, b = int(self.locais[0,0]), int(self.locais[0,1]) #robo
        
        self.dados [a,b] = 1000 #robo
        self.dados [int(self.locais[1,0]), int(self.locais[1,1]) ] = 110 #fábrica 1
        self.dados [int(self.locais[2,0]), int(self.locais[2,1]) ] = 120 #fábrica 2
        self.dados [int(self.locais[3,0]), int(self.locais[3,1]) ] = 230 #fábrica 3
        self.dados [int(self.locais[4,0]), int(self.locais[4,1]) ] = 140 #fábrica 4
        
        
        for i in range (len(self.itens)):
            j=0
            while j < self.itens[i]:
                a = np.random.randint(0,high=42)
                b = np.random.randint(0,high=42)
                if (self.dados[a,b] == 0):
                    self.dados[a,b] = self.itens[i]*25
                    j=j+1	

        #se pegar, colocar custo 1(verde) 
	#criar classe robô
	#fazer o raio
	#fazer inicio da movimentação

class Robo():
    def __init__(self,grid,coordenadas):
        self.raio = 4
        self.coordenadas = coordenadas
        self.grid = grid
        self.x = 0
        self.y = 0
        
        self.bracos = 0
        self.baterias = 0
        self.bombas = 0
        self.refrigeracao = 0
        self.solda = 0

    
    def andar(self):
        #grid = self.grid
        x = self.x + np.random.randint(-1,2) #np.random.randint(-1,2)
        y = self.y + np.random.randint(-1,2) #np.random.randint(-1,2)
        return x,y
        #x,y = self.x, self.y
        
        #if grid[x,y] == None:
         #   if self.carregando:
          #      self.largar()
        #elif grid[x,y] != None:
         #   if not self.carregando:
          #      self.pegar()

        #self.x, self.y = self.posicao()
        #self.itera -= 1
        #print(self.itera)
    	
    def run(self):
    	return self.andar()

    def calculos():
        pass

    def pegar():
        pass

    def largar():
        pass


        

class Formiga():
    def __init__(self, x,y,raio_visao, grid,its,alpha, n_dados):
        self.grid = grid
        self.raio_visao = raio_visao
        self.x = x
        self.y = y
        self.itera = its
        self._calc_r_()
        self.carregando = False
        self.data = None
        #self.c              = self.raio_visao*10
        self.max_step_size  = self.grid.shape[0]//2 +1 #int((20*n_dados)**0.5)
        #print(self.max_step_size)
        self.alpha = alpha

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
        #print(self.itera)

    

    def get_carregando(self):
        return self.carregando




        

class AntProgram():
    def __init__(self, ambiente, locais):
        self.size = 42
        self.ambiente = ambiente
        self.locais = locais
        #print(self.locais)
        self.tam = 900
        self.cria_robo()
          

    def cria_robo(self):
    	robo = Robo(self.ambiente, self.locais)
    	x,y = robo.run()
    	self.ambiente[x,y] = 1000
    	self.run()
         #for i in range():
         #    x = np.random.randint(0,self.size-1)
         #    y = np.random.randint(0,self.size-1)
             
             #self.lista.append(formiga)

    def inicio(self):
        time.sleep(1)
        
        # for i in range(self.itr // self.num):
        #     for formiga in self.lista:
        #         formiga.run()
        # l = list()
        # for formiga in self.lista:
        #     l.append(formiga.get_carregando())
        # print(l)

    def matriz(self):
        ret = np.zeros((self.size, self.size))
        #a, b = int(self.locais[0,0]), int(self.locais[0,1]) #robo
        
        #faz a coloração do ambiente
        for i in range(self.size):
            for j in range(self.size):
                #print("oi")
                if self.ambiente[i,j] == 1:
                    #data = self.grid[i,j]
                    ret[i,j] = 40#self.brown
                elif self.ambiente[i,j] == 2:
                    ret[i,j] = 2#self.blue
                elif self.ambiente[i,j] == 3:
                    ret[i,j] =  80#self.orange 
                elif self.ambiente[i,j] == 0:
                    ret[i,j] = 25#self.green                   
                else:
                    ret[i,j] = self.ambiente[i,j]                                     
        
        
        return ret
        

    def run(self):
        pg.init()
        tela = pg.display.set_mode((900, 900))
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
            
            n_formigueiro = pg.transform.flip(n_formigueiro, True, False)  
            n_formigueiro = pg.transform.rotate(n_formigueiro,90)
            
            tela.blit(n_formigueiro, (0,0))
            pg.display.flip()


if __name__ == "__main__":
    dados = Ambiente('ambiente.txt', 'localizações.txt')
    AntProgram(ambiente=dados.dados, locais=dados.locais)
   
    #program = AntProgram(grid=(math.sqrt(10*dados.qntd_dados)), qntd_dados=dados.qntd_dados, dados=dados.dados_labels, alpha=dados.alpha, raio_visao=1, num=20, itr=5*10**6, tam=650,sleep=2)
    #program.run()
   



