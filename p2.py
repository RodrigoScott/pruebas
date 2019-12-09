#cambios de código

import math
import random
import sys
from sys import argv #para recibir argumentos desde linea de comandos 
 
class aco_TSP:
    def __init__(self,debug):
        self.debug = debug
        self.distancia = []
        self.feromonas = []
        self.visibilidad =[]
        self.alfa = 1.0
        self.beta = 1.0
        self.P = 0.5
        self.Q = 10
        self.Tij = 1.0
        self.ciudades = 0
        self.hormigas = 0
        self.pos_hormiga = 0
        self.pos_anterior = 1
        self.recorridos = [] 
        self.sitios = [0]
 
         
    def inicio(self):
        #La distancia de nuestro blog
        self.distancia =[[0,8,7,1,3,1,1,1,1,7,5],[8,0,1,1,1,4,1,1,4,5,4],[7,1,0,1,6,1,1,7,1,1,1],[1,1,1,0,1,1,2,1,3,1,1],[3,1,6,1,0,5,1,5,1,1,4],[1,4,1,1,5,0,3,5,3,1,1],[1,1,1,2,1,3,0,5,3,1,1],[1,1,7,1,5,5,5,0,1,1,1],[1,4,1,3,1,3,3,1,0,1,1],[7,5,1,1,1,1,1,1,1,0,1],[5,4,1,1,4,1,1,1,1,1,0]]
        #El numero de hormigas = #ciudades 
        self.hormigas = 4
        self.ciudades = len(self.distancia) #self.ciudades = self.hormigas = len(self.distancia)
        #Arreglo vacio para las feromonas de cada arista
        self.feromonas = [[0,0.01,0.01,0,0.01,0,0,0,0,0.01,0.01],[0.01,0,0,0,0,0.01,0,0,0.01,0.01,0.01],[0.01,0,0,0,0.01,0,0,0.01,0,0,0],[0,0,0,0,0,0,0,0.01,0,0.01,0],[0.01,0,0.01,0,0,0.01,0,0.01,0,0,0.01],[0,0.01,0,0,0.01,0,0.01,0.01,0.01,0,0.01],[0,0,0,0.01,0,0.01,0,0.01,0.01,0,0],[0,0,0.01,0,0.01,0.01,0.01,0,0,0,0],[0,0.01,0,0.01,0,0.01,0.01,0,0,0,0],[0.01,0.01,0,0,0,0,0,0,0,0,0],[0.01,0.01,0,0,0.01,0.01,0,0,0,0,0]]
        self.visibilidad = [[0,0.125,0.142,0,0.333,0,0,0,0,0.142,0.2],[0.125,0,0,0,0,0.25,0,0,0.25,0.2,0.25],[0.142,0,0,0,0.167,0,0,0.142,0,0,0],[0,0,0,0,0,0,0.5,0,0.333,0,0],[0.333,0,0.167,0,0,0.2,0,0.2,0,0,0.25],[0,0.25,0,0,0.2,0,0.333,0.2,0.333,0,1],[0,0,0,0.5,0,0.333,0,0.2,0.333,0,0],[0,0,0.142,0,0.2,0.2,0.2,0,0,0,0],[0,0.25,0,0.333,0,0.333,0.333,0,0,0,0],[0.142,0.2,0,0,0,0,0,0,0,0,0],[0.2,0.25,0,0,0.25,1,0,0,0,0,0]]
        print ("distancia:",self.distancia)
        print ("")
        print ("Feromonas:",self.feromonas)
        print ("")
 
    def correrHormiga(self):
        gral = []
        for hormigas in range(self.ciudades):
            r =  self.seleccionarArista() #mando a correr a una hormiga y almacen en r su recorrido
            gral.append(r)#mando los recorridos a una arreglo general
            self.actualizarFeromonas(r) #al final de cada hormiga actualizo la feromona
        print ("Recorridos de cada hormiga: ",gral)
 
        self.evaluarRecorridos(gral) #Evaluo los recorridos de cada Hormiga
         
                             
    def seleccionarArista(self):#,distancia):
        #for i in xrange(2):
        ruleta = []
        pos_hormiga = self.pos_hormiga
        #variables de la formula
        sumatoria = 0
        Tij_and_Nij = []
        pos_ant = 0
        pos_act = 0
        aristas_checar = []
        recorridos=[0]

        for hormigas in range(self.ciudades-1):
            aristas_checar = []
            for i in range(self.ciudades): #checar que puede usar la lista
                if not i in recorridos and i !=0:
                    aristas_checar.append(i)
            #if self.debug:
            #print ("Aristas a checar: ",aristas_checar)    
 
            Tij_and_Nij = []
            for elemento in aristas_checar: #sacar la sumatoria
                #calcular tij and nij
                #if self.debug:
                #print ("elemento: ",elemento," pos_hormiga: ",pos_hormiga)
                    #print ("\t elemento distancia: ",self.distancia[pos_hormiga][elemento])
                Tij = self.feromonas[pos_hormiga][elemento]
                Nij = 1.0/self.distancia[pos_hormiga][elemento]
                elev = math.pow(Tij,self.alfa)*math.pow(Nij,self.beta)
                Tij_and_Nij.append(elev)
 
            for elemento in Tij_and_Nij:    
                sumatoria += elemento
            if self.debug:    
                print ("soy TN: ",Tij_and_Nij)
                print ("voy a ruleta")
             
            ruleta = []
            i=0
            for T_N in Tij_and_Nij:#asignar a ruleta en base a probabilidad
                Pij = T_N/sumatoria
                if self.debug:
                    print ("Soy Pij de elem: ",Pij)
                for j in range(int(math.ceil(Pij*10.0)+1)):
                    ruleta.append(i)
                i+=1
 
            if self.debug:
                print ("Tij_and_Nij: ",Tij_and_Nij)
                print ("Sumatoria: ",sumatoria)
                print ("Ruleta: ",ruleta)
 
            random.shuffle(ruleta)#chaca chaca 
 
            #SELECCIONAR ARISTA DE LA RULETA
            arista = aristas_checar[ruleta[0]] #seleccinamos una arista
         
            if self.debug:
                print ("Arista selccionada: ",arista)
 
            pos_ant = pos_act
            pos_act = arista
            recorridos.append(pos_act)
            if self.debug:
                print ("vengo de : ",pos_ant,"voy a : ",pos_act)
                print ("mis sitios visitados: ",recorridos)
            self.ponerFeromonas(pos_ant,pos_act)
        recorridos.append(0)
        return recorridos
             
    def ponerFeromonas(self,pos_anterior,pos_hormiga):
        self.feromonas[pos_hormiga][pos_anterior] += self.Tij
        self.feromonas[pos_anterior][pos_hormiga] += self.Tij
        if self.debug:
            """print ("Feromonas: ",self.feromonas)"""
 
    def sumaTij_K(self,recorridos):
        suma = 0
        #for i in range(self.ciudades):
        L_k = 0
        for elemento in recorridos:
            L_k += elemento
        suma += self.Q/L_k
        return suma
 
    def actualizarFeromonas(self,recorridos):
         
        sumaT_i_j = self.sumaTij_K(recorridos)
        nuevas_feromonas = []
        for i in range(len(self.feromonas)):
            lote = []
            for elemento in self.feromonas[i]:
                lote.append( (1-self.P)*elemento + sumaT_i_j )
            nuevas_feromonas.append(lote)
 
        self.feromonas = nuevas_feromonas
        if self.debug:
            """print ("Nuevas feromonas: ",self.feromonas)"""
 
    def evaluarRecorridos(self,recorridos):
        index = 0
        evaluacion_ant = 0
        for i in range(len(recorridos)):
            evaluacion = 0
            elem_ant = 0
            for elemento in recorridos[i]:
                #if elemento != 0:
                evaluacion += self.distancia[elem_ant][elemento]
                elem_ant = elemento
             
            if evaluacion < evaluacion_ant:
                index = i
                evaluacion_ant = evaluacion
            if evaluacion_ant == 0:
                evaluacion_ant = evaluacion
 
            print ("Recorrido Hormiga =",i+1," evaluacion: ",evaluacion)
 
        print ("\nEl optimo es con: ",recorridos[index]," en camino: ",index+1)
                     
#FIN DE LA CLASE
 
debug = 0
distancia = 1
ciudades = 10
 
aco = aco_TSP(debug)
aco.inicio()   
aco.correrHormiga()

#evaluación es el total del recorrido, el index es el camino con mayor feromona

#agrenar nueva linea