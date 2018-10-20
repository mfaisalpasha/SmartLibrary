import serial
import RPi.GPIO as GPIO
import time
import pymysql
import os
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
 
while True:
        conn=pymysql.connect(host='192.168.0.108',user='pi',password='',db='smartlocker')
        a=conn.cursor()
        sql="SELECT * FROM`occopylocker` WHERE `state`='ON';"
        a.execute(sql)
        results = a.fetchone()

        if results is not None:  
               status= results[2]
               lock=results[1]
               if status=="ON":
                    sqls="UPDATE `occopylocker` SET `state`='OFF' where `Locker_num`=%s;"
                    a.execute(sqls,lock)
                    pinres="SELECT PinNum FROM`locker` WHERE `Locker_num`=%s;"
                    a.execute(pinres,lock)
                    pin=a.fetchone()
                    pinNum=int(pin[0])
                    sqls="UPDATE `occopylocker` SET `state`='OFF' where `Locker_num`=%s;"
                    a.execute(sqls,lock)
                    GPIO.output(pinNum,False)
                    time.sleep(2)
                    GPIO.output(pinNum,True)
        conn.commit()
