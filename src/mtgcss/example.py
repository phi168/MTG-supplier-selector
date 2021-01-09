#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 12:09:24 2021

@author: Thore
Generic algorithms
"""
from tools.optimisation import GeneticAlgorithm as ga
import tools.tools as t
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    #%% Load Card Info
    cardlist = t.get_cardlist_from_filename('resources/dec.cod')
    print('imported card list')
    suppliers_allcards = t.get_suppliers_from_cardlist(cardlist)
    print('received supplier information')
    all_ensembles_dict = t.get_dict_of_all_ensembles(cardlist, suppliers_allcards)
    print('computed ensembles')

    #%% try different population sizes
    cost_calculator = t.CostCalculator(suppliers_allcards, all_ensembles_dict)
    bounds = np.array(cost_calculator.ensemble_sizes) - 1
    
    #define cost functions
    cost_func = lambda p: sum(cost_calculator.get_cost(p))
    
    keys = ['N', 'seed', 'mutation_rate', 'survivor_fraction', 'beta']
    settings_val = [[4000, [], 0.0, 0.05, 0.15], 
                    [4000, [], 0.1, 0.05, 0.15],
                    [4000, [], 0.2, 0.05, 0.15],
                    [4000, [], 0.4, 0.05, 0.15]]
    labels = ['m0%', 'm10%', 'm20%', 'm40%']
    settings = [{keys[i]:val for i,val in enumerate(s)} for s in settings_val]
    
    models = [ga(cost_func, bounds, **s) for s in settings]
    
    fig = plt.figure()
    
    num_iterations = 50
    fitness_list = []
    
    for i in range(40):
        #Update
        f = [next(m) for m in models]
        #get fitness values
        fitness_list.append([e[0] for e in f])
        #Plot 
        plt.cla()
        for fitness, label in zip(np.array(fitness_list).T, labels):
            plt.plot(fitness, label=label)
        
        plt.xlabel('iteration')
        plt.ylabel('cost')
        plt.legend()
        fig.canvas.draw()
        fig.canvas.flush_events()
        
    
    winner = models[1].get_solution()
    #%% Plots
    #Start with Naive solution: Always pick cheapest cards
    min_cost = cost_calculator.generate_min_card_cost_arrangement()
    population = []
    for i in range(1000):
        ensemble = cost_calculator.generate_arrangement()
        population.append(ensemble)
        
    population = np.array(population)
    
    costs_ar = np.array([cost_calculator.get_cost(p) for p in population])
    mincosts_ar = np.array(cost_calculator.get_cost(min_cost))
    winner_ar = np.array(cost_calculator.get_cost(winner))  
                         
    plt.scatter(costs_ar[:,0], costs_ar[:,1], label = 'random')
    plt.scatter(mincosts_ar[0], mincosts_ar[1], label = 'min card cost (ignoring shipping)')
    plt.scatter(winner_ar[0], winner_ar[1], label = 'genetic algorithm winner')
    plt.ylabel('shipping cost')
    plt.xlabel('card cost')
    plt.show()
    plt.legend()


    #%% Analyse solution
    sol = cost_calculator.decode_arrangement(models[1].get_solution())
    
    new_df = sol.groupby('supplier').sum()
    new_df['count'] = sol.groupby('supplier').supplier.count()
    new_df = new_df.sort_values(by=['count'], ascending = False)
    ax = new_df.plot.bar(secondary_y = 'cost', rot=90)
    ax.legend(loc='upper left', bbox_to_anchor=(0., 1.11, 1., .102))
    ax.right_ax.legend(loc='upper right', bbox_to_anchor=(0., 1.11, 1., .102))
    ax.set_ylabel('count')
    ax.set_xlabel('supplier name')
    ax.right_ax.set_ylabel('cost')
    plt.tight_layout()
    
    sol = sol.sort_values(['supplier', 'cardname', 'cost'])
    sol = sol.reset_index(drop = True)
    
    card_cost = sol['cost'].sum()
    shipping_cost = len(new_df)
    
    print("card cost = %1.1f£" % card_cost)
    print("shipping cost = %1.1f£" % shipping_cost)
    print("total cost = %1.1f£" % (card_cost + shipping_cost))
    print(sol)
    
    sol.to_csv('out.txt')
