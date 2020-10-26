# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 20:47:39 2020

@author: Paul S.R
"""

import sys
import pandas as pd
import statistics
from model.predict_sentiment import BertSentiment
from database.DataBase import DataBase

if __name__ == "__main__":
    
    # Prompt user before start overriding DB
    _in1 = input("Do you really want to override the current DB? Enter yes/no: ")
    if _in1.lower() == 'yes':
        _in2 = input("It will take a day.. are you sure? Enter yes/no: ")
        if _in2.lower() == 'yes':
            print("Starting to re-populate DB.")
        else:
            print("Bye!")
            sys.exit()
    else:
        print("Bye!")
        sys.exit()
        
    db = None
    _i = None
    try:
        # create BERT model for Sentiment Analysis
        bert_sentiment = BertSentiment()
        
        # create DataBase object
        db = DataBase()
        
        # empty table before (re)populating data
        db.empty_table()
        
        # read the file with reviews and respective aspects
        df = pd.read_csv('./data/reviews_with_aspects_full.csv', engine='python')
        #df = pd.read_csv('./data/aspects-top55k.csv', engine='python')
        #df = pd.read_csv('./data/test.csv', engine='python')
        df = df.reset_index(drop=True)
        print(df.shape)

        df = df.iloc[55800:len(df), :]
        
        df = df.reset_index(drop=True)
        print(df.shape)
        
        df.loc[len(df)] = '0' # insert dummy row to persist last restaurent
        print(df.shape)
        print(df.tail(2))

        row_id = 49 
        rest_name_last = None
        f_rating_arr = []
        s_rating_arr = []
        a_rating_arr = []
        p_rating_arr = []
        
        for i, row in df.iterrows():
            #print('Row:',row)
            _i = i
            if i%1000 == 0:
                print("Processing review id", i)
            
            rest_name = str(row['restaurant']).strip()
            #print("rest_name-", rest_name)
            
            # If a new restaturant found
            if (rest_name_last != None and rest_name != rest_name_last):
                
                print("Found new restaurant, persisting data of the previous restaurant:", rest_name_last)
                
                # calculate mean probabilities
                f_rating = 0.0 if len(f_rating_arr) == 0 else statistics.mean(f_rating_arr)
                s_rating = 0.0 if len(s_rating_arr) == 0 else statistics.mean(s_rating_arr)
                a_rating = 0.0 if len(a_rating_arr) == 0 else statistics.mean(a_rating_arr)
                p_rating = 0.0 if len(p_rating_arr) == 0 else statistics.mean(p_rating_arr)
                
                # overall/average restaurant score
                rest_rating = (f_rating + s_rating + a_rating + p_rating)/4
                
                # scores for bi-aspect queries
                w_fs_rating = (f_rating*0.7 + s_rating*0.3) # e.g. f=0.9, s=0.5 --> fs=0.78
                w_fa_rating = (f_rating*0.7 + a_rating*0.3)
                w_fp_rating = (f_rating*0.7 + p_rating*0.3)
                
                # scores for tri-aspect queries
                w_fsa_rating = (f_rating*0.6 + s_rating*0.2 + a_rating*0.2) # e.g. f=0.9, s=0.5, a=0.8 --> fsa=0.8
                w_fsp_rating = (f_rating*0.6 + s_rating*0.2 + p_rating*0.2)
                w_fap_rating = (f_rating*0.6 + a_rating*0.2 + p_rating*0.2)
                
                # weighted overall restaurant score
                w_rest_rating = (f_rating*0.6 + s_rating*0.2 + a_rating*0.1 + p_rating*0.1)
                
                l_row = df.iloc[i-1]
                
                # persist the record of the last calculated restaurant
                record = (row_id, l_row['restaurant'], l_row['address'], l_row['region'], 
                    l_row['type'], l_row['food_subtype'],
                    f_rating, s_rating, a_rating, p_rating, rest_rating, 
                    w_fs_rating, w_fa_rating, w_fp_rating,
                    w_fsa_rating, w_fsp_rating, w_fap_rating,
                    w_rest_rating)
                
                print("inserting record:", record)
            
                last_row_id = db.insert_records(record)
                
                # calcualte next primary key using last_row_id
                print('last_row_id:', last_row_id)
                row_id = last_row_id+1
                
                # reset probability arrays
                f_rating_arr = []
                s_rating_arr = []
                a_rating_arr = []
                p_rating_arr = []
                
                print("End data persistance\n")
            
            rest_name_last = rest_name
            
            # run BERT to predict the sentiment score
            try:
                review = row['Review']
                prob = bert_sentiment.classify_sentiment(review)
            except TypeError:
                print("<<< Error while predicting sentiment, skip review >>>", i, rest_name, review, "\n")
                continue
            
            # Set individual sentiment probabilities
            aspect = str(row['aspect']).strip().lower()
            
            #print(review, "::", aspect, "::", prob)
            
            if aspect == 'food':
                f_rating_arr.append(prob)
            elif aspect == 'service':
                s_rating_arr.append(prob)
            elif aspect == 'ambience':
                a_rating_arr.append(prob)
            elif aspect == 'price':
                p_rating_arr.append(prob)
            else:
                print("No aspect found, call Tommy immediately")

    except:
        print("\n<<< An exception occurred >>> @index", _i) 
        raise
        
    finally:
        if(db):
            db.destroy()
