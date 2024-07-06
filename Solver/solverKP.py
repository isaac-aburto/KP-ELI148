import numpy as np
import os
import time

from Problem.KP.problem import KP
from Metaheuristics.imports import iterarWOA, iterarGWO, iterarSCA
from Diversity.imports import diversidadHussain,porcentajesXLPXPT
from Discretization import discretization as b
from util import util
from BD.sqlite import BD

def solverKP(id, mh, maxIter, pop, instancia, DS, param):
    
    dirResult = './Resultados/'
    instance = KP(instancia)
    
    chaotic_map = None
    
    # tomo el tiempo inicial de la ejecucion
    initialTime = time.time()
    
    tiempoInicializacion1 = time.time()

    print("------------------------------------------------------------------------------------------------------")
    print("instancia SCP a resolver: "+instancia)
    
    results = open(dirResult+mh+"_"+instancia.split(".")[0]+"_"+str(id)+".csv", "w")
    results.write(
        f'iter,fitness,time,XPL,XPT,DIV\n'
    )
    
    # Genero una población inicial binaria, esto ya que nuestro problema es binario
    poblacion = np.random.randint(low=0, high=2, size = (pop, instance.getItems()))
    
    maxDiversidad = diversidadHussain(poblacion)
    XPL , XPT, state = porcentajesXLPXPT(maxDiversidad, maxDiversidad)
    
    # Genero un vector donde almacenaré los fitness de cada individuo
    fitness = np.zeros(pop)

    # Genero un vetor dedonde tendré mis soluciones rankeadas
    solutionsRanking = np.zeros(pop)
    
    # calculo de factibilidad de cada individuo y calculo del fitness inicial
    for i in range(poblacion.__len__()):
        flag = instance.factibilityTest(poblacion[i])
        if not flag: #solucion infactible
            poblacion[i] = instance.repair(poblacion[i])
            

        fitness[i] = instance.fitness(poblacion[i])
        
    # esta funcion ordena de menor a mayor
    solutionsRanking = np.argsort(fitness) # rankings de los mejores fitnes
    # es de maximizacion
    bestRowAux = solutionsRanking[pop-1]
    
    # DETERMINO MI MEJOR SOLUCION Y LA GUARDO 
    Best = poblacion[bestRowAux].copy()
    BestFitness = fitness[bestRowAux]
    
    # PARA MFO
    BestFitnessArray = fitness[solutionsRanking] 
    bestSolutions = poblacion[solutionsRanking]
    
    matrixBin = poblacion.copy()
    
    tiempoInicializacion2 = time.time()
    
    # mostramos nuestro fitness iniciales
    print("------------------------------------------------------------------------------------------------------")
    print("fitness incial: "+str(fitness))
    print("Best fitness inicial: "+str(BestFitness))
    print("------------------------------------------------------------------------------------------------------")
    if mh == "SCA":
        print("COMIENZA A TRABAJAR LA METAHEURISTICA "+mh)
    else: 
        print("COMIENZA A TRABAJAR LA METAHEURISTICA "+mh+ " / Binarizacion: "+ str(DS))
    print("------------------------------------------------------------------------------------------------------")
    print("iteracion: "+
            str(0)+
            ", best: "+str(BestFitness)+
            ", mejor iter: "+str(fitness[solutionsRanking[pop-1]])+
            ", peor iter: "+str(fitness[solutionsRanking[0]])+
            ", optimo: "+str(instance.getOptimum())+
            ", time (s): "+str(round(tiempoInicializacion2-tiempoInicializacion1,3))+
            ", XPT: "+str(XPT)+
            ", XPL: "+str(XPL)+
            ", DIV: "+str(maxDiversidad))
    results.write(
        f'0,{str(BestFitness)},{str(round(tiempoInicializacion2-tiempoInicializacion1,3))},{str(XPL)},{str(XPT)},{maxDiversidad}\n'
    )
    
    for iter in range(0, maxIter):
        # obtengo mi tiempo inicial
        timerStart = time.time()
        
        if mh == "MFO":
            for i in range(bestSolutions.__len__()):
                BestFitnessArray[i] = instance.fitness(bestSolutions[i])
        
        # perturbo la poblacion con la metaheuristica, pueden usar SCA y GWO
        # en las funciones internas tenemos los otros dos for, for de individuos y for de dimensiones
        # print(poblacion)  
        if mh == "SCA":
            poblacion = iterarSCA(maxIter, iter, instance.getItems(), poblacion.tolist(), fitness.tolist(), 'MAX')
        if mh == "GWO":
            poblacion = iterarGWO(maxIter, iter, instance.getItems(), poblacion.tolist(), fitness.tolist(), 'MAX')
        if mh == 'WOA':
            poblacion = iterarWOA(maxIter, iter, instance.getItems(), poblacion.tolist(), Best.tolist())
        
        # Binarizo, calculo de factibilidad de cada individuo y calculo del fitness
        for i in range(poblacion.__len__()):

            if mh != "GA":
                poblacion[i] = b.aplicarBinarizacion(poblacion[i].tolist(), DS[0], DS[1], Best, matrixBin[i].tolist(), iter, pop, maxIter, i, chaotic_map)

            flag = instance.factibilityTest(poblacion[i])
            # print(aux)
            if not flag: #solucion infactible
                poblacion[i] = instance.repair(poblacion[i])
                

            fitness[i] = instance.fitness(poblacion[i])


        solutionsRanking = np.argsort(fitness) # rankings de los mejores fitness
        
        #Conservo el Best
        if fitness[solutionsRanking[pop-1]] > BestFitness:
            BestFitness = fitness[solutionsRanking[pop-1]]
            Best = poblacion[solutionsRanking[pop-1]]
        matrixBin = poblacion.copy()

        div_t = diversidadHussain(poblacion)
        
        if maxDiversidad < div_t:
            maxDiversidad = div_t
            
        XPL , XPT, state = porcentajesXLPXPT(div_t, maxDiversidad)

        timerFinal = time.time()
        # calculo mi tiempo para la iteracion t
        timeEjecuted = timerFinal - timerStart
        
        print("iteracion: "+
            str(iter+1)+
            ", best: "+str(BestFitness)+
            ", mejor iter: "+str(fitness[solutionsRanking[pop-1]])+
            ", peor iter: "+str(fitness[solutionsRanking[0]])+
            ", optimo: "+str(instance.getOptimum())+
            ", time (s): "+str(round(timeEjecuted,3))+
            ", XPT: "+str(XPT)+
            ", XPL: "+str(XPL)+
            ", DIV: "+str(div_t))
        
        results.write(
            f'{iter+1},{str(BestFitness)},{str(round(timeEjecuted,3))},{str(XPL)},{str(XPT)},{str(div_t)}\n'
        )
    print("------------------------------------------------------------------------------------------------------")
    print("Best fitness: "+str(BestFitness))
    print("Cantidad de columnas seleccionadas: "+str(sum(Best)))
    print("------------------------------------------------------------------------------------------------------")
    finalTime = time.time()
    tiempoEjecucion = finalTime - initialTime
    print("Tiempo de ejecucion (s): "+str(tiempoEjecucion))
    results.close()
    
    binary = util.convert_into_binary(dirResult+mh+"_"+instancia.split(".")[0]+"_"+str(id)+".csv")

    nombre_archivo = mh+"_"+instancia.split(".")[0]

    bd = BD()
    bd.insertarIteraciones(nombre_archivo, binary, id)
    bd.insertarResultados(BestFitness, tiempoEjecucion, Best, id)
    bd.actualizarExperimento(id, 'terminado')
    
    os.remove(dirResult+mh+"_"+instancia.split(".")[0]+"_"+str(id)+".csv")