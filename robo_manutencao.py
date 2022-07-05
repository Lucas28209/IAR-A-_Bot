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
                    self.ambiente[i,j] = self.brown
                    self.custos[i,j] = 5
                elif self.ambiente[i,j] == 2:
                    self.ambiente[i,j] = self.blue
                    self.custos[i,j] = 10
                elif self.ambiente[i,j] == 3:
                    self.ambiente[i,j] =  self.orange
                    self.custos[i,j] = 15 
                elif self.ambiente[i,j] == 0:
                    self.ambiente[i,j] = self.green  
                    self.custos[i,j] = 1
                elif self.ambiente[i,j] == 2000:
                    self.ambiente[i,j] = 0  #preto, obstáculo
                    self.custos[i,j] = 2000  

        self.ambiente[int(self.locais[1,0]), int(self.locais[1,1]) ] = 310 #fábrica 1
        self.ambiente[int(self.locais[2,0]), int(self.locais[2,1]) ] = 320 #fábrica 2
        self.ambiente[int(self.locais[3,0]), int(self.locais[3,1]) ] = 330 #fábrica 3
        self.ambiente[int(self.locais[4,0]), int(self.locais[4,1]) ] = 340 #fábrica 4
        self.ambiente[int(self.locais[5,0]), int(self.locais[5,1]) ] = 350 #fábrica 5   

        # for item in self.itens:
        #     i=0
        #     while i < item:
        #         x = np.random.randint(0,42)
        #         y = np.random.randint(0,42)
        #         if self.ambiente[x,y] == 25:
        #             f = open("aa.txt", "a")
        #             f.write(f'{x} {y}\n')                    
        #             self.ambiente[x,y] = item
        #             i=i+1
        # f.close()
        f = np.loadtxt('aa.txt')
        #print(f[0][1])
        j=0
        for item in self.itens:
            i=0
            while i < item:
                x = int(f[j][0])
                y = int(f[j][1])
                self.ambiente[x][y] = item
                j=j+1
                i=i+1
        

class Node():
    def __init__(self, parent=None, position=None, cost=None):
        self.parent = parent
        self.position = position
        self.x , self.y = position

        self.custo = cost[int(self.x)][int(self.y)]

        self.g = 0
        self.h = 0
        self.f = 0
        self.c = 0

    def __eq__(self, other):
        return self.position == other.position
           
class Mostra():
    def __init__(self, ambiente):
        self.size = 42
        self.ambiente = ambiente
    
    def matriz(self):
        ret = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                ret[i,j] = self.ambiente[i][j]
        #print(ret)
        return ret
              

    def run(self):
            
            #time.sleep(0.01) 
            pg.init()
            tela = pg.display.set_mode((900, 900))
            tela.set_alpha(None)

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
            #time.sleep(2)
            #pg.image.save(tela,"screenshot.jpg")

