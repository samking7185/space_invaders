from GA import *
import numpy as np
from fuzzy import *
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

R = Rulebase()

print(R.AND_rule([0.2,1]))
