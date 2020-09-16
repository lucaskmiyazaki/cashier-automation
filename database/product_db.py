# -*- coding: utf-8 -*-
"""
@author: Henrique Igai Wang

Functions responsible for database interaction
"""

import pandas as pd
import imp
product_class = imp.load_source("classes", "../classes/product_class.py")


# Receive String productName
# Return Product searchProduct, if there is a product with productName as its name
# Return int -1, if there is no product with productName as its name
def getProductPerName(productName):
    dataBase = pd.read_csv('products.csv')
    for i in range(len(dataBase)):
        searchName = dataBase["ProductName"][i]
        if (productName == searchName):
            searchID = dataBase["ProductId"][i]
            searchPrice = dataBase["ProductPrice"][i]
            searchProduct = product_class.Product(searchID, searchName, searchPrice)
            return searchProduct
    # Product name not found
    return (-1) 

# Return Array<Product> with all products in database
def getAllProducts():
    dataBase = pd.read_csv('products.csv')
    productsList = []
    for i in range(len(dataBase)):
        currID = dataBase["ProductId"][i]
        currName = dataBase["ProductName"][i]
        currPrice = dataBase["ProductPrice"][i]
        currProduct = product_class.Product(currID, currName, currPrice)
        productsList.append(currProduct)
    
    return productsList
        
# Receive String productName, dec price
# Return True, if it was changed the productName's price at database
# Return False, if it couldn't change        
def setProductPrice(productName, price):
    dataBase = pd.read_csv('products.csv')
    for i in range(len(dataBase)):
        currName = dataBase["ProductName"][i]
        if (productName == currName):
            # Change Product Price
            dataBase["ProductPrice"][i] = price
            # Save new value
            dataBase.to_csv('./products.csv', index = False)
            return True
    # Product name not found
    return False

# Receive String productName, dec productPrice
# Creates new Product(productName, productPrice) and adds to database
def addProduct(productName, productPrice):
    dataBase = pd.read_csv('products.csv')
    productId = len(dataBase)
    data = [{'ProductId': productId, 'ProductName': productName, 'ProductPrice': productPrice}]
    dataBase = dataBase.append(data,ignore_index=True)
    dataBase.to_csv('./products.csv', index = False)
   
# Receive Product product
# Delete product from database    
def deleteProduct(product):
    dataBase = pd.read_csv('products.csv')
    productName = product.getName()
    ID = 0
    newDB = pd.DataFrame(columns= ['ProductId', 'ProductName', 'ProductPrice'])
    for i in range(len(dataBase)):
        currProductName = dataBase["ProductName"][i]
        currProductPrice = dataBase["ProductPrice"][i]
        if (productName != currProductName):
            newData = [{'ProductId': ID, 'ProductName': currProductName, 'ProductPrice': currProductPrice}]
            newDB = newDB.append(newData, ignore_index=True)
            ID += 1
    
    
    newDB.to_csv('./products.csv', index = False)
            
# Return int product new ID
def getNewProductID():
    productList = getAllProducts()
    newID = len(productList)
    return newID

# Receive String productName
# If productName exists in database: return productID
# Else: return -1
def getProductID(productName):
    product = getProductPerName(productName)
    if (product == -1):
        return -1
    else:
        productID = product.getID()
        return productID

# Return array<String> allProductsNames
def getAllProductsNames():
    listProducts = getAllProducts()
    listNames = []
    for i in range (len(listProducts)):
        currProduct = listProducts[i]
        currName = currProduct.getName()
        listNames.append(currName)
    return listNames

def main():
    print(getProductPerName('coke'))
    setProductPrice('coke', 4.75)
    print(getProductPerName('coke'))
    print(getAllProductsNames())
    print(getNewProductID())
    addProduct("guaraná", 4.00)
    print(getProductID('guaraná'))
    deleteProduct(getProductPerName('guaraná'))
main()
