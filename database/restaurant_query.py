import pandas as pd
import sqlite3
from database.DataBase import DataBase

#conn = sqlite3.connect("gastrotommy.db")
#df = pd.read_sql_query("SELECT * FROM restaurant;", conn)

#print(df)


def get_more_restaurants(query,num):
    db=DataBase()

    morequery = query.replace('DESC LIMIT 5',f'DESC LIMIT 5 OFFSET {num}')
    df=db.fetch_restaurants_by_sql(morequery)
    print("SQL Query: " + morequery)
    return df   

def get_restaurant(type,region,aspects):
    db=DataBase()
    query = "SELECT rest_name, rest_address, rest_region, AVG(rest_food_rating) as rest_food_rating, AVG(rest_srvc_rating) as rest_srvc_rating, AVG(rest_ambi_rating) as rest_ambi_rating, AVG(rest_prce_rating) as rest_prce_rating, AVG(w_rest_rating) as w_rest_rating FROM restaurant"
    query = query + searchby_foodtype_region(type,region) + sort_by_aspect(aspects)
    df=db.fetch_restaurants_by_sql(query)
    print("SQL Query: " + query)

    return df,query

def detect_aspect(searchterms,item):
    array = []
    for x in searchterms: array.append(x in item)
    return all(array)


def searchby_foodtype_region(type,region):
    if (region != "whole"):
        if (region[0] == 'northeast' or region[0] == 'north east' or region[0] == 'north-east'): region[0] = 'north,east'
        region[0] = region[0].upper()  
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
                foodquery = foodquery + " AND " + basefoodquery.replace("**food**",x)
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
        query = " GROUP BY rest_name ORDER BY AVG(w_rest_rating) DESC LIMIT 5;"
     
        
    elif len(aspects) == 2:
        sortby_food_service = detect_aspect(aspects,["food","service"])
        sortby_food_ambience = detect_aspect(aspects,["food","ambience"])
        sortby_food_price = detect_aspect(aspects,["food","price"])

        if sortby_food_service: 
            query = " GROUP BY rest_name ORDER BY AVG(w_fs_rating) DESC LIMIT 5;"
        elif sortby_food_ambience:
            query = " GROUP BY rest_name ORDER BY AVG(w_fa_rating) DESC LIMIT 5;"
        elif sortby_food_price:
            query = " GROUP BY rest_name ORDER BY AVG(w_fp_rating) DESC LIMIT 5;"
          
    elif len(aspects) == 3:
        sortby_food_service_ambience = detect_aspect(aspects,["food","service","ambience"])
        sortby_food_service_price = detect_aspect(aspects,["food","service","price"])
        sortby_food_ambience_price = detect_aspect(aspects,["food","ambience","price"])

        if sortby_food_service_ambience: 
            query = " GROUP BY rest_name ORDER BY AVG(w_fsa_rating) DESC LIMIT 5;"
        elif sortby_food_service_price:
            query = " GROUP BY rest_name ORDER BY AVG(w_fsp_rating) DESC LIMIT 5;"
        elif sortby_food_ambience_price:
            query = " GROUP BY rest_name RDER BY AVG(w_fap_rating) DESC LIMIT 5;"


    else:
        query = " GROUP BY rest_name ORDER BY AVG(w_rest_rating) DESC LIMIT 5;"
       
    return query
