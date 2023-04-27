import mysql.connector
from getQuestion import *
from addNewClient import *
from goCreateNewClient import *

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="123123",
  db="pca001"
)

class getHistory:
    def gethistory(recipient_id, user_name):
      mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
      )
      id = recipient_id.strip()
      print("THIS IS ID in HISTORY: x"+id+'x')
      
      
      check_client_id = "SELECT count(1) FROM client WHERE client_id = %s"
      #check_client_id = "SELECT count(1) FROM client WHERE client_id = '6344868388898413'"
      check_id_cursor = mydb.cursor()
      check_id_cursor.execute(check_client_id,(id,))
      check_id = check_id_cursor.fetchall()
      str_check_id = str(check_id)
      print('This is str_chceck_id: x'+str_check_id+'x')
      check_id_filtered = str_check_id.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
      print('This is check_id: '+check_id_filtered)
      if check_id_filtered =='0':
        print('go create')
        goCreateNewClient.sss(id,user_name)
        mydb.close()
        return 'New'
      # else:
      #   #indicator = getHistory.findAcion(id)
      #   print('OK')
      #   return 'indicator'

    #def findAcion(id):
      mycursor = mydb.cursor()
      sql = "SELECT COUNT(*) FROM ass_action WHERE client_id = %s and complete='N'"
      mycursor.execute(sql,(id,))
      myresult = mycursor.fetchall()
      str_myresult = str(myresult)
      myresult_filter = str_myresult.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
      print('check action: '+myresult_filter)

      sql_chatHistory = "SELECT COUNT(*) FROM ass_action WHERE client_id = %s and complete='N' and chatHistory = 0"
      mycursor.execute(sql_chatHistory,(id,))
      myresult_chatHistory = mycursor.fetchall()
      str_myresult_chatHistory = str(myresult_chatHistory)
      myresult_chatHistory_filter = str_myresult_chatHistory.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
      print('check _chatHistory: '+myresult_chatHistory_filter)

      if myresult_chatHistory_filter == '1':
         mydb.close()
         print('null chatHistory')
         return 'null chatHistory'
      elif myresult_filter =='0':
          mydb.close()
          print('null action')
          return 'null action'
      elif myresult_filter == '1':
         print('cont')
         mydb.close()
         return 'cont'
      else:
         print('con_ans')
         return 'con_ans'


      # get_action_id = "SELECT MAX(action_id) FROM ass_action where client_id ='%a'"
      # action_cursor = mydb.cursor()
      # action_cursor.execute(get_action_id(id))
      # action_id = action_cursor.fetchall()
      # print('ACTION_ID: '+ action_id)




      # if myresult is not None:
      #   return 'hi'
      # else:
      #    return 'nothing in history'

