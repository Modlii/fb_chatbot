import mysql.connector
from getOption import getOption
import json

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="123123",
  db="pca001"
)

class getQuestion:
    def aaa(set_id):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        set = int(set_id)
        print("this is msg10:"+str(set))
        #if msg == "DIU":
        if set is not None:
            mycursor = mydb.cursor()
            sql_q_id = "SELECT q_id FROM q_set_mapping where set_id = %s order by q_id ASC limit 1"
            mycursor.execute(sql_q_id,(set,))
            myresult = mycursor.fetchall()
            str_myresult = str(myresult)
            myresult_filtered = str_myresult.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
            qid = int(myresult_filtered)
            print('resule1: '+str(qid))

            return_text = getQuestion.get_question(qid)
            option_str = getOption.get_option(qid)
            question_obj = {'Question': return_text}
            option_obj = json.loads(option_str)
            question_obj['Option'] = option_obj['Option']
            json_result = json.dumps(question_obj)
            print('aaa.getQuestion return text: x'+return_text+'x')
            print('aaa.conQuestion return text: x'+str(json_result)+'x')
            # sql = "SELECT descr FROM question where q_id = %s"
            # mycursor.execute(sql,(qid,))
            # q_result = mycursor.fetchall()
            # #print('My resault: '+str(myresult))

            # str_q_result = str(q_result)
            # q_result_filtered = str_q_result.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
            # print('This is check_id: '+q_result_filtered)


            # for row in myresult:
            #     print("THIS IS THE RESAULT: "+str(row[0]))
            #     msg = row[0]
            #     mycursor.close()
            mydb.close()
            return json_result
        else:
            return 'nothing'
    
    def conQuestion(id):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        sql_getLastAction = "select set_id, question from ass_action where complete='N' and client_id =%s"
        mycursor = mydb.cursor()
        mycursor.execute(sql_getLastAction,(id,))
        myresult = mycursor.fetchall()
        rows = []
        for row in myresult:
            rows.append({'set_id': row[0], 'question': row[1]})
            set_id  = int(row[0])
            print('conQuestion set_id: x'+str(set_id)+'x')
            question = int(row[1])
            print('conQuestion question: x'+str(question)+'x')


        # for row1 in myresult:
        #         print("THIS IS THE RESAULT: "+str(row1[0]))
        #         latestOption = int(row1[0])

        # Find next_q        
        sql_next_q = "select next_q from q_set_mapping where set_id = %s and q_id = %s"
        mycursor.execute(sql_next_q,(int(set_id), int(question)))
        myresult = mycursor.fetchall()
        print('Find next_q result: x'+str(myresult)+'x')
        filter_myresult = str(myresult).replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
        next_q = int(filter_myresult)
        if next_q == 0:
            return 'end'

        # get question
        question = getQuestion.get_question(next_q)
        option_str = getOption.get_option(next_q)
        question_obj = {'Question': question}
        option_obj = json.loads(option_str)
        question_obj['Option'] = option_obj['Option']
        json_result = json.dumps(question_obj)
        print('conQuestion return text: x'+str(json_result)+'x')
        mydb.close()
        return json_result
    
    def get_question(q_id):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )

        mycursor = mydb.cursor()
        sql = "SELECT descr FROM question where q_id = %s"
        mycursor.execute(sql,(q_id,))
        q_result = mycursor.fetchall()
        #print('My resault: '+str(myresult))

        str_q_result = str(q_result)
        q_result_filtered = str_q_result.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
        print('This is q_result_filtered: '+q_result_filtered)
        mydb.close()
        return q_result_filtered

    def checkCurrentQuestion(id):
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
        print('checkCurrentQuestion(id): '+id)
        sql_getLastAction = "select question from ass_action where complete='N' and client_id =%s"
        mycursor = mydb.cursor()
        mycursor.execute(sql_getLastAction,(str(id),))
        myresult = mycursor.fetchall()
        qid = myresult
        str_qid_result = str(qid)
        qid_result_filtered = str_qid_result.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
        print('checkCurrentQuestion qid: '+str(qid))

       # get question
        question = getQuestion.get_question(qid_result_filtered)
        option_str = getOption.get_option(qid_result_filtered)
        question_obj = {'Question': question}
        option_obj = json.loads(option_str)
        question_obj['Option'] = option_obj['Option']
        json_result = json.dumps(question_obj)
        print('conQuestion return text: x'+str(json_result)+'x')
        mydb.close()
        return json_result
