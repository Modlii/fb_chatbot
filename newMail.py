import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from datetime import datetime

def send_reminder_email(id):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123123",
        db="pca001"
        )
    mycursor = mydb.cursor()
    # sql = 'SELECT MAX(action_id) FROM ass_action where client_id = %s'
    # sql2 = "select set_id from ass_action where action_id = (SELECT MAX(action_id) FROM ass_action where client_id = %s)"
    sql_q_name = "SELECT set_name FROM question_set where set_id = (select set_id from ass_action where action_id = (SELECT MAX(action_id) FROM ass_action where client_id = %s))"
    mycursor.execute(sql_q_name,(id,))
    myresult = mycursor.fetchall()
    str_myresult = str(myresult)
    myresult_filtered = str_myresult.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
    print('resule1: '+str(myresult_filtered))

    sql_client_name = "SELECT client_name from client where client_id = %s"
    mycursor.execute(sql_client_name,(id,))
    my_client_name = mycursor.fetchall()
    str_my_client_name = str(my_client_name)
    my_client_name_filtered = str_my_client_name.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "")
    print('resule1: '+str(my_client_name_filtered))


    # Set up the email message    
    print('Ready to send email')
    to_address = 'itb303combot@gmail.com'
    from_address = 'itb303combot@gmail.com'
    subject = '['+str(datetime.now())+']Reminder: '+my_client_name_filtered+' has finish an assessment'
    message = 'This is a friendly reminder that '+my_client_name_filtered+' have finish an Assessment of '+myresult_filtered+'. Please contact '+my_client_name_filtered+' as soon as possible.'
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From'] = from_address
    msg['Subject'] = subject
    body = MIMEText(message, 'plain')
    msg.attach(body)

    # Connect to the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'itb303combot@gmail.com'
    smtp_password = 'ailrjdbjjtbzyfix'
    smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
    smtp_conn.starttls()
    smtp_conn.login(smtp_username, smtp_password)

    # Send the message
    smtp_conn.sendmail(from_address, to_address, msg.as_string())

    # Close the connection to the SMTP server
    smtp_conn.quit()
    print("email sent")