class Robo():
    def __init__(self,raio, grid,coord,custos,locais):
        self.grid = grid #ambiente
        self.raio = raio   
        self.r_ = 9#self._calc_r_()
        self.coord_atual = [coord[0],coord[1]]
        self.custos = custos
        self.fabricas = locais
        self.custo_total = 0
        self.expansion = 0 

        self.baterias = 0
        self.solda = 0
        self.sucçao = 0 
        self.refri = 0
        self.pneu = 0

        self.fab_grao = [310, self.fabricas[0], 8, False]
        self.fab_casco = [320, self.fabricas[1], 5, False]
        self.fab_pet = [330, self.fabricas[2], 2, False]
        self.fab_cald = [340, self.fabricas[3], 5, False]
        self.fab_aco = [350, self.fabricas[4], 2, False]
        
        self.lista = [self.fab_grao, self.fab_casco,self.fab_pet, self.fab_cald,self.fab_aco]
        self.aux = False

        self.last_coord = [self.coord_atual[0],self.coord_atual[1]] #[x,y]
        self.last_color = self.grid[self.last_coord[0],self.last_coord[1]] #25
        
        self.grid[self.coord_atual[0],self.coord_atual[1]] = 1000 #robo
        
    def neighbors(self,radius, row_number, column_number):
        a = self.grid
        return [[[a[i][j], [i,j]] if  i >= 0 and i < len(a) and j >= 0 and j < len(a[0]) else None
                for j in range(column_number-1-radius, column_number+radius)]
                    for i in range(row_number-1-radius, row_number+radius)]

    # def vizinhos(self, vet, x,y):
    #     n = self.r_
    #     #print(n)
    #     vet = np.roll(np.roll(vet, shift=-x+1, axis=0), shift=-y+1, axis=1)

    #     #print('\n', (vet[:n,:n]))
    #     return vet[:9,:9]
    #This function return the path of the search
    def return_path(self,current_node,maze, soma):
        path = []
        
        
        result = self.grid.copy() 
        current = current_node
        while current is not None:
            path.append(current.position)
            current = current.parent
        # Return reversed path as we need to show from start to end path
        path = path[::-1]
        #start_value = 0
        # we update the path of start to end found by A-star serch with every step incremented by 1
        custo_atual = 0
        for i in range(len(path)):
            result[path[i][0]][path[i][1]] = 1#start_value
            if (soma==True):
                custo_atual += self.custos[path[i][0]][path[i][1]]
                #print('custo atual', custo_atual)
                self.custo_total += custo_atual#self.custos[path[i][0]][path[i][1]]
                #self.custo_total = self.custo_total + start_value
        
        mostra = Mostra(result)
        mostra.run()
        return result


    def search(self,maze, cost, start, end):

        # Create start and end node with initized values for g, h and f
        start_node = Node(None, tuple(start),self.custos)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, tuple(end),self.custos)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both yet_to_visit and visited list
        # in this list we will put all node that are yet_to_visit for exploration. 
        # From here we will find the lowest cost node to expand next
        yet_to_visit_list = []  
        # in this list we will put all node those already explored so that we don't explore it again
        visited_list = [] 
        
        # Add the start node
        yet_to_visit_list.append(start_node)
        
        # Adding a stop condition. This is to avoid any infinite loop and stop 
        # execution after some reasonable number of steps
        outer_iterations = 0
        max_iterations = (len(maze) // 2) ** 10

        # what squares do we search . serarch movement is left-right-top-bottom 
        #(4 movements) from every positon

        move  =  [[-1, 0 ], # go up
                [ 0, -1], # go left
                [ 1, 0 ], # go down
                [ 0, 1 ]] # go right


        
        #find maze has got how many rows and columns 
        no_rows, no_columns = np.shape(maze)
        
        # Loop until you find the end
        
        while len(yet_to_visit_list) > 0:
            
            # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
            outer_iterations += 1    
            self.expansion += outer_iterations
            
            # Get the current node
            current_node = yet_to_visit_list[0]
            current_index = 0
            current_cost = yet_to_visit_list[0].custo
            

            for index, item in enumerate(yet_to_visit_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
                    
            # if we hit this point return the path such as it may be no solution or 
            # computation cost is too high
            if outer_iterations > max_iterations:
                print ("giving up on pathfinding too many iterations")
                return self.return_path(current_node,maze)

            # Pop current node out off yet_to_visit list, add to visited list
            yet_to_visit_list.pop(current_index)
            visited_list.append(current_node)
            #print(visited_list)
            # test if goal is reached or not, if yes then return the path
            #self.return_path(current_node, maze,False)
            if current_node == end_node:
                #print(current_node.c)
                return self.return_path(current_node,maze,True)
            #else:
                

            # Generate children from all adjacent squares
            children = []

            for new_position in move: 

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range (check if within maze boundary)
                if (node_position[0] > (no_rows - 1) or 
                    node_position[0] < 0 or 
                    node_position[1] > (no_columns -1) or 
                    node_position[1] < 0):
                    continue

                # Make sure walkable terrain
                #if maze[node_position[0]][node_position[1]] != 0:
                    #continue

                # Create new node
                new_node = Node(current_node, node_position, self.custos)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:
                
                # Child is on the visited list (search entire visited list)
                if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                    continue

                # Create the f, g, and h values
                #print(current_cost)
                child.g = current_node.g + current_cost
                child.c = child.c + current_cost 
                #print(child.c)
                ## Heuristic costs calculated here, this is using eucledian distance
                child.h = ( abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])) 

                child.f = 1*child.g + 1*child.h

                # Child is already in the yet_to_visit list and g cost is already lower
                if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                    continue

                # Add the child to the yet_to_visit list
                yet_to_visit_list.append(child)

    def run(self):
        self.andar()
        return self.grid    

    def andar(self):
        
        #print(self.neighbors(1,self.coord_atual[0],self.coord_atual[1]))
        self.grid[self.coord_atual[0],self.coord_atual[1]] = self.last_color #volta a cor originial
        
        vet = (self.neighbors(4,self.coord_atual[0],self.coord_atual[1]))
        #print('\n',vet)
        for a in vet:
             if (a):
                #print('\n',a)            
                for i in a:                
                    if (i): #print(i)     
                        #print('\n',i) 
                        if ((i[0] == 350 ) and (self.fab_aco[2] <= self.pneu) and self.fab_aco[3] == False):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.pneu = self.fab_aco[2] - self.pneu
                            print("chegou na fábrica aco... itens restantes = ", self.pneu) 
                            self.fab_aco[3] = True  
                            return 
                        
                        elif ((i[0] == 330 ) and (self.fab_pet[2] <= self.sucçao) and self.fab_pet[3] == False):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.sucçao = self.fab_pet[2] - self.sucçao
                            print("chegou na fábrica pet... itens restantes = ", self.sucçao)
                            self.fab_pet[3] = True


                        elif ((i[0] == 320 ) and (self.fab_casco[2] <= self.solda) and self.fab_casco[3] == False):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.solda = self.fab_casco[2] - self.solda
                            print("chegou na fábrica casco... itens restantes = ", self.solda)
                            self.fab_casco[3] = True
                            return

                        elif ((i[0] == 340 ) and (self.fab_cald[2] <= self.refri) and self.fab_cald[3] == False):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.refri = self.fab_cald[2] - self.refri
                            print("chegou na fábrica cald... itens restantes = ", self.refri)
                            self.fab_cald[3] = True
                            return
                        
                        elif ((i[0] == 310) and (self.fab_grao[2] <= self.baterias) and self.fab_grao[3] == False ):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.baterias = self.fab_grao[2] - self.baterias
                            print("chegou na fábrica grao... itens restantes = ", self.baterias)
                            self.fab_grao[3] = True
                            return
 

                        elif ((i[0] == 4) and (self.pneu < self.fab_aco[2]) and self.fab_aco[3] == False):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.last_color = self.grid[self.coord_atual[0],self.coord_atual[1]]
                            if(self.is_item(4)):
                                self.last_color = 25
                            self.grid[self.coord_atual[0],self.coord_atual[1]] = 1000 #muda robo de lugar
                            return                                                           
                                                          
                        elif ((i[0] == 6) and (self.refri < self.fab_cald[2]) and self.fab_cald[3] == False):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.last_color = self.grid[self.coord_atual[0],self.coord_atual[1]]
                            if(self.is_item(6)):
                                self.last_color = 25
                            self.grid[self.coord_atual[0],self.coord_atual[1]] = 1000 #muda robo de lugar
                            return                            
                        elif ((i[0] == 8) and (self.sucçao < self.fab_pet[2]) and self.fab_pet[3] == False):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.last_color = self.grid[self.coord_atual[0],self.coord_atual[1]]
                            if(self.is_item(8)):
                                self.last_color = 25
                            self.grid[self.coord_atual[0],self.coord_atual[1]] = 1000 #muda robo de lugar
                            return
                        elif ((i[0] == 10) and (self.solda < self.fab_casco[2]) and self.fab_casco[3] == False):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.last_color = self.grid[self.coord_atual[0],self.coord_atual[1]]
                            if(self.is_item(10)):
                                self.last_color = 25
                            self.grid[self.coord_atual[0],self.coord_atual[1]] = 1000 #muda robo de lugar
                            return
                        elif ((i[0] == 20) and (self.baterias < self.fab_grao[2]) and self.fab_grao[3] == False):
                            self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [i[1][0],i[1][1]])
                            self.coord_atual[0] = i[1][0]
                            self.coord_atual[1] = i[1][1]
                            self.last_color = self.grid[self.coord_atual[0],self.coord_atual[1]]
                            if(self.is_item(20)):
                                self.last_color = 25
                            self.grid[self.coord_atual[0],self.coord_atual[1]] = 1000 #muda robo de lugar
                            return
                   
        a = self.coord_atual[0]
        b = self.coord_atual[1]
        
        if (self.fab_aco[3] == False and self.fab_aco[2] <= self.pneu ):
            if (self.coord_atual[0] - self.fab_aco[1][0] > 0 ):
                a = self.coord_atual[0]-4
            else:
                a = self.coord_atual[0]+4
            if (self.coord_atual[1] - self.fab_aco[1][1] > 0 ):
                b = self.coord_atual[1]-4
            else:
                b = self.coord_atual[1]+4

        elif (self.fab_pet[3] == False and self.fab_pet[2] <= self.sucçao ):
            if (self.coord_atual[0] - self.fab_pet[1][0] > 0 ):
                a = self.coord_atual[0]-4
            else:
                a = self.coord_atual[0]+4
            if (self.coord_atual[1] - self.fab_pet[1][1] > 0 ):
                b = self.coord_atual[1]-4
            else:
                b = self.coord_atual[1]+4
        
        elif (self.fab_casco[3] == False and self.fab_casco[2] <= self.solda ):
            if (self.coord_atual[0] - self.fab_casco[1][0] > 0 ):
                a = self.coord_atual[0]-4
            else:
                a = self.coord_atual[0]+4
            if (self.coord_atual[1] - self.fab_casco[1][1] > 0 ):
                b = self.coord_atual[1]-4
            else:
                b = self.coord_atual[1]+4    
        
        elif (self.fab_cald[3] == False and self.fab_cald[2] <= self.refri ):
            if (self.coord_atual[0] - self.fab_cald[1][0] > 0 ):
                a = self.coord_atual[0]-4
            else:
                a = self.coord_atual[0]+4
            if (self.coord_atual[1] - self.fab_cald[1][1] > 0 ):
                b = self.coord_atual[1]-4
            else:
                b = self.coord_atual[1]+4
        
        elif (self.fab_grao[3] == False and self.fab_grao[2] <= self.baterias ):
            if (self.coord_atual[0] - self.fab_grao[1][0] > 0 ):
                a = self.coord_atual[0]-4
            else:
                a = self.coord_atual[0]+4
            if (self.coord_atual[1] - self.fab_grao[1][1] > 0 ):
                b = self.coord_atual[1]-4
            else:
                b = self.coord_atual[1]+4 
        
        
        else:
            x = np.random.randint(4,38)            

            if (self.coord_atual[0] != x): 
                if (self.coord_atual[0] - x > 0 ):
                    a = self.coord_atual[0]-4
                else:
                    a = self.coord_atual[0]+4
                
            elif (self.coord_atual[1] != x): 
                if (self.coord_atual[1] - x > 0 ):
                    b = self.coord_atual[1]-4
                else:
                    b = self.coord_atual[1]+4


        self.search(self.grid, self.custos, [self.coord_atual[0], self.coord_atual[1]], [a,b])     
        
        self.coord_atual[0] = a
        self.coord_atual[1] = b

        self.last_color = self.grid[self.coord_atual[0],self.coord_atual[1]]
        self.grid[self.coord_atual[0],self.coord_atual[1]] = 1000 #muda robo de lugar
        
        return

    # def dist_manhattan(self,x,y):
    #     ret = 1000
    #     for i in range(len(self.fabricas)):
    #         x,y = self.fabricas[i] #print(len(self.fabricas)) #
    #         res = (abs(self.coord_atual[0] - x) + abs(self.coord_atual[1] - y))
    #         if ret > res:
    #             ret = res 
    #             newx = x 
    #             newy = y
    #         #print('distancia = ',res)
    #     return newx,newy
     
        
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
            
    def verifica(self):
        if (self.fab_grao[3] and self.fab_casco[3] and self.fab_pet[3] and self.fab_cald[3] and self.fab_aco[3]):
            print('custo = ',self.custo_total)
            print('expansoes = ',self.expansion)
            return True
        else:
            return False

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
        self.locais = coord[1:]
        self.coord = [int(coord[0,0]),int(coord[0,1])]
        self.custos = custos
        self.sleep = sleep
        self.pecas = [20,10,8,6,4] #peças
        self.lista = list()

        #print(self.ambiente)

        #self.distribui(self.ambiente, self.pecas)
        self.cria_robo(self.raio, self.ambiente,self.coord,self.custos,self.locais)

    def cria_robo(self,raio,ambiente,coord,custos,locais):
        robo = Robo(raio, ambiente,coord,custos,locais)
        self.lista.append(robo)
    
    def inicio(self):
        #time.sleep(self.sleep)
        for robo in self.lista:
            while (robo.verifica() == False):
            #for i in range (0,400):
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
            #print('oi')
            #time.sleep(0.05) 
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
    
