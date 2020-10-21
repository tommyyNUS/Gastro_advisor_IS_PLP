import pandas as pd

subtype = pd.read_csv("restaurants_with_subtypes.csv")

def get_restaurant(type,region,num):

    if (region == 'northeast' or region == 'north east' or region == 'north-east'): region = 'north,east'

    init = True
    getallinfo = False

    for foodquery in type:
        #query conditions here
        typecondition = subtype['type'].str.lower().str.contains(foodquery, regex=False)
        subtypecondition = subtype['food_subtype'].str.lower().str.contains(foodquery, regex=False)
        locationcondition = subtype['region'].str.lower().str.contains(region[0], regex=False)

        if (type != "any" and region != "whole"):
            if (init == True) : 
                foundtype = (typecondition | subtypecondition) & (locationcondition)
                init = False
            else : foundtype = foundtype & ((typecondition | subtypecondition) & locationcondition)
        
        elif (type != "any" and region == "whole"):
            if (init == True) : 
                foundtype = typecondition | subtypecondition
                init = False
            else : foundtype = foundtype & (typecondition | subtypecondition)
        
        elif (type == "any" and region != "whole"): foundtype = locationcondition
        else: getallinfo = True



    if (getallinfo == False):
        numfound = foundtype.values.sum()
        print(numfound,"entries found!\n")
        result = subtype['restaurant'][foundtype].head(num)
    else:
        numfound = len(subtype['restaurant'])
        print(numfound,"entries found!\n")
        result = subtype['restaurant'].head(num)    



    output = f'Restaurants Found (Top {num}): \n\n' 

    if (numfound != 0):
        for x in result:
            output=output + x + "\n"
        #print (output)

    if (output == f'Restaurants Found (Top {num}): \n\n'): output = "Sorry, no results found! Please try to refine your search terms.."

    return output

#print(get_restaurant(["curry fish head"],["west"],20))