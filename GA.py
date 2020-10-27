import numpy as np
import os
import time

class GA:
    def __init__(self,M, MaxGen, Pc, Pm, Er, n, UB, LB):
        self.M = M
        self.MaxGen = MaxGen
        self.Pc = Pc
        self.Pm = Pm
        self.Er = Er
        self.n = n
        self.UB = UB
        self.LB = LB
        self.population = None
        self.Chromosome = None
        self.initialization()
        self.selection()

    def initialization(self):
        self.population = []
        self.Chromosome = []
        idx = 20
        for i in range(self.M):
            gene = np.random.random_integers(self.LB[0],self.UB[0],self.n[0])
            self.population.append(gene)
            self.Chromosome.append((gene, idx))
            idx -= 1

    def selection(self):
        self.Chromosome.sort(reverse=True, key=lambda x: x[1])
