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
        self.BestGene = None
        self.Chromosome = self.initChromosome()
        self.initialization()
        self.selection()

    class initChromosome:
        def __init__(self):
            self.population = None
            self.fitness = None
            self.normalfitness = None
            self.parent1 = None
            self.parent2 = None

    def initialization(self):
        self.Chromosome.population = []
        self.Chromosome.fitness = []
        self.Chromosome.normalfitness = []
        idx = 20
        for i in range(self.M):
            gene = np.random.random_integers(self.LB[0],self.UB[0],self.n[0])
            self.Chromosome.population.append(gene)
            self.Chromosome.fitness.append(idx)
            idx -= 1

    def selection(self):
        temp_population = []
        cum_sum = []
        value = np.sum(self.Chromosome.fitness)
        normalized_fitness = [x / value for x in self.Chromosome.fitness]
        self.Chromosome.normalfitness = normalized_fitness
        for i in range(self.M):
            temp_population.append((self.Chromosome.population[i],self.Chromosome.fitness[i],self.Chromosome.normalfitness[i]))
        temp_population.sort(reverse=True, key=lambda x: x[2])
        cum_sum = np.cumsum(self.Chromosome.normalfitness)
        cum_sum = cum_sum[::-1]

        rand_num1 = np.random.random_sample()
        parent1_idx = np.where(cum_sum < rand_num1)
        parent1_idx = len(parent1_idx[0])

        rand_num2 = np.random.random_sample()
        parent2_idx = np.where(cum_sum < rand_num2)
        parent2_idx = len(parent2_idx[0])

        self.Chromosome.parent1 = temp_population[parent1_idx]
        self.Chromosome.parent2 = temp_population[parent2_idx]
