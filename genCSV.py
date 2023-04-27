import csv
import sqlite3
import mysql.connector
import json
from openpyxl import Workbook
from datetime import datetime

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
   password="123123",
  db="pca001"
)

def gencsv(id):
    mydb = mysql.connector.connect(
      host="127.0.0.1",
      user="root",
      password="123123",
      db="pca001"
    )
    # Query the data
    sql_action_id = "select Max(action_id) from ass_action where client_id =%s and complete = 'Y'"
    action_cursor = mydb.cursor()
    action_cursor.execute(sql_action_id,(id,))
    result_action_id = action_cursor.fetchall()
    print('ACTION_ID: '+ str(result_action_id))
    filter_action_id = str(result_action_id).replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
    
    sql_question = "SELECT q.descr, o.descr FROM answer a JOIN options o ON a.option_id = o.option_id JOIN question q ON o.q_id = q.q_id WHERE a.action_id = %s"
    question_cursor = mydb.cursor()
    question_cursor.execute(sql_question,(filter_action_id,))
    rows = question_cursor.fetchall()
    # Store the data as a JSON object
    # data = {'questions': [row[0] for row in rows]}
    # json_data = json.dumps(data)

    sql_client_name = "SELECT client_name from client where client_id = %s"
    mycursor = mydb.cursor()
    mycursor.execute(sql_client_name,(id,))
    my_client_name = mycursor.fetchall()
    str_my_client_name = str(my_client_name)
    my_client_name_filtered = str_my_client_name.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "").replace("'", "")
    print('resule1: '+str(my_client_name_filtered))


    # # Write the data to a CSV file
    # with open('data.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['Question', 'Option'])
    #     for row in rows:
    #         writer.writerow(row)

    # Write the data to an Excel file
    now = datetime.now()
    formatted = now.strftime('%Y%m%d_%H%M')
    file_name = str(my_client_name_filtered)+'_'+formatted
    print('file_name: '+file_name)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Data'
    ws.append(['Question', 'Option'])
    for row in rows:
        ws.append(row)
    wb.save('C:/report/'+file_name+'.xlsx')

    # Close the database connection
    mydb.close()