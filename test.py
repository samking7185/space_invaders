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

gaTest = GA(M, MaxGen, Pc, Pm, Er, n, UB, LB, types)
print('--------------------- Best Chromosome ------------------------')
print(gaTest.BestChrom)
print(gaTest.Fitness)


#################################################
# This section of code is used to test my defuzzification process
# Mu = [0, 0, 0.8136, 0.1864, 0]
# outMF_values = [(-3,-2,-1), (-2,-1,0), (-1, 0, 1), (0, 1, 2), (1,2,3)]
# fz = Defuzz(Mu, outMF_values)
# command = fz.defuzz_out()
# print(command)
# plt.plot(fz.max)
# plt.show()
