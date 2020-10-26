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
            
            # overall/average restaurant score
            rest_rating = (f_rating + s_rating + a_rating + p_rating)/4
            print("new rest_rating:", rest_rating)
            
            # scores for bi-aspect queries
            w_fs_rating = (f_rating*0.3 + s_rating*0.7)
            w_fa_rating = (f_rating*0.3 + a_rating*0.7)
            w_fp_rating = (f_rating*0.3 + p_rating*0.7)
            print("new bi-scores:{},{},{}".format(w_fs_rating,w_fa_rating,w_fp_rating))
            
            # scores for tri-aspect queries
            w_fsa_rating = (f_rating*0.4 + s_rating*0.3 + a_rating*0.3)
            w_fsp_rating = (f_rating*0.4 + s_rating*0.3 + p_rating*0.3)
            w_fap_rating = (f_rating*0.4 + a_rating*0.3 + p_rating*0.3)
            print("new tri-scores:{},{},{}".format(w_fsa_rating,w_fsp_rating,w_fap_rating))
            
            # weighted overall restaurant score
            w_rest_rating = (f_rating*0.6 + s_rating*0.2 + a_rating*0.1 + p_rating*0.1)
            print("new w_rest_rating:", w_rest_rating)
            
            updt_sql = '''  UPDATE restaurant 
                            SET w_fs_rating=?, w_fa_rating=?, w_fp_rating=?, 
                            w_fsa_rating=?, w_fsp_rating=?, w_fap_rating=?, 
                            rest_rating=?, w_rest_rating=? 
                            WHERE id=?; '''
            cur = conn.cursor()
            cur.execute(updt_sql, [str(w_fs_rating),str(w_fa_rating),str(w_fp_rating),
                                   str(w_fsa_rating),str(w_fsp_rating),str(w_fap_rating),
                                   str(rest_rating), str(w_rest_rating),
                                   str(i)])
            conn.commit()
            print("Update is done for ", i)
            
    except:
        print("\n<<< An exception occurred >>> @index") 
        raise
        
    finally:
        if(db):
            db.destroy()
            
#8, 44, 75, 91, 92, 126