MTGSS
#####

Magic the gathering supplier selector
Currently, the tool identifies sellers of magic cards on lilianamarket.co.uk as well as magicmadhouse.co.uk and identifies a low-cost combination of of whom to buy the cards in order to minimise (card_cost + shipping_cost). In the current version, minimisation is done stochastically over all possible combinations using a genetic algorithm. 


INSTALLATION
############

The module was written in Python 3.7.6 and is not anticipated to work in Python 2.x.


USAGE
#####

In command-line: 
.. code:: bash
    >>> python mtgss.py path_to_cardlist output.csv

