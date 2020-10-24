import pandas as pd
import sqlite3

#conn = sqlite3.connect("gastrotommy.db")
#df = pd.read_sql_query("SELECT * FROM restaurant;", conn)

#print(df)

def get_restaurant(type,region,aspects):
    query = "SELECT * FROM restaurant"
    query = query + searchby_foodtype_region(type,region) + sort_by_aspect(aspects)
    conn = sqlite3.connect("gastrotommy.db")
    df = pd.read_sql_query(query, conn)
    print("SQL Query: " + query)
    return df

def detect_aspect(searchterms,item):
    array = []
    for x in searchterms: array.append(x in item)
    return all(array)


def searchby_foodtype_region(type,region):

    if (region == 'northeast' or region == 'north east' or region == 'north-east'): region = 'north,east'  
    query = " WHERE ("
    basefoodquery = "rest_type like '%**food**%' OR rest_food_type like '%**food**%'"
    foodquery = ""
    init = True

    if len(type) != 0:
        for x in type:
            x=x.lower()
            if(init==True): 
                foodquery = basefoodquery.replace("**food**",x)
                init = False
            else:
                foodquery = foodquery + " OR " + basefoodquery.replace("**food**",x)
    else:
        foodquery = ""
        

    if (region != "whole" and type !="any"):
        query = query + foodquery + ") AND rest_region like '%**region**%'".replace("**region**",region[0])
    elif (region == "whole" and type !="any"):
        query = query + foodquery + ")"
    elif (region != "whole" and type =="any"):
        query = query + "rest_region like '%**region**%'".replace("**region**",region[0]) + ")"    
    else:
        query = ""
    #print(query)
    return query



def sort_by_aspect(aspects):
    if len(aspects) == 1:
        #sortby_food = detect_aspect(aspects,["food"])
        query = " ORDER BY rest_food_rating DESC LIMIT 5;"
     
        
    elif len(aspects) == 2:
        sortby_food_service = detect_aspect(aspects,["food","service"])
        sortby_food_ambience = detect_aspect(aspects,["food","ambience"])
        sortby_food_price = detect_aspect(aspects,["food","price"])

        if sortby_food_service: 
            query = " ORDER BY w_fs_rating DESC LIMIT 5;"
        elif sortby_food_ambience:
            query = " ORDER BY w_fa_rating DESC LIMIT 5;"
        elif sortby_food_price:
            query = " ORDER BY w_fp_rating DESC LIMIT 5;"
          
    elif len(aspects) == 3:
        sortby_food_service_ambience = detect_aspect(aspects,["food","service","ambience"])
        sortby_food_service_price = detect_aspect(aspects,["food","service","price"])
        #sortby_food_ambience_price = detect_aspect(aspects,["food","ambience","price"])

        if sortby_food_service_ambience: 
            query = " ORDER BY w_fsa_rating DESC LIMIT 5;"
        elif sortby_food_service_price:
            query = " ORDER BY w_fsp_rating DESC LIMIT 5;"


    else:
        query = " ORDER BY w_rest_rating DESC LIMIT 5;"
       
    return query
