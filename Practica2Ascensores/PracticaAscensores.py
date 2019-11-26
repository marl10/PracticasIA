# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'Practica2Ascensores'))
	print(os.getcwd())
except:
	pass
# %%
from IPython import get_ipython

# %%
#Representacion de los estados para la resolaucion del problema de los ascensores. 

#Estado Inicial: 
#          * personas indicando la plata actual en la que estan
#ini = ((1, 3, 4), ((0,[]),(0,[])))
ini = (((0,1), (1,7), (2,11)), ((0,0), (1,5), (1,6), (2, 10)))
#                   * Ascensores tambien indicando en la planta actual en la que estan. 


fin = ((1,6), (2,10), (0,3)) #Reresentacion des estado final solo de las personas ya que los ascensores no importa doende 
#acaben 


# %%
if (1,6) == (1,6):
    print("true")
else:
    print("false")


# %%
# importamos las cosas que vamos a usar de aima
from search import *

class Ascensores(Problem):
    ''' Clase Ascensores la cual implenta la clase abstracta Problema que nos ayuda a resover el porblema
           con varias funciones de busqueda '''
    def __init__(self,initial, goal):
        '''Metodo que inicializa nustro problema'''
        
        Problem.__init__(self, initial, goal)
        #self.search = initial
        self.goal = goal
        
        

from search import *

class Ascensores(Problem):
    ''' Clase Ascensores la cual implenta la clase abstracta Problema que nos ayuda a resover el porblema
           con varias funciones de busqueda '''
    def __init__(self,initial, goal):
        '''Metodo que inicializa nustro problema'''
        
        Problem.__init__(self, initial, goal)
        #self.search = initial
        self.goal = goal
        
        

    def actions(self, estado):
        '''Apartir de un estado(n) dado nos lista un conjunto de acciones(a) que le podimos aplicar a n para
        alcanzar otro estado n'  ''' 
        
        listaPersonas = list(estado[0])
        listAscensores = list(estado[1])
        
        acciones = list() 
      
        for i in range (len(listaPersonas)):
            persona = listaPersonas[i] #tupla (bloque, pisoAct)
            
            for j in range (len(listAscensores)):
                ascensor = listAscensores[j] #tupla (bloque, pisoAct)
                if persona != ascensor and ((ascensor[0] == 0 and ascensor[1] < 4) or (ascensor[0] == 1 and ascensor[1] < 8) or (ascensor[0] == 2 and ascensor[1] < 12)):
                    acciones.append((i,j, "Subir ascensor")) # sube al ascensor j a la planta donde esta la persona i
                if persona != ascensor and ((ascensor[0] == 0 and ascensor[1] > 0) or (ascensor[0] == 1 and ascensor[1] > 4) or (ascensor[0] == 2 and ascensor[1] > 8)):
                    acciones.append((i,j, "Bajar ascensor"))
                if persona == ascensor and persona[1] < 12: # para si la persona esta en la ultima planta solo
                    acciones.append((i,j, "Bajar pasajero"))           #pordria bajar 
                if persona == ascensor and persona[1] > 0: # Idem pero al reves 
                    acciones.append((i,j, "Subir pasajero"))
                #en el momento que ascensor este en la misma planta que la persona el arbol se ramifica en dos caminos
                #por lo que se generaran estas dos acciones. Quien decida que accion utilizar será la heuristica 
                #puesto que cogere la que menos heuristica tenga ya que estará mas cerca de la solución
                
        return acciones; 

        
    #accion = (plantaPersona,PlantaAscensor, accion en string)
    def result(self, estado, accion):
        '''Dado un estado(n, nodo actual) y una accion(a) nos permite general un nuevo nodo(n') aplicando la accion dada'''
        listaPersonas = list(estado[0]) #la primera(0)posicion de la tupla de estado la convertimos a una lista
        listAscensores = list(estado[1])# Idema para los ascensores con la segunda posicion (1)

        persona = accion[0] # Extraemos la posicion de la listaen donde se encutra la persona a modificar su posicion en el edificio
        ascensor = accion[1]# Idem con los ascensores 
                #Se hace simplemente para facilitar la lectura del codigo

        actualPersona = list(listaPersonas[persona]) #Planta actual donde se encutra la persona (bloque, posAct)
        actualAscensor = list(listAscensores[ascensor])#idem con el ascensor (bloque, posAct)

        if accion[2] == "Subir ascensor":
            actualAscensor[1] += 1 # Si es llamar a la posicion actual le asignamos la posicion 
                    #actual de la persona que ha solicitado el ascensor
            listaPersonas[persona] = tuple(actualPersona)
            listAscensores[ascensor] = tuple(actualAscensor)
        elif accion[2] == "Bajar ascensor":
            actualAscensor[1] -= 1 # Si es llamar a la posicion actual le asignamos la posicion 
                    #actual de la persona que ha solicitado el ascensor
            listaPersonas[persona] = tuple(actualPersona)
            listAscensores[ascensor] = tuple(actualAscensor)
        elif accion[2] == "Bajar pasajero": #Si es bajar restamos en uno la posicion actual de ambos(bajan un piso)
            actualPersona[1] -= 1 
            actualAscensor[1] -=1
            listaPersonas[persona] = tuple(actualPersona)
            listAscensores[ascensor] = tuple(actualAscensor)
        elif accion[2] == "Subir pasajero": #Si es Subir sumamos en uno la posicion actual de ambos(sube un piso)
            actualPersona[1] += 1
            actualAscensor[1] +=1
            listaPersonas[persona] = tuple(actualPersona)
            listAscensores[ascensor] = tuple(actualAscensor)
        else:
            print("error de formato de accion")
        
        return (tuple(listaPersonas), tuple(listAscensores))

    def goal_test(self, estado): # Devuelve true si se ha alcanzado el estado objetivo 
        return estado[0] == self.goal 


