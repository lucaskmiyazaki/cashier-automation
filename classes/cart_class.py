# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
@author: Henrique Igai Wang

Class that represents each item of customer's cart
"""

from classes.item_class import Item

class Cart:
    def __init__(self):
        self.productList = []
        
    def __str__(self):
        string = ""
        productList = self.getProductList()
        for i in range(len(productList)):
            string += "Product:{}; Quantity:{} \n".format(productList[i].getName(), productList[i].getQuantity())
        return string
        
    def addProduct(self, item):
        try:
            productName = item.getName()
            print(productName)
            i = self.haveProduct(productName)
            if (i >= 0):
                self.productList[i].addQuantity(1)
            else:
                self.productList.append(item)
            return True
        except:
            return False
        
    def getProductList(self):
        return self.productList
    
    # Receive String productName
    # Return int i >= 0 that represents the position of productName in the dataBase
    # Return -1 if there is no product in the database with its name as productName
    def haveProduct(self, productName):
        productList = self.getProductList()
        for i in range(len(productList)):
            currProductName = productList[i].getName()
            if (productName == currProductName):
                return i
        return -1
            
    
    