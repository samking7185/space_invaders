import numpy as np
import os
import time
from fitnessFunc import *
import sys
class GA:
    def __init__(self,M, MaxGen, Pc, Pm, Er, n, UB, LB, type, enemy, level_quit, iterations):
        self.M = M
        self.MaxGen = MaxGen
        self.Pc = Pc
        self.Pm = Pm
        self.Er = Er
        self.n = n
        self.UB = UB
        self.LB = LB
        self.type = type
        self.BestGene = None
        self.Fitness = []
        self.Chromosome = self.initChromosome()
        self.evolution(enemy, level_quit, iterations)
        # self.selection()
        # self.crossover()
        # self.mutation()

    class initChromosome:
        def __init__(self):
            self.population = None
            self.newPopulation = []
            self.newPopulation2 = []
            self.parent1 = None
            self.parent2 = None
            self.child1 = None
            self.child2 = None

    def evolution(self, enemy, level_quit, iterations):
        self.initialization()
        for idx in range(self.M):
            self.fitnessFunc(enemy, level_quit, idx, None, iterations)
        for idxm in range(1,self.MaxGen):
            for k in range(0,self.M,2):
                self.selection()
                self.crossover()
                self.mutation()
                self.Chromosome.newPopulation[k, 0] = np.array(self.Chromosome.child1)
                self.Chromosome.newPopulation[k+1, 0] = np.array(self.Chromosome.child2)
            for i in range(self.M):
                self.fitnessFunc(enemy, level_quit, i, 'New', iterations)
            self.elitism()
            self.Chromosome.population = self.Chromosome.newPopulation2
            self.Fitness.append(self.Chromosome.population[0,1])
            print('------------------------------------')
            print('Generation: ' + str(idxm))
            print(self.Chromosome.population[0,1])
            print(self.Chromosome.population[0,0])

        for idx in range(self.M):
            self.fitnessFunc(enemy, level_quit, k, None, iterations)
        self.Chromosome.population = self.Chromosome.population.tolist()
        self.Chromosome.population.sort(reverse=True, key=lambda x: x[1])
        self.BestChrom = self.Chromosome.population[0]

    def fitnessFunc(self, enemy, level_quit, ind, gene, iterations):
        fit_list = []
        if gene == 'Best':
            for i in range(iterations):
                fit = game(enemy, level_quit, gene, self.N, None, None)
                fit_list.append(fit)
        elif gene == 'New':
            for i in range(iterations):
                fit = game(enemy, level_quit, self.Chromosome.newPopulation[ind], self.n, i, iterations)
                fit_list.append(fit)
        else:
            for i in range(iterations):
                fit = game(enemy, level_quit, self.Chromosome.population[ind], self.n, i, iterations)
                fit_list.append(fit)

        trimmed_fitness = []
        for lst in fit_list:
            if lst is None:
                continue
            elif len(lst)==0:
                continue
            else:
                trimmed_fitness.append(np.amax(lst))
        fit_value = np.sum(trimmed_fitness)

        if gene == 'Best' :
            return fit_value
        elif gene == 'New':
            self.Chromosome.newPopulation[ind, 1] = fit_value
        else:
            self.Chromosome.population[ind, 1] = fit_value

    def initialization(self):
        self.Chromosome.population = []
        for i in range(self.M):
            allele = []
            for idx,val in enumerate(self.n):
                if self.type[idx] == 'int':
                    gene_piece = np.random.random_integers(self.LB[idx],self.UB[idx],size=self.n[idx])
                elif self.type[idx] == 'float':
                    gene_piece = np.random.uniform(self.LB[idx],self.UB[idx],size=self.n[idx])
                allele.append(gene_piece)
            self.Chromosome.population.append([np.concatenate(allele), 0, 0])
            self.Chromosome.newPopulation.append([np.array([0]), 0, 0])
            self.Chromosome.newPopulation2.append([np.array([0]), 0, 0])
        self.Chromosome.population = np.array(self.Chromosome.population, dtype=list)
        self.Chromosome.newPopulation = np.array(self.Chromosome.newPopulation, dtype=list)
        self.Chromosome.newPopulation2 = np.array(self.Chromosome.newPopulation2, dtype=list)

    def selection(self):
        temp_population = []
        cum_sum = []
        value = np.sum(self.Chromosome.population[:,1])
        normalized_fitness = [x / value for x in self.Chromosome.population[:,1]]
        self.Chromosome.population[:,2] = normalized_fitness

        for i in range(self.M):
            temp_population.append(self.Chromosome.population[i])
        temp_population.sort(reverse=True, key=lambda x: x[2])

        cum_sum = np.cumsum(self.Chromosome.population[:,2])
        cum_sum = cum_sum[::-1]

        rand_num1 = np.random.rand()
        parent1_idx = np.where(cum_sum < rand_num1)
        parent1_idx = len(parent1_idx[0])

        rand_num2 = np.random.rand()
        parent2_idx = np.where(cum_sum < rand_num2)
        parent2_idx = len(parent2_idx[0])

        self.Chromosome.parent1 = temp_population[parent1_idx]
        self.Chromosome.parent2 = temp_population[parent2_idx]

    def crossover(self):
        temp_parent1 = self.Chromosome.parent1[0]
        temp_parent2 = self.Chromosome.parent2[0]
        temp_parent1 = temp_parent1.tolist()
        temp_parent2 = temp_parent2.tolist()

        idxm = np.random.randint(1, np.sum(self.n))
        if idxm / np.sum(self.n) > 0.7:
            idxm = round(idxm*0.7)

        temp_child1 = temp_parent1[0:idxm] + temp_parent2[idxm:]
        temp_child2 = temp_parent2[0:idxm] + temp_parent1[idxm:]

        r = np.random.rand(1,2)
        r = r[0]

        if r[0] <= self.Pc:
            self.Chromosome.child1 = temp_child1
        else:
            self.Chromosome.child1 = temp_parent1
        if r[1] <= self.Pc:
            self.Chromosome.child2 = temp_child2
        else:
            self.Chromosome.child2 = temp_parent2

    def mutation(self):
        temp_child1 = self.Chromosome.child1
        temp_child2 = self.Chromosome.child2

        r1 = np.random.rand(1,len(self.n))
        idxm1 = np.random.randint(1,self.n)
        valm1 = np.random.randint(self.LB,self.UB)
        r1 = r1[0]

        r2 = np.random.rand(1,len(self.n))
        r2 = r2[0]
        idxm2 = np.random.randint(1,self.n)
        valm2 = np.random.randint(self.LB,self.UB)

        for idx,num in enumerate(idxm1):
            if r1[idx] < self.Pm:
                if idx == 0:
                    temp_child1[idxm1[0]] = valm1[idx]
                else:
                    numval = num + np.sum(self.n[0:idx])
                    temp_child1[numval] = valm1[idx]
            if r2[idx] < self.Pm:
                if idx == 0:
                    temp_child2[idxm2[0]] = valm2[idx]
                else:
                    numval = num + np.sum(self.n[0:idx])
                    temp_child2[numval] = valm2[idx]

    def elitism(self):
        newPopulation2 = []
        elite_no = round(np.multiply(self.M,self.Er))

        temp_population = self.Chromosome.population
        temp_population = temp_population.tolist()
        temp_population.sort(reverse=True, key=lambda x: x[1])
        temp_population2 = self.Chromosome.newPopulation
        temp_population2 = temp_population2.tolist()
        temp_population2.sort(reverse=True, key=lambda x: x[1])

        for i in range(elite_no):
            self.Chromosome.newPopulation2[i] = temp_population[i]

        for j in range(elite_no,self.M):
            self.Chromosome.newPopulation2[j] = temp_population2[j]

        # self.Chromosome.newPopulation2 = np.array(self.Chromosome.newPopulation2, dtype=list)
