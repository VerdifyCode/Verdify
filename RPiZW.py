import paho.mqtt.publish as publish
import time
import RPi.GPIO as GPIO
import MFRC522


MIFAREReader = MFRC522.MFRC522()

print("Looking for cards")
print("Press Ctrl-C to stop.")
try:
  
  while True:

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    #(status,TagType) = MIFAREReaderA.MFRC522A_Request(MIFAREReaderA.PICC_REQIDL)
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    #(status,uid) = MIFAREReaderA.MFRC522A_Anticoll()
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

      # Print UID
      cardUID = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
      print("Card UID: " + cardUID)
      publish.single("RPiZW", cardUID, hostname="172.17.33.48")
      time.sleep(0.2)
    #if status == MIFAREReaderA.MI_OK:

      # Print UID
      #cardUID = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
      #print("Card UID: " + cardUID)
      #publish.single("RPiZW", cardUID, hostname="172.17.33.48")
      #time.sleep(0.1) 

except KeyboardInterrupt:
  GPIO.cleanup()
 