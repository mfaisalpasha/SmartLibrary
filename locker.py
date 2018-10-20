import serial
import RPi.GPIO as GPIO
import urllib2
import time
import pymysql
import os
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7,GPIO.OUT)
GPIO.output(7,GPIO.HIGH)
GPIO.setup(11,GPIO.OUT)
GPIO.output(7,GPIO.HIGH)
GPIO.setup(12,GPIO.OUT)
GPIO.output(7,GPIO.HIGH)
GPIO.setup(13,GPIO.OUT)
GPIO.output(7,GPIO.HIGH)
 
PortRF = serial.Serial('/dev/serial0', 9600)
PortRF.flushInput()
while True:
        os.system('clear')
        conn=pymysql.connect(host='192.168.0.108',user='pi',password='',db='smartlocker')
        a=conn.cursor()
        print "Swipe your ID card please"
        
        ID = ""
        read_byte=""
        read_byte = PortRF.read()
        if read_byte=="\x02":
            for Counter in range(12):
                read_byte=PortRF.read()
                ID = ID + str(read_byte)
                #print hex(ord( read_byte))
            print ID
            PortRF.flushInput()
            
            sql2="SELECT St_id FROM`student` WHERE `RFID`= %s;"
            a.execute(sql2,ID)
            stud = a.fetchone()
            
            if stud is not None:
                st=str(stud[0])
                sql1="SELECT Locker_num FROM`occopylocker` WHERE `St_id`= %s;"
                a.execute(sql1,st)
                res = a.fetchone()
                if res is not None:
                    locker=int(res[0])
                    pinres1="SELECT PinNum FROM`locker` WHERE `Locker_num`=%s;"
                    a.execute(pinres1,locker)
                    pin1=a.fetchone()
                    pinNuM=int(pin1[0])
                    #print pinNuM
                    print "Do you want to open the locker or release?"
                    ans=raw_input("press o/r \n")
                    if ans.lower() == 'o':
                        GPIO.output(pinNuM,False)
                        time.sleep(1)
                        GPIO.output(pinNuM,True)
                        print "Locker number",locker, "has been opened"
                        time.sleep(2)
                        #os.system('clear')
                        PortRF.flushInput()
                        
                    elif ans.lower() == 'r':
                        DeleteFromOccupytable="DELETE FROM occopylocker where locker_num=%s;"
                        a.execute(DeleteFromOccupytable,locker)
                        SetFlagTo0="UPDATE locker SET flag=0 where Locker_num=%s;"
                        a.execute(SetFlagTo0,locker)
                        print "Your locker is released. Thank you."
                        GPIO.output(pinNuM,False)
                        time.sleep(1)
                        GPIO.output(pinNuM,True)
                        #os.system('clear')
                        time.sleep(2)
                        PortRF.flushInput()
                        
                    else:
                         print "thank you"
                         PortRF.flushInput()
                         
                        
                         
                else:
                    print "There is no locker for you. Do you want one?"
                    ans2=raw_input("press y/n \n")
                    if ans2.lower() == 'y':
                                occupylockersql="SELECT Locker_num from locker WHERE flag = 0;"
                                a.execute(occupylockersql)
                                occupyLockerRes=a.fetchone()
                                if occupyLockerRes is not None:
                                    LockerNum=int(occupyLockerRes[0])
                                    SetFlagTo1="UPDATE locker SET flag=1 where Locker_num=%s;"
                                    a.execute(SetFlagTo1,LockerNum)
                                    occupylockersql2="INSERT INTO occopylocker(St_id,Locker_num,state) VALUES(%s,%s,'OFF');"
                                    a.execute(occupylockersql2,(st,LockerNum))
                                    AfterOccupyPinNumSql="SELECT PinNum FROM`locker` WHERE `Locker_num`=%s;"
                                    a.execute(AfterOccupyPinNumSql,LockerNum)
                                    AfterOccupyPinRes=a.fetchone()
                                    AfterOccupyPinNum=int(AfterOccupyPinRes[0])
                                    print "You have been allocated locker number ", LockerNum
                                    time.sleep(2)
                                    GPIO.output(AfterOccupyPinNum,False)
                                    time.sleep(1)
                                    GPIO.output(AfterOccupyPinNum,True)
                                    #os.system('clear')
                                    PortRF.flushInput()
                                    
                                else:
                                        print "Sorry! No Locker is available!"
                                        PortRF.flushInput()
                                        
                
            else:
                print "Access Denied"
                PortRF.flushInput()
             

        conn.commit()
        PortRF.flushInput()
        