# %%
estado = ini
accion = (0,0, "Mover ascensor")

l = list(estado)
listaPersonas = list(estado[0]) #la primera(0)posicion de la tupla de estado la convertimos a una lista
listAscensores = list(estado[1])# Idema para los ascensores con la segunda posicion (1)
        
persona = accion[0] # Extraemos la posicion de la listaen donde se encutra la persona a modificar su posicion en el edificio
ascensor = accion[1]# Idem con los ascensores 
        #Se hace simplemente para facilitar la lectura del codigo
        
actualPersona = list(listaPersonas[persona]) #Planta actual donde se encutra la persona (bloque, posAct)
actualAscensor = list(listAscensores[ascensor])#idem con el ascensor (bloque, posAct)
        
if accion[2] == "Mover ascensor":
    actualAscensor[1] = int(actualPersona[1]) # Si es llamar a la posicion actual le asignamos la posicion 
            #actual de la persona que ha solicitado el ascensor
    listaPersonas[persona] = tuple(actualPersona)
    listAscensores[ascensor] = tuple(actualAscensor)
if accion[2] == "Bajar pasajero": #Si es bajar restamos en uno la posicion actual de ambos(bajan un piso)
    actualPersona[1] -= 1 
    actualAscensor[1] -=1
    listaPersonas[persona] = tuple(actualPersona)
    listAscensores[ascensor] = tuple(actualAscensor)
if accion[2] == "Subir pasajero": #Si es Subir sumamos en uno la posicion actual de ambos(sube un piso)
    actualPersona[1] += 1
    actualAscensor[1] +=1
    listaPersonas[persona] = tuple(actualPersona)
    listAscensores[ascensor] = tuple(actualAscensor)
        
print(tuple(listaPersonas), tuple(listAscensores))


# %%
p = Ascensores(ini, fin)
p.initial


# %%
p.result((((0, 1), (1, 7), (2, 11)), ((0, 0), (1, 5), (1, 6), (2, 10))), (0, 0 ""))


# %%
p.actions(p.initial)


# %%
p.result(p.initial, (0,0, "Mover ascensor"))


# %%
# Importamos los modulos pertenecinetes a los algoritmos de busqueda 
from search import *
from search import breadth_first_tree_search, depth_first_tree_search, depth_first_graph_search, breadth_first_graph_search


# %%
get_ipython().run_cell_magic('time', '', 'breadth_first_graph_search(p).solution()')


# %%
#Definimos algunas Hehuristicas 

def linear(node): # dado un estado nos devuelve las personas que todavia no estan en su planta objetivo
# es decir, que estan mal colocadas (como en el puzzle de 8)
    result = 0
    goal = fin
    estado = node.state[0]
    
    for i in range (len(estado)):
        if goal[i] != estado[i]:
            result += 1
    return result

# Sería como el de distancia hasta su objetivo quitando los if que comprueban las paradas para cambio de ascensor
def paradasTotales(node):
    result = 0
    bloque1 = (0,1,2,3,4)
    bloque2 = (4,5,6,7,8)
    bloque3 = (8,9,10,11,12)
    
    goal = fin
    estado = node.state[0] 
    
    for i in range (len(estado)):
        plantaIni = estado[i][1]
        plantaFin = goal[i][1]
        #podemos ignorar la comporacion de goal[i] == estado[i] ya que el resultado es 0
        result += abs(plantaFin - plantaIni)
        
        if plantaFin != plantaIni: 
        #Hago esto con conjuntos para determinar las paradas que han de hacer los ascensores Lentos
        #Por ejemplo si el inicio esta en el bloque 1 y el objetivo es el bloque3 entonces ha de hacer dos paradas
            if plantaIni < plantaFin: #Sube 
                if plantaFin in bloque2 and plantaIni in bloque1: 
                    result += 1
                elif plantaFin in bloque3 and plantaIni in bloque1:
                    result +=2
                elif plantaFin in bloque3 and plantaIni in bloque2:
                    result += 1
            else: # Baja
                if plantaIni in bloque3 and plantaFin in bloque2: 
                    result += 1
                elif plantaIni in bloque3 and plantaFin in bloque1:
                    result +=2
                elif plantaIni in bloque2 and plantaFin in bloque1:
                    result += 1
                
    return result

def distanciaParaObjetivo(node):
    result = 0
    goal = fin
    estado = node.state[0]
    
    for i in range (len(estado)):
        if(goal[i][1] != estado[i][1]):
            result += abs(goal[i][1] - estado[i][1])
    
    return result
        
    
    


# %%
get_ipython().run_cell_magic('time', '', 'astar_search(p, distanciaParaObjetivo).solution()')


# %%



