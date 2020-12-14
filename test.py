from GA import *
import numpy as np
from fuzzy import *
from fitnessFunc import *
import matplotlib.pyplot as plt

# M must be even number
M = 50
MaxGen = 100
Pc = 0.9
Pm = 0.4
Er = 0.05

n =  [13, 13, 9,  9,  25, 25]
UB = [32, 32, 5,  10, 3,  3]
LB = [0,  0,  -5, 0 , 1,  1]

types = ['int','int','int','int','int','int']

# enemy_no = 2
# level_quit = 2
# iterations = 7

# gaTest = GA(M, MaxGen, Pc, Pm, Er, n, UB, LB, types)
# print('--------------------- Best Chromosome ------------------------')
# print(gaTest.BestChrom)
# print(gaTest.Fitness)


#################################################
# This section of code is used to test my defuzzification process
# Mu = [0, 0, 0.8136, 0.1864, 0]
# outMF_values = [(-3,-2,-1), (-2,-1,0), (-1, 0, 1), (0, 1, 2), (1,2,3)]
# fz = Defuzz(Mu, outMF_values)
# command = fz.defuzz_out()
# print(command)
# plt.plot(fz.max)
# plt.show()

#################################################
# This section of code is evaluating the two genes that were constructed
# Gene from Method 1
gene1 = [[9, 9, 2, 6, 4, 4, 26, 4, 2, 6, 3, 10, 23, 23, 31, 7, 28, 5, 21, 3, 24, 2, 8, 11,
        22, 32, 5, 4, 2, 0, -4, -1, -5, -2, 0, 2, 4, 5, 10, 6, 9, 1, 4, 6, 2, 1, 2, 3,
        2, 2, 2, 3, 3, 2, 1, 2, 3, 2, 3, 1, 2, 2, 1, 2, 2, 2, 3, 3, 1, 3, 2, 2,
        2, 2, 1, 1, 2, 2, 1, 1, 1, 3, 3, 3, 1, 3, 1, 2, 2, 2, 3, 1, 2, 1], 0, 0]
# Gene from Method 2
gene2 = [[9, 0, 10, 7, 13, 0, 1, 27, 18, 18, 28, 20, 22, 6, 9, 29, 19, 25, 24, 18, 27, 8, 18, 1,
        4, 0, 0, -2, 1, -3, -4, -5, -5, -5, 2, 1, 6, 4, 1, 4, 8, 9, 7, 10, 1, 2, 2, 3,
        1, 2, 2, 2, 3, 2, 2, 2, 2, 1, 2, 1, 1, 1, 3, 1, 2, 3, 3, 3, 3, 3, 2, 1,
        1, 1, 3, 1, 3, 3, 2, 2, 1, 1, 1, 2, 2, 3, 1, 1, 1, 2, 1, 3, 1, 3], 0, 0]
fit1 = []
fit2 = []
for i in range(10):
    fit = game(gene1, n)
    fit1.append(fit)

for j in range(10):
    fit = game(gene2, n)
    fit2.append(fit)
print('----------------------------------')
print('Fit 1')
print(fit1)
print('----------------------------------')
print('Fit 2')
print(fit2)
print('----------------------------------')
