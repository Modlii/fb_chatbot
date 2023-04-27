import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="123123",
  db="pca001"
)

class goCreateNewClient:
    def sss(recipient_id,user_name):
        id = recipient_id
        print("this is new client id:" + id)
        sql_input_client = "INSERT INTO client (client_id,client_name) VALUES (%s,%s)"
        input_cursor = mydb.cursor()
        input_cursor.execute(sql_input_client, (id,user_name,))
        mydb.commit()  # commit the changes to the database
        input_cursor.close()
        print('create done')