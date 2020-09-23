# Covered topics:

# 1. Dealing with CoinMarketCap API
# 2. Making GET and POST requests with the Requests library
# 3. Dealing with json-objects with Python (reading and writing)
# 4. Creating a Flask application. Handling POST-requests with a Flask
# 5. Searching a text with regular expressions
# 6. Creating a Telegram Bot with BotFather. Adding a bot commands.
# 7. Dealing with the Telegram bots API.
# 8. Testing a webhook with tunneling services
# 9. Deploy Telegram bot (a Flask application) to the PythonAnyWhere servers.
# 10. Solving a SSL certificates issue with the Flask-SSLify extension
from flask import Flask,request,redirect,url_for
from flask import request
from flask import Response

from flaskext.mysql import MySQL
# from tokens import cmc_token
import requests
import json
import re

from flask_sslify import SSLify

token_telegram='1184469265:AAGgnSA0T1z3_PLNWMLu9LpB1fu6dCeNjyY'
# dùng link sau de ktra bot telegram hoạt động(dùng phương thức http)
# thông qua API tại link https://core.telegram.org/bots/api
# https://api.telegram.org/bot1150831495:AAF60TeituBAEZ9j4kiBp0Dhd1ArH9LpHH0/getMe
# dùng hậu tố sendMessage?+chat_id+&+text=...noi dung ==> gửi tin nhắn
# https://api.telegram.org/bot1150831495:AAF60TeituBAEZ9j4kiBp0Dhd1ArH9LpHH0/sendMessage?chat_id=1343733841&text=hello thongtinvtd
# set webhook
#https://api.telegram.org/bot1150831495:AAF60TeituBAEZ9j4kiBp0Dhd1ArH9LpHH0/setWebhook?url=https://8e53b91dd33a.ngrok.io ....
app = Flask(__name__) 
sslify = SSLify(app)

app.secret_key='qwetrqwywetyrtysdf'

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_PORT']= 3307
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='usbw'
app.config['MYSQL_DATABASE_DB']='test'

mysql=MySQL()
mysql.init_app(app)
conn = mysql.connect()
curs = conn.cursor()
print("Connect successful!")



def write_json(data,filename='reponse.json'):
    with open(filename,'w') as f:              #dung thu tuc with open() as tenfile: json.dump() de luu file
            json.dump(data,f,indent=4,ensure_ascii=False)


def get_data():
    # url='https://api.thevirustracker.com/free-api?global=stats'
    # r=requests.get(url).json()
    # return_result=r['results'][0]['total_cases']
    sql0="select temperature from climate where id=(select max(id) from climate);"
    curs.execute(sql0)
    tempo = curs.flechone()
    return tempo
#----------------------------------------------------------------------
def send_message(chat_id,text='hellllo'):
    url = f'https://api.telegram.org/bot{token_telegram}/sendMessage'
    payload = {'chat_id':chat_id,'text':text}

    r=requests.post(url,json=payload)
    return r
#--------------------------------------------------------
def parse_message(message):  #check dungs ten lenhj de phan hoi

    chat_id = message['message']['chat']['id']
    txt     = message['message']['text']

    pattern=r'/[a-zA-Z]{2,6}'       #taoj pattern de kiem tra lenh dua vao 
    ticker = re.findall(pattern,txt)    

    if ticker:                 # neu lenh dua vao co cau truc thich hop thi cho chuyen tiep lenh ko thi lenh = 'khong co gi'
        command=ticker[0][1:] #cat bo dau '/' 
    else:
        command=''
    
    return chat_id,command
#---------------------------------------------------

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id,command=parse_message(msg)  #tra ve chat_id va lenh sau khi nhan duoc chuoi json
        list_commands=('start','stop','help','status')
        
        if  command not in list_commands:
            send_message(chat_id,'Wrong command')
            return Response('ok',status=200)
        else:
            if command=='start':
                getdata=get_data()
                send_message(chat_id,getdata)
                return Response('ok',status=200)
            elif command=='help':
                list_commands='I have 4 commands:\n\b\b\b/start : start command, send the information\n\b\b\b/help : about me'
                send_message(chat_id,list_commands)
                return Response('ok',status=200)
        # totalcase=get_cmc_data()
        # send_message(chat_id,totalcase)
        # return Response('ok',status=200)
##vi tri ban dau UNDO

        # 
        # write_json(msg,'telegram_request.json')
        # return Response('ok',status=200)

    return '<h1>Telegram bot running_1  </h1>'

# def main():
    # print(get_cmc_data('BTC'))
    # 1. locally create a basic Flask application
    # 2. set up a tunnel
    # 3. set a webhook
    # 4. receiver and parser users messages
    # 5. send messages to a user

if __name__ == "__main__":
    app.run(debug=True)
    # main()