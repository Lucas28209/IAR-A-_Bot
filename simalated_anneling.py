import numpy as np

class Dados:
	def __init__(self):
		self.coord = np.loadtxt('51.txt')
		self.matrix = []
		for i in self.coord:
			#print(i[0])			
			self.matrix[int(i[0])].append(self.matrix[i][1],self.matrix[i][2])  
		print(self.matrix)



if __name__ == "__main__":
	dados = Dados()
