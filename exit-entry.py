import time
import serial
import RPi.GPIO as GPIO
import urllib2
import time
import pymysql
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(40, GPIO.OUT)
p = GPIO.PWM(40, 50)
p.start(2.5)

ans=1
#Tag1 = str('4E009698F3B3')
PortRF = serial.Serial('/dev/serial0',9600)
PortRF.flushInput()
while True:
    print "\nSwipe your ID card please "
    conn=pymysql.connect(host='192.168.0.108',user='pi',password='',db='smartlocker')
    a=conn.cursor()
    ID = ""
    read_byte = PortRF.read()
    if read_byte=="\x02":
        for Counter in range(12):
            read_byte=PortRF.read()
            ID = ID + str(read_byte)
            #print hex(ord( read_byte))
        print ID
        PortRF.flushInput()
        
        CheckStdID="SELECT St_id FROM`student` WHERE `RFID`= %s;"
        a.execute(CheckStdID,ID)
        stud = a.fetchone()
        ID = ""
        read_byte =""
        if stud is not None:
            st=str(stud[0])
            CheckStInCurrentStdTable="SELECT * FROM current_std WHERE `St_id`= %s;"
            a.execute(CheckStInCurrentStdTable,st)
            res = a.fetchone()
            if res is not None:
                
                DeletefromCurrentStdTable="DELETE FROM current_std WHERE `St_id`= %s;"
                a.execute(DeletefromCurrentStdTable,st)
                PortRF.flushInput()
                print "Bye!"
                p.ChangeDutyCycle(12.5)  # turn towards 0 degree
                time.sleep(3) # sleep 1 second
                p.ChangeDutyCycle(2.5) # turn towards 180 degree
                time.sleep(1) # sleep 1 second 
            else:
                InsertIntoCurrentSttdTable="INSERT INTO current_std(floor_num,St_id) VALUES(1,%s);"
                a.execute(InsertIntoCurrentSttdTable,st)
                #print ans
                PortRF.flushInput()
                print "WelCome!"
                p.ChangeDutyCycle(12.5)  # turn towards 0 degree
                time.sleep(3) # sleep 1 second
                p.ChangeDutyCycle(2.5) # turn towards 180 degree
                time.sleep(1) # sleep 1 second 
            
        else:
            
            print "Access Denied"
            PortRF.flushInput()
    PortRF.flushInput()
    conn.commit()
    time.sleep(2)
    ans+=1
