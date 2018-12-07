import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
import MFRC522
import paho.mqtt.client as mqtt
import threading

hx = HX711(5, 6)
hx.set_reading_format("LSB", "MSB")

hx.reset()
hx.tare()

RST1 = 22 #GPIO
RST2 = 27 #GPIO
SPI_DEV0 = '/dev/spidev0.0'
SPI_DEV1 = '/dev/spidev0.1'

global validCardIDBlank
global validCardIDLiam
validCardIDBlank = 648156165
validCardIDLiam = 7111720969
global validCardIDPointsLiam
global validCardIDPointsBlank
validCardIDPointsLiam = 0
validCardIDPointsBlank = 0
global topActive
global bottomActive
global timeStart
global liamFile


timeStart = 0
topActive = 0
bottomActive = 0

global setVal
setVal = 0
global val
val = 0
global i
i = 0



def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()
    device
def on_connect(client, userdata, flatgs, rc):
    print("Connected with result code "+str(rc))
    
    client.subscribe("RPiZ")
    client.subscribe("RPiZW")
    client.subscribe("RPi2B")
    
    
    
def on_message(client, userdata, msg):
    global timeStart
    global bottomActive
    global topActive
    global validCardIDBlank
    global validCardIDLiam

    global validCardIDPointsLiam
    global validCardIDPointsBlank
    global setVal
    global i
    global val
    global liamFile
    liamFile = open("LiamOutput.csv", "w+")
       
  
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "RPiZW":
        print("Top stair card reader swiped")
	cardUIDint = int(msg.payload)
	print(cardUIDint)
	
	if ((cardUIDint == validCardIDBlank or cardUIDint == validCardIDLiam) and (topActive == 0) and (bottomActive== 0)):
            
            topActive = 1
            global timeStart
	    timeStart = time.time()
	    
			
	if ((cardUIDint == validCardIDBlank or cardUIDint == validCardIDLiam) and topActive == 0 and bottomActive == 1 and (time.time() <= timeStart + 10)):
	    if (cardUIDint == validCardIDLiam):
                validCardIDPointsLiam += 10
                topActive = 0
                bottomActive = 0
                print("Your current points are:"),
                print validCardIDPointsLiam
                
                
            if (cardUIDint == validCardIDBlank):
                validCardIDPointsBlank += 10
                topActive = 0
                bottomActive = 0
                print("Your current points are:"),
                print validCardIDPointsBlank
	if ((cardUIDint != validCardIDBlank) and (cardUIDint != validCardIDLiam)): 
	    print("Please use valid card\n")
	if ((cardUIDint == validCardIDBlank or cardUIDint == validCardIDLiam) and topActive == 0 and bottomActive == 1 and (time.time() > timeStart + 10)):
	    topActive = 0
	    bottomActive = 0
			 
			
        
    if msg.topic == "RPiZ":
        print("Bottom stair card reader swiped")
        cardUIDint = int(msg.payload)
	if ((cardUIDint == validCardIDBlank or cardUIDint == validCardIDLiam) and topActive == 0 and bottomActive== 0):
	    
	  
	    bottomActive = 1
	    
	    timeStart = time.time()
			
	if ((cardUIDint == validCardIDBlank) or (cardUIDint == validCardIDLiam) and topActive == 1 and bottomActive == 0):
	    
	    if (cardUIDint == validCardIDLiam):
                validCardIDPointsLiam += 7
                topActive = 0
                bottomActive = 0
                print("Your current points are:"),
                print validCardIDPointsLiam
                
            if (cardUIDint == validCardIDBlank):
                validCardIDPointsBlank += 7
                topActive = 0
                bottomActive = 0
                print("Your current points are:"),
                print validCardIDPointsBlank
	    if ((cardUIDint != validCardIDBlank) and (cardUIDint != validCardIDLiam)):
		print("Please use valid card")
	    if ((cardUIDint == validCardIDBlank or cardUIDint == validCardIDLiam) and topActive == 0 and bottomActive == 1 and (time.time() > timeStart + 10)):
                topActive = 0
                bottomActive = 0
		
    if msg.topic == "RPi2B":
        print("Recycling reader swiped")
	cardUIDint = int(msg.payload)
	if (cardUIDint == validCardIDBlank or cardUIDint == validCardIDLiam):
	    timeStart = time.time()
	    print timeStart
			
	    while (time.time() < timeStart + 10):
		try:
                    while (i < 5):
                        val = hx.get_weight(1)
                        if (val > 2000):
                            setVal = val
			print val
			print setVal
			i = i + 1
			
                    i = 0
                    hx.power_down()
		    hx.power_up()
		    time.sleep(0.1)
		except (KeyboardInterrupt, SystemExit):
                    cleanAndExit()
            print("End of timer loop")
            if (setVal >= 2000 and cardUIDint == validCardIDLiam):
                
                validCardIDPointsLiam += 5
                print("Your current points are:"),
                print validCardIDPointsLiam
                liamFile.write(validIDPointsLiam)
                
            if (setVal >= 2000 and cardUIDint == validCardIDBlank):
                validCardIDPointsBlank += 5
                print("Your current points are:"),
                print validCardIDPointsBlank
                
            setVal = 0
	if ((cardUIDint != validCardIDBlank) and (cardUIDint != validCardIDLiam)):
	    cardUIDint = str(cardUIDint)
	    print(cardUIDint + "is invalid card. Please use authorized card")
  
         
    print(topActive)
    print(bottomActive)
    msg.payload = inputUID
    print("Received "+inputUID)
    
def mqttThings():
    while True:
        lock.acquire()
        client.loop_start()
        client.loop_stop()
        lock.release()
        time.sleep(0.1)
        
if __name__ == "__main__":
    lock = threading.Lock()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.1.1", 1883, 60)
    


client.loop_forever()











	
