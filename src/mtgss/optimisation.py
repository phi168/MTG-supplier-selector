#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 08:56:58 2021

@author: Thore
"""
import numpy as np
from numpy.random import exponential
from random import randint, uniform

class GeneticAlgorithm:
    def __init__(self, cost_func, bounds, N = 8000, mutation_rate = 0.05,
                 survivor_fraction = 0.1, num_children = 2, beta = 0.1, seed = []):
        """
        Create model for genetic algorithm solver

        Parameters
        ----------
        cost_func : function
            takes in population and computes cost.
        bounds : list or array
            upper bounds for population.
        N : int, optional
            population size. The default is 8000.
        mutation_rate : float, optional
            chance each gene mutates. The default is 0.05.
        survivor_fraction : TYPE, optional
            fraction of carry-over of fittest from previous gen. The default is 0.1.
        num_children : int, optional
            number of children each parent pair generates. The default is 2.
        beta: float, optional
            exp(-1)% of parents are chosen in top fraction of this size. The default is 0.1.
        seed : Array, optional
            initial population. Random if left empty. The default is [].

        """
        
        self.f = cost_func
        self.bounds  = bounds
        self.N = N #population size
        self.mutation_rate = mutation_rate #chance a feature mutates randomly
        self.survivor_fraction = survivor_fraction #fraction of fittest old gen carry-over to new gen
        self.num_children = num_children #number of children each selected pair generates
        self.beta = beta #exp(-1)% of parents are chosen in top fraction of this size

        if len(seed) == 0:
            print('randomly generating seed.')
            self.population = self.generate_random(N)
        else:
            self.population = seed
            
        assert len(self.population) == N, str(len(self.population))
        
    def generate_random(self, N):
        """generate random population of size N"""
        
        population = []
        for i in range(N):
            ensemble =  [randint(0, upper_limit) for upper_limit in self.bounds]
            population.append(ensemble)
        
        return np.array(population)
        
            
    def get_fitness(self):
        """compute fitness of population"""
        
        return np.array([self.f(p) for p in self.population])
    
    def get_diversity(self):
        """compote how varied the population is in each feature"""
        
        return np.array([len(np.unique(p)) for p in self.population.T])
    
    def __iter__(self):
        """make iterable"""
        return self
        
    def __next__(self):
        """Next step in optimisation: Update population by one generation"""
        #calculate fitness
        fitness = self.get_fitness()
        #calucate diversity
        diversity = self.get_diversity()
        
        #Oder popluation
        order = np.argsort(fitness)
        population_sorted = self.population[order]
        
        #create new generation
        population_newgen = []
        b = self.N * self.beta
        newsize = int(self.N * (1 - self.survivor_fraction))
        oldsize = int(self.N - newsize)
        
        while len(population_newgen) < newsize:
            #get random indeces to select parents
            pairs_idx = np.array(exponential(b, 2)).astype(int)
            if max(pairs_idx) >= (self.N - 1): #index too high
                continue #try again
            
            pair = population_sorted[pairs_idx]
            #cross over: randomly select features from 2 parents
            children = []
            for i in range(self.num_children):
                children.append([b[randint(0,1)] for b in pair.T])
            
            #mutate
            for child in children:
                for i, feature in enumerate(child):
                    #mutate this gene with a chance of mutation_rate
                    if uniform(0, 1) < self.mutation_rate:
                        child[i] = randint(0, self.bounds[i])        
            
            #add to population
            for child in children:
                population_newgen.append(child)
        
        #finished creating new population, turn to np.array
        population_newgen = np.array(population_newgen)
        #carry-over fittest from the old gen
        population_oldgen = population_sorted[0:oldsize,:]
        #update population
        self.population = np.concatenate((population_newgen,population_oldgen))
        return (min(fitness), diversity)
    
    def get_solution(self):
        """return fittest sample"""
        
        fitness = self.get_fitness()
        order = np.argsort(fitness)
        population_sorted = self.population[order]
        return population_sorted[0]
