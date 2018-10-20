import time
import serial
import RPi.GPIO as GPIO
import urllib2
import time
import pymysql
import datetime
import os
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
 
#Tag1 = str('4E009698F3B3')
PortRF = serial.Serial('/dev/serial0',9600)
conn=pymysql.connect(host='192.168.0.108',user='pi',password='',db='smartlocker')
a=conn.cursor()
PortRF.flushInput()
while True:
    os.system('clear')
    print "\nSwipe your ID card please "
    now = datetime.datetime.now()
    Time="%s:%s:%s"%(now.hour,now.minute,now.second)

    DeleteTime="DELETE FROM `book_table` WHERE %s > ADDTIME(start_time,'00:05:00') AND occupy=0"
    a.execute(DeleteTime,Time)
    ID = ""
    read_byte = PortRF.read()
    if read_byte=="\x02":
        for Counter in range(12):
            read_byte=PortRF.read()
            ID = ID + str(read_byte)
            #print hex(ord( read_byte))
        print ID
        
        
        sql2="SELECT St_id FROM`student` WHERE `RFID`= %s;"
        a.execute(sql2,ID)
        stud = a.fetchone()
        
        if stud is not None:
            st=str(stud[0])
            sql1="SELECT table_num,SeatNum FROM`book_table` WHERE `St_id`= %s;"
            a.execute(sql1,st)
            PortRF.flushInput()
            GPIO.cleanup()
            res = a.fetchone()
            if res is not None:
                TableNum=int(res[0])
                SeatNum=int(res[1])
                SetFlag="UPDATE book_table SET occupy=1 where table_num=%s;"
                a.execute(SetFlag,TableNum)
                PortRF.flushInput()
                GPIO.cleanup()
                print "Your Table Number is ",TableNum,"Your Seat Number is ",SeatNum
                
            else:
                print "There is no seat for you please book one"
                PortRF.flushInput()
                GPIO.cleanup()
                
            
            
        else:
            
            print "Access Denied"
            PortRF.flushInput()
            GPIO.cleanup()
    
    
    conn.commit()
    PortRF.flushInput()
    GPIO.cleanup()

