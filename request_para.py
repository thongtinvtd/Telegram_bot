# coding: utf-8
from flask import Flask,request,redirect,url_for
from flask import request
from flask import Response
import requests
import lxml.html as html
from flaskext.mysql import MySQL
import requests
import json
from time import sleep
#with open('/home/huy/Desktop/tem.html', 'rb') as f:
#    content_html = f.read()

token_telegram='1184469265:AAGgnSA0T1z3_PLNWMLu9LpB1fu6dCeNjyY'

app = Flask(__name__)
app.secret_key='qwetrqwywetyrtysdsf'

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_PORT']= 3307
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='usbw'
app.config['MYSQL_DATABASE_DB']='test'

TIMEOUT = 10

mysql=MySQL()
mysql.init_app(app)
conn = mysql.connect()
curs = conn.cursor()
print("Connect successful!")

#-----------------------------------------------------------
def read_error():
    r = None
    while not r or r.status_code != 200:
        try:
            r = requests.get(
                'http://192.168.3.105/simpac/warning/c3k_warn.plc', 
                timeout=TIMEOUT
            )
        except Exception as e:
            print('Timeout, request again')
            sleep(1)

    tree = html.fromstring(r.content)
    # tr_error = tree.cssselect('div#tr_msquit')
    # name_error = tr_error[0].text
    #lay dc string error trong name error

    tbody = tree.cssselect('tbody') #--> tbody table notification.
    td1 = tbody[1].cssselect('td')  #--> row 2 has type error
    name_error = td1[1].text_content()
    type_error = td1[3].text_content()
    if type_error == '1':
        type_error = 'Alarm'
    elif type_error == '2':
        type_error = 'Warning'
    else :
        type_error = 'Info'
 # chua biet error hien thi nhu the nao
    return name_error,type_error
#------------------------------------------------------------
def send_message(chat_id,text='hellllo'):
    url = f'https://api.telegram.org/bot{token_telegram}/sendMessage'
    payload = {'chat_id':chat_id,'text':text}

    r=requests.post(url,json=payload)
    return r
#------------------------------------------------------------
def list_chat_id():
    try:
        sql3 = "SELECT USER_ID FROM ALERT_LIST"
        curs.execute(sql3)
        rows = curs.fetchall()
        listchatid = []
        if rows and rows[0]>0:
            for i in range (0, len(rows)-1):
                listchatid[i]=rows[i][0]
        
        return listchatid
    except Exception as e:
        raise(e)
#------------------------------------------------------------
while(1):
    sleep(10)  #chu ky ktra 10s
    error_text,error_type = read_error()   # kiem tra co loi thi gui tin nhan cho ng dung da dang ky
    if error_text != 'Quit Errors':
        list_chat_id_0 = list_chat_id()
        for chat_id in list_chat_id_0:
            mess = 'Attention ! Attention ! Now the climate camera has a problem : ' + error_text + ' .Type error : ' + error_type
            send_message(chat_id, mess) #--> gui message cho ng dung
    
    r = requests.get('http://192.168.3.105/simpac/info/c3k_frCVMV.plc') #Tao request de lay ve trang web so lieu
    r1= requests.get('http://192.168.3.105/simpac/auto/c3k_auto.plc')

    #noi dung dc chua trong content_html
    tree = html.fromstring(r.content)
    # tim trong chuoi table 
    trs_odd = tree.cssselect('tr.col_odd')

    tds_of_first_row = trs_odd[0].cssselect('td') #
    actual_temperature=tds_of_first_row[3].text
    setpoint_temperature=tds_of_first_row[4].text

    trs_even=tree.cssselect('tr.col_even')
    tds_of_second_row=trs_even[0].cssselect('td')
    actual_humidity=tds_of_second_row[3].text
    setpoint_humidity=tds_of_second_row[4].text
#-------------new parameter--------------------      
    tree = html.fromstring(r1.content)
    # tim trong chuoi table 
    # name_csssl0 = tree.cssselect('div#tr_profilno')
    # name_data0 = name_csssl.text_content()
    val_csssl0 = tree.cssselect('div#val_profilno')
    val_data0 = val_csssl0[0].text_content()
    val_csssl1 = tree.cssselect('div#val_profilename')
    val_data1 = val_csssl1[0].text_content()
    val_csssl2 = tree.cssselect('div#val_profilecycles')
    val_data2 = val_csssl2[0].text_content()
    val_csssl3 = tree.cssselect('div#val_activecycles')
    val_data3 = val_csssl3[0].text_content()
    val_csssl4 = tree.cssselect('div#val_totalloops')
    val_data4 = val_csssl4[0].text_content()
    val_csssl5 = tree.cssselect('div#val_actloops')
    val_data5 = val_csssl5[0].text_content()
    val_csssl6 = tree.cssselect('div#val_segment')
    val_data6 = val_csssl6[0].text_content()
    val_csssl7 = tree.cssselect('div#val_activetime')
    val_data7 = val_csssl7[0].text_content()
    val_csssl8 = tree.cssselect('div#val_profiletime')
    val_data8 = val_csssl8[0].text_content()
    val_csssl9 = tree.cssselect('div#val_totaltime')
    val_data9 = val_csssl9[0].text_content()
    val_csssl10 = tree.cssselect('div#val_segmenttype')
    val_data10 = val_csssl10[0].text_content()
    val_csssl11 = tree.cssselect('div#val_segmenttotaltime')
    val_data11 = val_csssl11[0].text_content()
    val_csssl12 = tree.cssselect('div#val_segmentremaintime')
    val_data12 = val_csssl12[0].text_content()
    val_csssl13 = tree.cssselect('div#val_status')
    val_data13 = val_csssl13[0].text_content()


    try:
        sql1="INSERT INTO CLIMATE(TEMPERATURE, \
                HUMIDITY, \
                TEMPERATURE_SET, \
                HUMIDITY_SET, \
                `Profile No.`, \
                `Profile Name`, \
                `Profile Cycles`, \
                `Active Cycles`, \
                `Total Loops`, \
                `Act Loops`, \
                `Segment`, \
                `Active Time`, \
                `Profile Time`, \
                `Total Time`, \
                `Segment Type`, \
                `Segment Total Time`, \
                `Segment Remain Time`, \
                `Status`) \
                VALUES \
                ({0},{1},{2},{3},\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\',\'{14}\',\'{15}\',\'{16}\',\'{17}\');".format(actual_temperature.strip(), \
                actual_humidity.strip(), setpoint_temperature.strip(), setpoint_humidity.strip(), \
                val_data0.strip(), val_data1.strip(), val_data2.strip(), val_data3.strip(), \
                val_data4.strip(), val_data5.strip(),val_data6.strip(),val_data7.strip(), \
                val_data8.strip(),val_data9.strip(),val_data10.strip(),val_data11.strip(), \
                val_data12.strip(),val_data13.strip())
        print(sql1)
        curs.execute(sql1)
        conn.commit()
    except Exception as e:
        raise(e)

    
    print ("Can not connect to http://192.168.3.105/simpac/info/c3k_frCVMV.plc")
    print ("Can not connect to http://192.168.3.105/simpac/auto/c3k_auto.plc")
        #-------------------------------------------------------
