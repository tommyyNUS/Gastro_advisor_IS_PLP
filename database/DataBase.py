# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 20:25:52 2020

@author: Paul S.R
"""

import sqlite3
from sqlite3 import Error
import pandas as pd

class DataBase:
    # tasks table
    create_master_table_sql = ''' CREATE TABLE IF NOT EXISTS restaurant (
                                    	id integer PRIMARY KEY,
                                    	rest_name text NOT NULL,
                                    	rest_address text,
                                        rest_region text,
                                        rest_type text,
                                        rest_food_type text,
                                        rest_food_rating real,
                                        rest_srvc_rating real,
                                        rest_ambi_rating real,
                                        rest_prce_rating real,
                                        rest_rating real,
                                        w_fs_rating real,
                                        w_fa_rating real,
                                        w_fp_rating real,
                                        w_fsa_rating real,
                                        w_fsp_rating real,
                                        w_fap_rating real,
                                        w_rest_rating real
                                    ); '''
    
    SQLITE_CONN = None
    
    def __init__(self):
        try:
            if self.SQLITE_CONN is None:
                self.SQLITE_CONN = self.connect_to_db()
        except Error as e:
            print("ERROR while creating connection", e)
    
    def destroy(self):
        if (self.SQLITE_CONN):
            self.SQLITE_CONN.close()
            print("The SQLite connection is closed")
    
    def connect_to_db(self, path=""):
        try:
            
            if path == "":
                path = 'gastrotommy.db'
                
            sqliteConn = sqlite3.connect(path)
            cursor = sqliteConn.cursor()
            print("Database created and Successfully Connected to SQLite")
        
            sqlite_select_Query = "select sqlite_version();"
            cursor.execute(sqlite_select_Query)
            record = cursor.fetchall()
            print("SQLite Database Version is: ", record)
            cursor.close()
        
        except Error as e:
            print("Error while connecting to sqlite", e)
    
        return sqliteConn        
    
    def create_tables(self):
        try:
            c = self.SQLITE_CONN.cursor()
            c.execute(self.create_master_table_sql)
        except Error as e:
            print("ERROR while creating table", e)
    
    def empty_table(self):
        sql = ''' DELETE FROM restaurant; '''
        try:
            c = self.SQLITE_CONN.cursor()
            c.execute(sql)
            print("Table restaurant is empty now.")
        except Error as e:
            print("ERROR while emptying table", e)
    
    def insert_records(self, record):
        sql = ''' INSERT INTO restaurant (id, 
        rest_name,rest_address,rest_region,rest_type,rest_food_type,
        rest_food_rating,rest_srvc_rating,rest_ambi_rating,
        rest_prce_rating, rest_rating,
        w_fs_rating, w_fa_rating, w_fp_rating,
        w_fsa_rating, w_fsp_rating, w_fap_rating,
        w_rest_rating)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); '''
        
        cur = self.SQLITE_CONN.cursor()
        cur.execute(sql, record)
        self.SQLITE_CONN.commit()
    
        return cur.lastrowid

    def fetch_restaurants_by_sql(self, sql):
        cur = self.SQLITE_CONN
        #cur.execute(sql)
        #rows = cur.fetchall()
        rows = pd.read_sql_query(sql,cur)
        return rows

    def fetch_restaurant_by_name(self, rname):
        sql = " SELECT * FROM restaurant WHERE rest_name = ? ; "
        
        cur = self.SQLITE_CONN.cursor()
        cur.execute(sql, [rname])
        rows = cur.fetchall()
    
        return rows

    def fetch_restaurant_by_type(self, rtype):
        sql = " SELECT * FROM restaurant WHERE rest_type LIKE ? ;"
        srch_str = '%'+rtype+'%'
        
        cur = self.SQLITE_CONN.cursor()
        #print("sql", sql, srch_str)
        cur.execute(sql, [srch_str])
        rows = cur.fetchall()
    
        return rows

    def fetch_restaurant_by_food_type(self, ftype):
        sql = " SELECT * FROM restaurant WHERE rest_food_type LIKE ? ;"
        srch_str = '%'+ftype+'%'
        
        cur = self.SQLITE_CONN.cursor()
        #print("sql", sql, srch_str)
        cur.execute(sql, [srch_str])
        rows = cur.fetchall()
    
        return rows

    def fetch_restaurant_by_region(self, region):
        sql = " SELECT * FROM restaurant WHERE rest_region = ? ;"
        
        cur = self.SQLITE_CONN.cursor()
        #print("sql", sql, srch_str)
        cur.execute(sql, [region])
        rows = cur.fetchall()
    
        return rows

    def fetch_topx_by_food_rating(self, x):
        sql = " SELECT * FROM restaurant ORDER BY rest_food_rating DESC LIMIT ?;"
        
        cur = self.SQLITE_CONN.cursor()
        #print("sql", sql, srch_str)
        cur.execute(sql, [x])
        rows = cur.fetchall()
    
        return rows

    def fetch_topx_by_ambi_rating(self, x):
        sql = " SELECT * FROM restaurant ORDER BY rest_ambi_rating DESC LIMIT ?;"
        
        cur = self.SQLITE_CONN.cursor()
        #print("sql", sql, srch_str)
        cur.execute(sql, [x])
        rows = cur.fetchall()
    
        return rows
    
    def fetch_topx_by_service_rating(self, x):
        sql = " SELECT * FROM restaurant ORDER BY rest_srvc_rating DESC LIMIT ?;"
        
        cur = self.SQLITE_CONN.cursor()
        #print("sql", sql, srch_str)
        cur.execute(sql, [x])
        rows = cur.fetchall()
    
        return rows
    
    def fetch_topx_by_price_rating(self, x):
        sql = " SELECT * FROM restaurant ORDER BY rest_prce_rating DESC LIMIT ?;"
        
        cur = self.SQLITE_CONN.cursor()
        #print("sql", sql, srch_str)
        cur.execute(sql, [x])
        rows = cur.fetchall()
    
        return rows
    
    def fetch_topx_by_overall_rating(self, x):
        sql = " SELECT * FROM restaurant ORDER BY rest_rating DESC LIMIT ?;"
        
        cur = self.SQLITE_CONN.cursor()
        #print("sql", sql, srch_str)
        cur.execute(sql, [x])
        rows = cur.fetchall()
    
        return rows

########################################
########################################

if __name__ == '__main__':
    
    db = None
    try:
        db = DataBase()
        #db.create_tables()
                
        """
        rest = (1, 'Ichiban Sushi', '123 Orchard Road', 'Central', 
                'Japaneese,Traditional', 'Sushi#Sake#Saba Hot Plate',
                9.5, 7.0, 6.0, 5.0, 9.0)
        db.insert_records(rest)
        rest = (2, 'McDonalds', '123 Ang Mo Kio', 'North', 
                'FastFood,Modern', 'Burger#Chicken',
                8.5, 7.5, 6.0, 5.0, 8.0)
        db.insert_records(rest)
        rest = (3, 'PizzaHut', '123 Suntec City', 'Central', 
                'FastFood,Modern', 'Pizza#Chicken',
                8.0, 8.5, 6.0, 5.0, 8.0)
        db.insert_records(rest)
        rest = (4, 'Soup Spoon', '123 Sunte City', 'Central', 
                'Soup&Salad', 'Soup#Salad#Bun#Mushroom',
                7.5, 6.5, 6.0, 5.0, 8.5)
        db.insert_records(rest)
        rest = (5, 'Anjappar Chettinaad Restaurant', '123 Little india', 'South', 
                'Indian,Traditional', 'Briyani#Prata#Tandoori Chicken',
                9.0, 7.0, 6.0, 5.0, 9.0)
        db.insert_records(rest)
        
        print("")
        print("\nfetch_restaurant_by_name:ABC", db.fetch_restaurant_by_name('ABC'))
        print("\nfetch_restaurant_by_name:Ichiban Sushi", db.fetch_restaurant_by_name('Ichiban Sushi'))
        print("\nfetch_restaurant_by_type:Japaneese", db.fetch_restaurant_by_type('Japaneese'))
        print("\nfetch_restaurant_by_food_type:Briyani", db.fetch_restaurant_by_food_type('Briyani'))
        print("\nfetch_restaurant_by_region:North", db.fetch_restaurant_by_region('North'))
        print("\nfetch_topx_by_food_rating:3", db.fetch_topx_by_food_rating(3))
        print("\nfetch_topx_by_overall_rating:3", db.fetch_topx_by_overall_rating(3))
        print("")
        """
        
        """
        sql = "SELECT * FROM restaurant WHERE id=1"
        print("\nfetch_rest_by_overall_custom_sql", db.fetch_restaurants_by_sql(sql))
        """
        
    except:
        print("An exception occurred")
        raise
        
    finally:
        if(db):
            db.destroy()
