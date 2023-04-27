import mysql.connector
import json

class answer:
    def add_Answer(id,msg):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        option_msg = int(msg)
        mycursor = mydb.cursor()
        sql_set_id = "SELECT action_id, set_id, question FROM ass_action WHERE client_id = %s and complete = 'N'"        
        mycursor.execute(sql_set_id, (id,))
        data = mycursor.fetchall()
        json_data = json.dumps(data)
        print('answer data' + str(json_data))

        for row in data:
            action_id = row[0]
            set_id = row[1]
            question = row[2]
        print('action_id+set_id+question: '+str(action_id)+' : '+str(set_id)+' : '+str(question))

        #sql = "INSERT INTO answer (action_id, option_id, client_id) SELECT aa.action_id, o.option_id, %s FROM ass_action aa INNER JOIN option o ON aa.set_id = o.set_id WHERE aa.client_id = %s AND aa.complete = 'N' AND o.display_number = %s"

        option_id_sql = "select option_id from options where q_id = %s and display_number = %s"
        mycursor.execute(option_id_sql, (question,option_msg,))
        option_id = mycursor.fetchall()
        str_check_record = str(option_id)
        check_option_id = int(str_check_record.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", ""))
        sql = "insert into answer (action_id,option_id,client_id) value (%s,%s,%s)"
        mycursor.execute(sql, (action_id,check_option_id,id,))
        mydb.commit()
        mycursor.close()
        print('New Answer created')