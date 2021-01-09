# -*- coding: utf-8 -*-
import pickle
import pytest
from mtgss.optimisation import GeneticAlgorithm as ga
import mtgss.tools as t
import numpy as np
from numpy.random import seed as npseed
from random import seed as rdseed
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname,'resources','objs.pkl')

## run this to overwrite the fixtures:
    # with open('objs.pkl', 'wb') as f: 
    #     pickle.dump([all_ensembles_dict, cardlist, suppliers_allcards, fitness_list], f)


@pytest.fixture
def all_ensembles_dict():
    with open(filename , 'rb') as f:  
        all_ensembles_dict = pickle.load(f)[0] 
    return all_ensembles_dict

@pytest.fixture
def cardlist():
    with open(filename , 'rb') as f:  
        cardlist = pickle.load(f)[1] 
    return cardlist

@pytest.fixture
def suppliers_allcards():
    with open(filename , 'rb') as f: 
        suppliers_allcards = pickle.load(f)[2] 
    return suppliers_allcards

@pytest.fixture
def fitness_list():
    with open(filename , 'rb') as f: 
        fitness_list = pickle.load(f)[3] 
    return fitness_list

def test_cardlist_import(cardlist):
    """test reading of cards from file"""
    print(cardlist)
    filename = os.path.join(dirname,'resources','dec.cod')
    assert(len(cardlist) == len(t.get_cardlist_from_filename(filename)))
    
# def test_webscrape(cardlist, suppliers_allcards):
#     """test that correct number of cards a scraped of the web"""
#     assert(len(suppliers_allcards) == len(t.get_suppliers_from_cardlist(cardlist)))
    
def test_findallcombinatoins(cardlist, suppliers_allcards, all_ensembles_dict):
    """test functionality to derive relevant supplier combinations"""
    temp_var  = t.get_dict_of_all_ensembles(cardlist, suppliers_allcards)
    assert len(temp_var) == len(all_ensembles_dict)
    
    for key in temp_var:
        assert(len(temp_var[key]) == len(all_ensembles_dict[key]))
    
def test_optimisation(suppliers_allcards, all_ensembles_dict, fitness_list):
    #setup cost
    cost_calculator = t.CostCalculator(suppliers_allcards, all_ensembles_dict)
    bounds = np.array(cost_calculator.ensemble_sizes) - 1
    cost_func = lambda p: sum(cost_calculator.get_cost(p))
    #setup random seeds
    npseed(1)
    rdseed(1)

    model = ga(cost_func, bounds, N=1000)
    
    fitness_list2 = [];
    num_iterations = 10
    for i in range(num_iterations):
        #Update
        f = next(model)
        #get fitness values
        fitness_list2.append(f[0])
        #Output
        print('\r(%d/%d) '%(i+1,num_iterations), end = '')
        print('top ensemble fitness: %1.1f   '%f[0], end = '')
            

    assert(fitness_list2 ==  fitness_list)