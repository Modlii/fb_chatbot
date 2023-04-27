import mysql.connector
import json

class action:
    def createAction(id,set_id):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        mycursor = mydb.cursor()
        q_id = "SELECT MIN(q_id) FROM q_set_mapping WHERE set_id = %s"
        mycursor.execute(q_id, (set_id,))
        myresult = mycursor.fetchall()
        filter_myresult = str(myresult).replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
        qid = int(filter_myresult)
        sql = "insert into ass_action (client_id,set_id,complete,chatHistory,question) value (%s,%s,'N',0,%s)"
        mycursor.execute(sql, (id,set_id,qid))
        mydb.commit()
        mycursor.close()
        print('Action created')
    
    def updateAction(id):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        mycursor = mydb.cursor()
        sql_next_q = "UPDATE ass_action SET question = (SELECT next_q FROM q_set_mapping WHERE q_id = ass_action.question) WHERE client_id = %s and complete = 'N'"
        mycursor.execute(sql_next_q,(id,))
        mydb.commit()
        sql_update_chatHistory = "UPDATE ass_action SET chatHistory = 1 WHERE client_id = %s and complete = 'N'"
        mycursor.execute(sql_update_chatHistory,(id,))
        mydb.commit()
        print('updateAction done: ')
        mydb.close()

    
    def forceEndndAction(id):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        mycursor = mydb.cursor()
        sql_check_record = "SELECT COUNT(*) FROM ass_action WHERE client_id = %s and complete = 'N'"
        mycursor.execute(sql_check_record, (id,))
        check_record = mycursor.fetchall()
        str_check_record = str(check_record)
        check_record_filter = str_check_record.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
        print('check check_record: '+check_record_filter)
        if check_record_filter == '1':            
            sql = "Update ass_action Set complete='E' where client_id = %s and complete = 'N'"
            mycursor.execute(sql, (id,))
            mydb.commit()
            mycursor.close()
            print('Forced End')
        else:
            print('Nothing to Force End')
    
    def endndAction(id):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        mycursor = mydb.cursor()
        sql = "Update ass_action Set complete = 'Y' where client_id = %s and complete = 'N'"
        mycursor.execute(sql, (id,))
        mydb.commit()
        mycursor.close()
        print('Finished assessment')

    def check_history(id):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        mycursor = mydb.cursor()
        sql = "select chatHistory from ass_action where client_id = %s and complete = 'N'"
        mycursor.execute(sql, (id,))
        myresult = mycursor.fetchall()
        str_myresult = str(myresult)
        myresult_filtered = str_myresult.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
        chatHistory = int(myresult_filtered)
        print('resule1: '+str(chatHistory))
        mycursor.close()
        print('get chatHistory')
        return chatHistory