from logging import log
import os, sys, mysql.connector
import requests
from flask import Flask, request
from pymessenger import Bot
from getQuestion import *
from getHistory import *
from addNewClient import *
from mysql.connector import (connection)
import json
from getOption import *
from action import *
from anwser import *
from newMail import *
from genCSV import *

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'myCustomToken1234'#BTqkaSWoqAUiUd2qIsxoECUX5AAD8mz1MxNRx1rAoCM= <paste your verify token here>
PAGE_ACCESS_TOKEN = "EAAi5Ow5Ol24BABZCx9cRVltPZA7sKgT2K9fPiFeZAqrEaH9pSikMLTsuIPX5C35FVNshWHmd7A4AW2rOxKS2QGRM3FZAxW0r0uZAb4weddssZAKcjKaFZBxZC2C2uDWPZApP2kuSj3wJ8BwZA6rw83KYMvZBeLFTd3ZANGh6CytLmplg6TMASyLyXCpYanGIQWXOo6EZD"# paste your page access token here>
bot = Bot(PAGE_ACCESS_TOKEN)

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
   password="123123",
  db="pca001"
)

@app.route('/webhook', methods=['GET'])
def verify():
 # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'myCustomToken1234':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200
@app.route('/webhook', methods=['POST'])

def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
         for entry in data['entry']:
             #sender_id = data['entry'][0]['messaging'][0]['sender']['id']
            entry_id = data['entry'][0]['id']
            str_entry_id = str(entry_id)
            print('This is entry_id: '+ entry_id)
            #print('----------------------------------------------------------------------------------------------------------------------------------------')
             #print("THIS IS sender_id: "+sender_id)

            
            for messaging_event in entry['messaging']:
                 sender_id = ''
                 sender_id.strip()
                 flag1 = ''
                 msg = ''
                #  messaging_text = messaging_event['message']['text']
                #  msg  = messaging_text
                 if 'entry' in data and data['entry'] and 'messaging' in data['entry'][0] and data['entry'][0]['messaging'] and 'message' in data['entry'][0]['messaging'][0] and data['entry'][0]['messaging'][0]['message'] and 'text' in data['entry'][0]['messaging'][0]['message']:
                     flag1='1'
                     messaging_text = messaging_event['message']['text']
                     msg  = messaging_text
                     if str_entry_id != str(messaging_event['sender']['id']):
                        sender_id = messaging_event['sender']['id']
                        sender_id.strip()
                        print('they are not same')
                     if sender_id is not None:
                        store_sender_id = sender_id
                        store_sender_id.strip()
                        print("THIS IS sender_id: "+store_sender_id)
                        recipient_id = messaging_event['recipient']['id']
                        break
                 else:
                     flag1='0'
                     sender_id = messaging_event['sender']['id']
                     sender_id.strip()
                     print("werfwe: "+str(msg))
                     break

                 #print("THIS IS msg_TOP: "+msg)
                 # IDs
 
    # #ID action verfication
    # #action_sataus = getHistory.gethistory(sender_id)

    if msg is not None and flag1=='1' and sender_id.strip() !='':
         #messaging_text = messaging_event['message']['text']
         print("THIS IS messaging_text: "+msg)
         endpoint = 'https://graph.facebook.com/v12.0/' + store_sender_id
         params = {'fields': 'name', 'access_token': PAGE_ACCESS_TOKEN}
         response = requests.get(endpoint, params=params)
         data = json.loads(response.text)
         print('response.data: '+str(data))
         user_name = data['name']
         print('User name:', user_name)
        # msg = messaging_text
         print('*******************************************************************************************************************************************')
         print("THIS IS store_sender_id before go history:x"+store_sender_id+'x')
        # Check force to end the Assessment
         if msg.lower() == 'end assessment':
            action.forceEndndAction(store_sender_id)
            bot.send_text_message(store_sender_id, 'The assessment is forced to end\nThank you')
            sys.stdout.flush()
            return "ok", 200
        # sender id validation, return an indicator
         indicator = getHistory.gethistory(store_sender_id,user_name)
         print('THIS IS indicator: '+indicator)

         if indicator =='null action':
             print("get in indicator =='null action'")
             if msg is not None and msg.isdigit():
             #if msg.lower() == 'quit smoking' or msg == '1':
                 print("THIS IS msg1: "+msg)
                 Question = str(getQuestion.aaa(msg))
                 str_getQuestion = json.loads(Question)
                 action.createAction(store_sender_id,int(msg))

                # Question
                 question_text = str(str_getQuestion["Question"])
                 bot.send_text_message(store_sender_id, question_text)

                # Option
                 option_list = str_getQuestion["Option"]
                 option_count = len(option_list)
                 option_numbers = [str(i+1) for i in range(option_count)]
                 option_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(option_list)])
                 bot.send_text_message(store_sender_id, option_text)
                 bot.send_text_message(store_sender_id, f"Please choose an option (1-{option_count}):")
                 #bot.send_text_message(store_sender_id,f"Type End Assessment")
                # bot.send_text_message(store_sender_id, return_text)
                 sys.stdout.flush()
                 return "ok", 200
            #  elif msg == 'Back Pain':
            #      return_text = getQuestion.aaa(msg)
            #      bot.send_text_message(store_sender_id, return_text)
             else:
                 #bot.send_text_message(store_sender_id, 'Sorry, your input is invalided.\nPlease input again.')
                 bot.send_text_message(store_sender_id, "What can I help you with?\nSelect an option\n(Type the option below)\n\n1. Quit Smoking\n2. NRT Usage Assessment")
                 sys.stdout.flush()
                 return "ok", 200
             
         elif indicator == 'cont':
             #check last option list
             current_option = getQuestion.checkCurrentQuestion(store_sender_id)
             str_option = json.loads(current_option)
             currentQuestion = str_option["Question"]
             current_option_list = str_option["Option"]
             current_option_count = len(current_option_list)
             current_option_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(current_option_list)])             
            #  option_numbers = [str(i+1) for i in range(option_count)]
            #  option_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(option_list)])
            #  chatHistory = action.check_history(store_sender_id)
            #  if chatHistory==1:
             if msg > str(current_option_count) and msg.isdigit():
                    bot.send_text_message(store_sender_id, currentQuestion)
                    bot.send_text_message(store_sender_id, current_option_text)
                    bot.send_text_message(store_sender_id, f"Please choose an option (1-{current_option_count}):")
                    sys.stdout.flush()
                    return "ok", 200
             elif '1' <= msg <= str(current_option_count):
                    return_text = getQuestion.conQuestion(store_sender_id)
                    answer.add_Answer(store_sender_id,msg)
                    action.updateAction(store_sender_id)

                    if return_text == 'end':
                        bot.send_text_message(store_sender_id, 'This is the end of Assessment\nOur staff will contact You soon')
                        action.endndAction(store_sender_id)
                        print("server go mail")
                        send_reminder_email(store_sender_id)
                        print('server mail done')
                        print("server go genCSV")
                        gencsv(store_sender_id)
                        print('server genCSV done')
                        sys.stdout.flush()
                        return "ok", 200
                    
                    print('cont return text:'+return_text)
                    str_return_text = json.loads(return_text)
                    # Question
                    question_text = str_return_text["Question"]
                    bot.send_text_message(store_sender_id, question_text)

                    # Option
                    option_list = str_return_text["Option"]
                    option_count = len(option_list)
                    option_numbers = [str(i+1) for i in range(option_count)]
                    option_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(option_list)])
                    bot.send_text_message(store_sender_id, option_text)
                    bot.send_text_message(store_sender_id, f"Please choose an option (1-{option_count}):")
                    sys.stdout.flush()
                    return "ok", 200
             else:
                currentQuestion = str_option["Question"]
                bot.send_text_message(store_sender_id, currentQuestion)
                current_option_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(current_option_list)])
                bot.send_text_message(store_sender_id, current_option_text)
                bot.send_text_message(store_sender_id, f"Please choose an option (1-{current_option_count}):")
                sys.stdout.flush()
                return "ok", 200

         
         elif indicator == 'null chatHistory':
            current_option = getQuestion.checkCurrentQuestion(store_sender_id)
            str_option = json.loads(current_option)
            currentQuestion = str_option["Question"]
            current_option_list = str_option["Option"]
            current_option_count = len(current_option_list)
            #bot.send_text_message(store_sender_id, currentQuestion)
            current_option_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(current_option_list)])
            #bot.send_text_message(store_sender_id, current_option_text)
            #bot.send_text_message(store_sender_id, f"Please choose an option (1-{current_option_count}):")

            if msg > str(current_option_count) and msg.isdigit():
                    bot.send_text_message(store_sender_id, currentQuestion)
                    bot.send_text_message(store_sender_id, current_option_text)
                    bot.send_text_message(store_sender_id, f"Please choose an option (1-{current_option_count}):")
                    sys.stdout.flush()
                    return "ok", 200
            elif '1' <= msg <= str(current_option_count):
                    return_text = getQuestion.conQuestion(store_sender_id)
                    answer.add_Answer(store_sender_id,msg)
                    action.updateAction(store_sender_id)                    
                    
                    if return_text == 'end':
                        bot.send_text_message(store_sender_id, 'This is the end of Assessment\nOur staff will contact You soon')
                        sys.stdout.flush()
                        return "ok", 200
                    
                    print('null chatHistory return text:'+return_text)
                    str_return_text = json.loads(return_text)
                    # Question
                    question_text = str_return_text["Question"]
                    bot.send_text_message(store_sender_id, question_text)

                    # Option
                    option_list = str_return_text["Option"]
                    option_count = len(option_list)
                    option_numbers = [str(i+1) for i in range(option_count)]
                    option_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(option_list)])
                    bot.send_text_message(store_sender_id, option_text)
                    bot.send_text_message(store_sender_id, f"Please choose an option (1-{option_count}):")
                    sys.stdout.flush()
                    return "ok", 200
            else:
                currentQuestion = str_option["Question"]
                bot.send_text_message(store_sender_id, currentQuestion)
                current_option_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(current_option_list)])
                bot.send_text_message(store_sender_id, current_option_text)
                bot.send_text_message(store_sender_id, f"Please choose an option (1-{current_option_count}):")
                sys.stdout.flush()
                return "ok", 200


         else:
                    bot.send_text_message(store_sender_id, "What can I help you with?\nSelect an option\n(Type the option below)\n\n1. Quit Smoking\n2. NRT Usage Assessment")
                    sys.stdout.flush()
                    return "ok", 200
    else:
        sys.stdout.flush()
        return "ok", 200
    


def log(message):
 print('Here is Something\n')
 print(message)
 sys.stdout.flush()



if __name__ == "__main__":
 app.run(debug = True, port = 5000)
