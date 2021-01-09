#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 12:39:08 2021

@author: Thore
"""
import pandas as pd
import requests
import lxml.html as lh
import re

def _get_url(base_url, cardname) -> str:
    """
    Parameters
    ----------
    cardname : STR
        Name of mtg card (correct spelling)

    Returns
    -------
    url : STR
        URL to card on LilianaMarket. Doesn't Check that URL exists!'

    """
    #non a-z becomes ''
    words_list = re.findall('[A-Za-z]*', cardname) 
    #remove ''
    while '' in words_list: words_list.remove('') 
    #hypen separated
    cardname_clean = '-'.join(words_list) 
    #create URL
    url = base_url + cardname_clean
    return url

def get_mm_suppliers(cardname) -> pd.DataFrame:
    """Finds all offers on magicmadhouse.co.uk of cardname.

    Returns
    -------
    Pandas DataFrame of sellers, with seller_name,Language,
    Foil/NotFoil,Price,num in stock

    """
    url_base = "https://www.magicmadhouse.co.uk/search/"
    url = _get_url(url_base, cardname)
    
    #get website content
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    #all cards listed on homepage
    tr_elements = doc.xpath("//div[starts-with(@class,'product p')]")
    
    headers = ['Seller', 
           'Language', 
           'URL', 
           'Condition',
           'Card type', 
           'Price', 
           '# in stock']
    
    data = []
    for node in tr_elements:
        try:
            cardname_scraped = node.xpath(".//a[starts-with(@href,'/magic-the-gathering')]/@title")[1]
            url_ = node.xpath(".//a[starts-with(@href,'/magic-the-gathering')]/@href")[1]
        except IndexError:
            continue #not a magic card
            
        price = float(node.xpath(".//span[@class='GBP']/text()")[0][1:])
        stock = node.xpath(".//span[starts-with(@class,'stock-message ')]/text()")[0]
        stock = (''.join(re.findall('[1-9]', stock)))
 
        #check card type
        if cardname_scraped.lower() == cardname.lower():
            cardtype = 'Regular'
        elif cardname_scraped.lower() == (cardname.lower() + ' (foil)'):
            cardtype = 'Foil'
        else:
            continue #not the right card
        
        #check stock
        try:
            stock = int(stock)
        except ValueError:
            continue #none in stock
            
        #correct card found
        #assume all cards are English
        data.append(['www.MagicMadhouse', 
                     'English', 
                     url + url_[1:], 
                     'Unknown',
                     cardtype,
                     price, 
                     stock])
        
    #turn into dataframe
    supplier_db = pd.DataFrame(data, columns = headers)
    return supplier_db
        
def get_lm_suppliers(cardname) -> pd.DataFrame:
    """Finds all sellers on lilianamarket.co.uk of cardname.

    Returns
    -------
    Pandas DataFrame of sellers, with seller_name,Language,Condition,
    Foil/NotFoil,Price,num in stock

    """
    url_base = "https://lilianamarket.co.uk/magic-cards/" 
    url = _get_url(url_base, cardname)
    
    #get website content
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')


    #Check that page has been found
    try:
        page.raise_for_status()
    except requests.HTTPError:
        print('error with card: '+cardname)
        raise
    
    headers = ['Seller', 
           'Language', 
           'URL', 
           'Condition',
           'Card type', 
           'Price', 
           '# in stock']
    
    #Reach here if headers found, so at least one card is sold
    #Fill table
    data = []
    #iterate through rows (first row is header)
    try:
        for listing in tr_elements[1:-1]:
            #get entries of each category in table row
            entries = [cat.text_content().strip() for cat in listing]
            #remove empty strings
            while '' in entries: entries.remove('') 
            seller = entries[0]
            url = "https://lilianamarket.co.uk/"+seller
            entries.insert(2, url)
            data.append(entries)
    except IndexError: #No cards listed
        pass
    
    #turn into dataframe
    supplier_db = pd.DataFrame(data, columns = headers)
    #change format of cost 
    supplier_db['Price'] = supplier_db['Price'].replace({'£':''}, regex = True).astype(float)
    #change format of num of cards
    supplier_db['# in stock'] = supplier_db['# in stock'].astype(int)
    return supplier_db

