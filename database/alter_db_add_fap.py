# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 21:05:15 2020

@author: rajpaul
"""

from database.DataBase import DataBase

if __name__ == "__main__":
    
    db = None
    try:
        
        # create DataBase object
        db = DataBase()
        conn = db.connect_to_db()
        
        # select max record id
        id_sql = " SELECT MAX(id) FROM restaurant; "
        
        cur = conn.cursor()
        cur.execute(id_sql)
        rows = cur.fetchall()
        
        last_row_id = rows[0][0]
        print("last_row_id:", last_row_id)
        
        for i in range(1,last_row_id+1):
            print("updating row with id:",i)
            
            rest_sql = " SELECT rest_food_rating,rest_ambi_rating,rest_prce_rating FROM restaurant where id=?; "
        
            cur = conn.cursor()
            cur.execute(rest_sql,[str(i)])
            rows = cur.fetchall()
            print("rows:", rows)
        
            f_rating,a_rating,p_rating = rows[0]
            print("rows:", f_rating,a_rating,p_rating)
            
            w_fap_rating = (f_rating*0.6 + a_rating*0.2 + p_rating*0.2)
            print("fap:", w_fap_rating)
            
            updt_sql = " UPDATE restaurant SET w_fap_rating=? WHERE id=?; "
            cur = conn.cursor()
            cur.execute(updt_sql, [str(w_fap_rating),str(i)])
            conn.commit()
            print("Update is done for ", i)
            
    except:
        print("\n<<< An exception occurred >>> @index") 
        raise
        
    finally:
        if(db):
            db.destroy()
            
