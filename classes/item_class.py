# -*- coding: utf-8 -*-
"""
@author: Henrique Igai Wang

Class that represents each item of customer's cart
"""

import classes.product_class
import database.product_db as db

class Item:
    def __init__(self, productName, productQuantity=1):
        self.name = productName
        self.quantity = productQuantity
        productDB = db.getProductPerName(productName)
        self.itemPrice = productDB.getPrice()
        
    def getName(self):
        return self.name
    
    def getQuantity(self):
        return self.quantity
    
    def getIndividualPrice(self):
        return self.itemPrice
    
    def addQuantity(self, quantity):
        self.quantity += quantity
