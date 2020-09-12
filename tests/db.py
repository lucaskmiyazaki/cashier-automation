import os
#os.chdir('../')
import sys
sys.path.append('../')


from database.product_db import *
products = getAllProducts()
for product in products:
    print(product.getName())
