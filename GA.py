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
        self.crossover()
        self.mutation()

    class initChromosome:
        def __init__(self):
            self.population = None
            self.fitness = None
            self.normalfitness = None
            self.parent1 = None
            self.parent2 = None
            self.child1 = None
            self.child2 = None

    def initialization(self):
        self.Chromosome.population = []
        self.Chromosome.fitness = []
        self.Chromosome.normalfitness = []
        fitval = 50
        for i in range(self.M):
            allele = []
            for idx,val in enumerate(self.n):
                gene_piece = np.random.randint(self.LB[idx],self.UB[idx],size=self.n[idx])
                gene = [str(i) for i in gene_piece]
                gene = "".join(gene)
                allele.append(gene)

            allele_string = [str(j) for j in allele]
            allele_whole = "".join(allele_string)
            self.Chromosome.population.append(allele_whole)
            self.Chromosome.fitness.append(fitval)
            fitval -= 1

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
        temp_child1 = []
        temp_child2 = []
        idxm = np.random.randint(1,self.n)

        for idx,num in enumerate(idxm):
            if idx == 0:
                endval = self.n[0]

                temp_child1.append(temp_parent1[0:num] + temp_parent2[num:endval])
                temp_child2.append(temp_parent2[0:num] + temp_parent1[num:endval])

            else:
                endval = np.sum(self.n[0:idx+1])
                startval = np.sum(self.n[0:idx])
                numval = num + np.sum(self.n[0:idx])

                temp_child1.append(temp_parent1[startval:numval] + temp_parent2[numval:endval])
                temp_child2.append(temp_parent2[startval:numval] + temp_parent1[numval:endval])
        r = np.random.rand(1,2)
        r = r[0]

        if r[0] <= self.Pc:
            self.child1 = "".join(temp_child1)
        else:
            self.child1 = temp_parent1
        if r[1] <= self.Pc:
            self.child2 = "".join(temp_child2)
        else:
            self.child2 = temp_parent2

    def mutation(self):
        temp_child1 = list(self.child1)
        temp_child2 = list(self.child2)

        r1 = np.random.rand(1,len(self.n))
        idxm1 = np.random.randint(1,self.n)
        valm1 = np.random.randint(1,self.UB)
        r1 = r1[0]

        r2 = np.random.rand(1,len(self.n))
        r2 = r2[0]
        idxm2 = np.random.randint(1,self.n)
        valm2 = np.random.randint(1,self.UB)

        for idx,num in enumerate(idxm1):
            if r1[idx] < self.Pm:
                print(idxm1)

                if idx == 0:
                    temp_child1[idxm1[0]] = valm1[idx]
                else:
                    numval = num + np.sum(self.n[0:idx])
                    temp_child1[numval] = valm1[idx]
            if r2[idx] < self.Pm:
                print(idxm2)

                if idx == 0:
                    temp_child2[idxm2[0]] = valm2[idx]
                else:
                    numval = num + np.sum(self.n[0:idx])
                    temp_child2[numval] = valm2[idx]
