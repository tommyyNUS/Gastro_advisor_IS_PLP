# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 21:05:15 2020

@author: rajpaul
"""
import sys
from database.DataBase import DataBase

if __name__ == "__main__":
    
    """
    # Prompt user before re-scoring DB
    _in1 = input("Do you really want to re-score the current DB? Enter yes/no: ")
    if _in1.lower() == 'yes':
        print("Starting to re-score DB.")
    else:
        print("Bye!")
        sys.exit()
    """
    db = None
    try:
        
        # create DataBase object
        db = DataBase('C:\\NUS_ISS_MTech\Year 2\Semester 2 - Practical Natural Language Processing\PLP CA\database\gastrotommy_v3.db')
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
            
            rest_sql = " SELECT rest_food_rating,rest_srvc_rating,rest_ambi_rating,rest_prce_rating FROM restaurant where id=?; "
        
            cur = conn.cursor()
            cur.execute(rest_sql,[str(i)])
            rows = cur.fetchall()
            print("rows:", rows)
            
            f_rating,s_rating,a_rating,p_rating = rows[0]

            zero_sql = " UPDATE restaurant SET " 
            if f_rating == 0.0:
                zero_sql = zero_sql + "rest_food_rating=0.5, "
            if s_rating == 0.0:
                zero_sql = zero_sql + "rest_srvc_rating=0.5, "
            if a_rating == 0.0:
                zero_sql = zero_sql + "rest_ambi_rating=0.5, "
            if p_rating == 0.0:
                zero_sql = zero_sql + "rest_prce_rating=0.5, "
            
            zero_sql = zero_sql.rstrip().rstrip(',') + " WHERE id=?; "
            
            print("0 update sql:", zero_sql)
            if '0.5' in zero_sql:
                print("updating 0.0 to 0.5")
                cur = conn.cursor()
                cur.execute(zero_sql, [str(i)])
                conn.commit()
            
            sql = ""

    except:
        print("\n<<< An exception occurred >>> @index") 
        raise
        
    finally:
        if(db):
            db.destroy()
