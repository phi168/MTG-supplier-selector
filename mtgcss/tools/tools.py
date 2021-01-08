#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 09:59:32 2021

@author: Thore
"""
#%% Imports
import os 
import pandas as pd
import tools.webscrape as ws
from itertools import combinations
from scipy.special import comb
from random import randint
import numpy as np
#%% Classes
class Card:
    """Card class: name and how many of that card are required"""
    
    def __init__(self, cardname, cardnumber):
        self.name = cardname
        self.number = cardnumber
    
    def __repr__(self):
        return 'Card(%s, %d)' % (self.name, self.number)
        

class CardList:
    """Class containing Cards"""
    
    def __init__(self, cardlist_dict):      
        """Initialise class"""
        
        self.cardlist = [Card(name, number) for (name, number) in zip(cardlist_dict['Name'], cardlist_dict['Number'])]
        self.count = -1
    
    def __repr__(self):
        """reprepresentation"""
        
        return '\n'.join([str(c) for c in self.cardlist])
    
    def __iter__(self):
        """return self for iteration"""
        
        return self
    
    def __len__(self):
        """return length"""
        
        return len(self.cardlist)
    
    def __next__(self):
        """iteration produces Card objects. Reset at the end for re-use"""
        
        self.count += 1
        try:
            return self.cardlist[self.count]
        except IndexError:
            self.count = -1
            raise StopIteration
    
    def __getitem__(self, i):
        return self.cardlist[i]
    
class SuppliersOfCard:
    """Class containing table of suppliers of a single card"""
    
    def __init__(self, supplier_db, cardname):
        """ Initialise Class
        
        Parameters
        ----------
        supplier_db : DataFrame
            Table containing suppliers of cards.
        cardname : Str
            Name of card."""
            
        self.supplier_db = supplier_db
        self.prices = np.array(supplier_db['Price'])
        self.sellers = np.array(supplier_db['Seller'])
        self.cardname = cardname
        try:
            self.stock = {i:int(v) for i,v in enumerate (supplier_db['# in stock'].to_numpy())}
            self.total_cards_on_offer = sum(self.stock.values())
        except TypeError:
            #no cards listed
            self.stock = {0:0}
            self.total_cards_on_offer = 0
        
        
    def get_all_configurations(self, num_cards):
        """get all possible ways to buy num_cards from for this card"""
        
        #all options
        options = [e for key in self.stock for s in [key]*self.stock[key] for e in [s]]
        #get possible configs
        #number of combinations:
        N = comb(len(options), num_cards)
        if N > 10E6:
            print('Number of options too high: Compute aborted')
            print(self.cardname)
            print(N)
            return []
            
        #use set to make them all unique
        configurations = set([c for c in combinations(options, num_cards)])
        #return list rather than set
        return list(configurations)
    def get_suppliers_from_config(self, configuration):
        """return suppliername:cardcost for each id in configuration"""
        out = []
        for c in configuration:
            name = self.sellers[c]
            cost = self.prices[c]
            url = list(self.supplier_db['URL'])[c]
            out.append([name, cost, url])
        return out       
            
    def get_cost_no_shipping(self, configuration):
        """get cost based on single order of cards, ignoring shipping"""
        
        cost = 0
        for c in configuration:
            cost += self.prices[c]
        return cost
    
    def get_supplier_names(self, configuration): 
        """get names of suppliers for a given order configuration"""
        
        return [self.sellers[i] for i in configuration]
    
class CostCalculator:
    """Class that takes in some choice of cards and computes the cost"""
    
    def __init__(self, suppliers_allcards, all_ensembles_dict):
        """Initialise CostCalculater Class"""
        
        keys = []
        ensembles = []
        ensemble_sizes = []
        suppliers = []
        for key in all_ensembles_dict:
            ensemble_size = len(all_ensembles_dict[key])
            if ensemble_size == 0: #we ignore cards that we cannot buy
                continue
            
            keys.append(key)
            ensembles.append(all_ensembles_dict[key])
            ensemble_sizes.append(ensemble_size)
            suppliers.append(suppliers_allcards[key])
            
        self.suppliers = suppliers
        self.ensembles = ensembles
        self.ensemble_sizes = ensemble_sizes
        self.keys = keys
        self.shipping_cost = 1
    
    def get_cost(self, sample: list):
        """Calculate cost of ordering all cards for a given ensemble."""
        
        selected_suppliers = []
        cost_cards_only = 0
        #for each card, get idx which corresponds to a possible Seller config
        for i, j in enumerate(sample): 
            #get which Seller configuration
            config = self.ensembles[i][j]
            #get cost for each seller
            cost = self.suppliers[i].get_cost_no_shipping(config)
            cost_cards_only += cost
            #append list of suppliers
            selected_suppliers.extend(self.suppliers[i].get_supplier_names(config))
        
        #get set of all suppliers and multiply by shipping cost for each supplier
        cost_shipping = len(set(selected_suppliers)) *  self.shipping_cost
        
        return(cost_cards_only, cost_shipping)
            
    def generate_arrangement(self):
        """Generate a random ensemble of buying configurations"""
             
        return [randint(0, upper_limit - 1) for upper_limit in self.ensemble_sizes]
    
    def generate_min_card_cost_arrangement(self):
        """Generate a ensemble with minimum cost_cards_only
        takes entries with lowest index.
        Assumes cards are sorted by price in ascending order"""
        
        return [np.argmin(np.sum(np.array(e),1)) for e in self.ensembles]
    
    def decode_arrangement(self, solution) -> pd.DataFrame:
        """take an arrangement of ensemble indeces and translate to suppliers"""
        sol = {}
        for i, idx in enumerate(solution):
            cardname = self.keys[i]
            config = self.ensembles[i][idx]
            sol[cardname] =  self.suppliers[i].get_suppliers_from_config(config)
        
        #turn dict into DataFrame
        headers = ['supplier', 'cardname', 'cost', 'url']    
        entries = []
        for key in sol:
            card = key
            for supplier, cost, url in sol[key]:
                entries.append([supplier, card, cost, url])
        
        return pd.DataFrame(entries, columns = headers)


#%% Functions
def _parse_cod(filename) -> CardList: 
    """Parse .COD filetypes (cockatric format .xml)
    Imports all cards anywhere in the deck
    """
    import xml.etree.ElementTree as et 
    xtree = et.parse(filename)
    xroot = xtree.getroot()
    xcards = xroot.findall('.//card') #find all cards in tree
    card_names = []
    card_numbers = []
    #get card name and number of cards and append to list
    for xcard in xcards:
        card_numbers.append(int(xcard.attrib.get('number')))
        card_names.append(xcard.attrib.get('name'))
    #turn list of cards into dataframe
    data = {'Name': card_names, 
            'Number': card_numbers}

    return(CardList(data))
    
def get_cardlist_from_filename(filename) -> CardList:
    """ Returns pandas database with parsed filename
    File should contain list of cards with number and card names
    """
    _, file_extension = os.path.splitext(filename)
    if file_extension == '.cod':
        cardlist = _parse_cod(filename)
        
        return(cardlist)
    else:
        raise NameError('Unknown filetype')

def get_suppliers(cardname):
    
    db1 = ws.get_lm_suppliers(cardname)
    db2 = ws.get_mm_suppliers(cardname)
    db = pd.concat([db1, db2]).reset_index(drop = True)
    print('%d sellers found for: '%len(db) + cardname)
    return SuppliersOfCard(db, cardname)
    

def get_suppliers_from_cardlist(cardlist: CardList) -> dict:
    """turn a cardlist into a dictionary cardname:SuppliersOfCard"""
    
    num_cards = len(cardlist)
    suppliers_allcards = {}
    for i, card in enumerate(cardlist):
        print('(%d/%d) '%(i+1,num_cards), end = '')
        suppliers_allcards[card.name] = get_suppliers(card.name)
    return suppliers_allcards

def get_dict_of_all_ensembles(cardlist: CardList, suppliers_allcards_dict: dict) -> dict:
    """for each card, calculate all possible arrangements required cards be bought. 
    

    Parameters
    ----------
    cardlist : CardList
        contains cardnames and numbers required. 
    suppliers_allcards : dict
        dictionary of cardname:SuppliersOfCard.
        

    Returns
    -------
    dict
        cardname: list of tuples of all possible buying combinations.

    """
    all_ensembles_dict = {}
    
    for card in cardlist:
        suppliers = suppliers_allcards_dict[card.name]
        configs = suppliers.get_all_configurations(card.number)
        all_ensembles_dict[card.name] = configs
        
    return all_ensembles_dict


