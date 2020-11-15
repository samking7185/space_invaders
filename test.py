from GA import *
import numpy as np
from fuzzy import *
from fitnessFunc import *
import numpy as np

M = 10
MaxGen = 100
Pc = 0.8
Pm = 0.2
Er = 0.1

n = [25, 10]
UB = [5, 5]
LB = [0, 0]
# gaTest = GA(M, MaxGen, Pc, Pm, Er, n, UB, LB)
# print(gaTest.Chromosome.normalfitness)
enemy_no = 1
level_quit = 5
gene = [1,2,3,4,5]
# fit = game(enemy_no, level_quit, gene)

fit = ['s', -50,
's', 30, 30, 30, 30, 30, 30, 100,
's', 10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 20, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
's', 10, 10, 10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]

fitness_array = []

fit = np.array(fit)
searchval = 's'
idx = np.where(fit == searchval)[0]
idx = idx.tolist()
fit = fit.tolist()

for val in range(len(idx)-1):
    fit_array = fit[idx[val]+1:idx[val+1]]
    fitness_array.append(list(map(int, fit_array)))
fitness_array.append(list(map(int, fit[idx[-1]+1:])))
trimmed_fitness = []

for list in fitness_array:
    if list:
        if list == [-50]:
            temp = -50
        else:
            temp = np.amax(list)
        trimmed_fitness.append(temp)
