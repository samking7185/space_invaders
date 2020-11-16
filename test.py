from GA import *
import numpy as np
from fuzzy import *
from fitnessFunc import *

M = 6
MaxGen = 4
Pc = 1
Pm = 0.2
Er = 0.1

# n = [13, 13, 9, 15, 25]
# UB = [32, 32, 10, 1, 3]
# LB = [0, 0, 0, -1, 1]
# type = ['int','int','int','float','int']

n = [5, 5]
UB = [32, 32]
LB = [0, 0]
type = ['int','int']

enemy_no = 1
level_quit = 3

gaTest = GA(M, MaxGen, Pc, Pm, Er, n, UB, LB, type, enemy_no, level_quit)
for i in range(len(gaTest.Chromosome.population)):
    print(gaTest.Chromosome.population[i])
print(gaTest.BestChrom)


# gene = [1,2,3,4,5]
#
# fit = game(enemy_no, level_quit, gene)
# fitness_array = []
#
# fit = np.array(fit)
# searchval = 's'
# idx = np.where(fit == searchval)[0]
# idx = idx.tolist()
# fit = fit.tolist()
#
# for val in range(len(idx)-1):
#     fit_array = fit[idx[val]+1:idx[val+1]]
#     fitness_array.append(list(map(int, fit_array)))
# fitness_array.append(list(map(int, fit[idx[-1]+1:])))
# trimmed_fitness = []
#
# for list in fitness_array:
#     if list:
#         if list == [-50]:
#             temp = -50
#         else:
#             temp = np.amax(list)
#         trimmed_fitness.append(temp)
# print(trimmed_fitness)
