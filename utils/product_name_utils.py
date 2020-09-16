"""
@author: Henrique Igai Wang

Functions responsible for products names interactions
"""

# Receive array<String> listNames
# Return one String with all names from listNames separated by \n
def getProductNamesString(listNames):
    namesString = ""
    for i in range(len(listNames)):
        if (i == (len(listNames) - 1)):
            namesString += listNames[i]
        else:
            namesString += listNames[i] + '\n'
    return namesString