from GA import *
import numpy as np
from fuzzy import *
from fitnessFunc import *

M = 10
MaxGen = 4
Pc = 0.8
Pm = 0.2
Er = 0.1

n = [13, 13, 9, 15, 25]
UB = [32, 32, 10, 1, 3]
LB = [0, 0, 0, -1, 1]
type = ['int','int','int','float','int']

enemy_no = 1
level_quit = 2

gaTest = GA(M, MaxGen, Pc, Pm, Er, n, UB, LB, type, enemy_no, level_quit)
for i in range(len(gaTest.Chromosome.population)):
    print(gaTest.Chromosome.population[i])
print(gaTest.BestChrom)
