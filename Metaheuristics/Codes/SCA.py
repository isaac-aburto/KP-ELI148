import numpy as np
import random

# Sine Cosine Algorithm (SCA)
def iterarSCA(maxIter, t, dimension, population, fitness, typeProblem):
    r1 = 2 - 2*(t/maxIter)
    # r1 = t * (np.pi / maxIter) # Linearly decreases from 0 to pi
    sortedPositions = np.argsort(fitness)
    
    # eq. 3.6
    if typeProblem == "MIN":
        Xbest = population[sortedPositions[0]]
    if typeProblem == "MAX":
        Xbest = population[sortedPositions[-1]]
    
    for i in range(len(population)):
        for j in range(dimension):
            r2 = random.uniform(0, 2 * np.pi)
            r3 = random.uniform(0, 2)
            r4 = random.uniform(0, 1)
            
            if r4 < 0.5:
                population[i][j] = population[i][j] + r3 * np.sin(r2) * abs(r1 * Xbest[j] - population[i][j])
            else:
                population[i][j] = population[i][j] + r3 * np.cos(r2) * abs(r1 * Xbest[j] - population[i][j])
    
    return np.array(population)

