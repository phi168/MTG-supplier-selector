#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Magic the gathering card supplier selector

Created on Wed Jan  6 19:24:08 2021

@author: Thore
"""

from tools.optimisation import GeneticAlgorithm as ga
import tools.tools as t
import numpy as np
from matplotlib import pyplot as plt
import sys

class SupplierSelector:
    def __init__(self, cardlist_path: str, **kwargs):
        """Initialise SupplierSelector. Provide path to cardlist and the
        object will collect supplier information from the web upon instantiation.
        """
        #manual override if desired
        cardlist = kwargs.get('cardlist', None)
        suppliers_allcards = kwargs.get('suppliers_allcards', None)
        all_ensembles_dict = kwargs.get('all_ensembles_dict', None)
        
        if not cardlist:
            print('importing list ' + cardlist_path, end = '')
            self.cardlist = t.get_cardlist_from_filename(cardlist_path)
            print('\rimported card list '+ cardlist_path)
        else:
            self.cardlist = cardlist
        
        if not suppliers_allcards:
            print('importing suppliers of card..')
            self.suppliers_allcards = t.get_suppliers_from_cardlist(self.cardlist)
            print('received supplier information')
        else:
            self.suppliers_allcards = suppliers_allcards
        
        if not all_ensembles_dict:
            print('computing ensembles')
            self.all_ensembles_dict = t.get_dict_of_all_ensembles(self.cardlist, self.suppliers_allcards)
            print('finished computing ensembles')
        else:
            self.all_ensembles_dict = all_ensembles_dict
    
    def run(self, num_iterations = 50, **kwargs):
        """run the genetic algorithm to find the optimal card arrangement.
        The genetic algorithm object will be stored as self.model."""
        
        #setup system
        self.cost_calculator = t.CostCalculator(self.suppliers_allcards, self.all_ensembles_dict)
        bounds = np.array(self.cost_calculator.ensemble_sizes) - 1
        #define cost functions
        cost_func = lambda p: sum(self.cost_calculator.get_cost(p))
        #create model
        self.model = ga(cost_func, bounds, **kwargs)
        
        fitness_list = [];
        
        for i in range(num_iterations):
            #Update
            f = next(self.model)
            #get fitness values
            fitness_list.append(f[0])
            #Output
            print('\r(%d/%d) '%(i+1,num_iterations), end = '')
            print('top ensemble fitness: %1.1f   '%f[0], end = '')
            
        print('\nDone')
        self.solution = self.cost_calculator.decode_arrangement(self.model.get_solution())
    
    def plot_results(self):
        """create bar-chart of suppliers with num_cards and cost per supplier"""
        #get data
        new_df = self.solution.groupby('supplier').sum()
        new_df['count'] = self.solution.groupby('supplier').supplier.count()
        new_df = new_df.sort_values(by=['count'], ascending = False)
        
        #plotting 
        ax = new_df.plot.bar(secondary_y = 'cost', rot=90)
        ax.legend(loc='upper left', bbox_to_anchor=(0., 1.11, 1., .102))
        ax.right_ax.legend(loc='upper right', bbox_to_anchor=(0., 1.11, 1., .102))
        ax.set_ylabel('count')
        ax.set_xlabel('supplier name')
        ax.right_ax.set_ylabel('cost')
        plt.tight_layout()
        
    def print_results(self, filename = ''):

        sol = self.solution.sort_values(['supplier', 'cardname', 'cost']).reset_index(drop = True)
        
        card_cost = sol['cost'].sum()
        shipping_cost = len(groupby('supplier').sum())
        
        print("card cost = %1.1f£" % card_cost)
        print("shipping cost = %1.1f£" % shipping_cost)
        print("total cost = %1.1f£" % (card_cost + shipping_cost))
        print(sol)
        
        if filename:
            sol.to_csv(filename)
    
def main(path_in, path_out, *args):
    kwargs = {arg.split("=")[0]:float(arg.split("=")[1]) for arg in args}
    model = SupplierSelector(path_in)
    model.run(**kwargs)
    model.print_results(path_out)

    
#%%
if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        raise SyntaxError("Insufficient arguments.")
        
    if len(sys.argv) != 2:
        main(sys.argv[1], sys.argv[2], *sys.argv[3:])
    else:   
        main(sys.argv[1], sys.argv[2])
