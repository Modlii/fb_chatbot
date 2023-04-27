import mysql.connector
import pymysql
import json

class getOption:
    def get_option(qid):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        mycursor = mydb.cursor()
        sql = "select descr from options where q_id = %s"
        mycursor.execute(sql,(qid,))
        rows = mycursor.fetchall()

        option_values = []
        for row in rows:
            option_values.append(row[0])

        result = {'Option': option_values}

        json_result = json.dumps(result)

        print('get_option result: '+str(json_result))
        mydb.close()

        return json_result
    
    def get_option_list(qid):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        mycursor = mydb.cursor()
        sql = "select count(descr) from options where q_id = %s"
        mycursor.execute(sql,(qid,))
        result = mycursor.fetchall()
        str_result = str(result)
        result_filter = str_result.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
        
        mydb.close()

        return int(result_filter)
    
    def count_option(qid):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        mycursor = mydb.cursor()
        sql = "select count(descr) from options where q_id = %s"
        mycursor.execute(sql,(qid,))
        result = mycursor.fetchall()
        str_result = str(result)
        result_filter = str_result.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
        
        mydb.close()

        return int(result_filter)