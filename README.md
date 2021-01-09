# MTGSS

Magic the gathering supplier selector.

Currently, the tool identifies sellers of magic cards on lilianamarket.co.uk as well as magicmadhouse.co.uk and identifies a low-cost combination of of whom to buy the cards in order to minimise (card_cost + shipping_cost). 
In the current version, minimisation is done stochastically over all possible combinations using a genetic algorithm. 
Currently only accepts cockatrice's .COD file format as input. 


## INSTALLATION

The module was written in Python 3.7.6 and is not anticipated to work in Python 2.x.
    pip install -e <path-to-projectfolder>

for easy command-line usage:
    brew install pipx
    pipx install mtgcss
    

## USAGE

In python: 
```python
import mtgss 
model = mtgss.SupplierSelector(path_to_cardlist)
model.run()
model.print_results(path_out)
```

In commandline (navigate to src/mtgss/):
```console
python mtgss.py path_to_cardlist output.csv
```
    
Or, with pipx installed as above:
```console
mtgcss path_to_cardlist output.csv
```

