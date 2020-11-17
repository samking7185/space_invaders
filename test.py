from GA import *
import numpy as np
from fuzzy import *
from fitnessFunc import *

M = 10
MaxGen = 4
Pc = 0.8
Pm = 0.2
Er = 0.1

n =  [13, 13, 9, 25, 13, 13, 15]
UB = [32, 32, 10, 3, 32, 32,  2]
LB = [0,  0,  0,  1,  0, 0,  -2]

type = ['int','int','int','int','int','int','float']

enemy_no = 1
level_quit = 2

gaTest = GA(M, MaxGen, Pc, Pm, Er, n, UB, LB, type, enemy_no, level_quit)

print(gaTest.BestChrom)
