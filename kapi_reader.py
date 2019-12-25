#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import logging
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

cards = "/home/pi/cards.txt"
successfull_reads = "/home/pi/successfull_reads.txt"
unsuccessfull_reads = "/home/pi/unsuccessfull_reads.txt"

role = 37
#isAddingCardInd = 38
timeToKeepRoleOpen = 1
new_key = 0




def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='a+')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)    


setup_logger('log1', successfull_reads)
setup_logger('log2', unsuccessfull_reads)
logger_success = logging.getLogger('log1')
logger_fail = logging.getLogger('log2')




logger_success.info('Restarted Server.')
logger_fail.info('Restarted Server.')




GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)


GPIO.setup(role, GPIO.OUT)
GPIO.output(role, GPIO.HIGH)

#GPIO.setup(isAddingCardInd, GPIO.OUT)
#GPIO.output(isAddingCardInd, GPIO.LOW)



def authenticate(new_key):
	if not new_key:
		return False
	f = open(cards, "r")
	f1 = f.readlines()
	for x in f1:
		if str(new_key) == x[0:12]:
			logger_success.info(str(new_key))
			f.close()
			return True
	f.close()
	logger_fail.info(str(new_key))
	return False
	


#def blink():
#	GPIO.output(isAddingCardInd, GPIO.LOW)
#	sleep(0.1)
#	GPIO.output(isAddingCardInd, GPIO.HIGH)
#	sleep(0.3)
#	GPIO.output(isAddingCardInd, GPIO.LOW)
#	sleep(0.1)
#	GPIO.output(isAddingCardInd, GPIO.HIGH)
#	sleep(0.3)
#	GPIO.output(isAddingCardInd, GPIO.LOW)
#	sleep(0.1)
#	GPIO.output(isAddingCardInd, GPIO.HIGH)
#	sleep(0.3)
#	GPIO.output(isAddingCardInd, GPIO.LOW)
#	sleep(0.1)
#	return

def unlock():
	GPIO.output(role, GPIO.LOW)
	#GPIO.output(isAddingCardInd, GPIO.HIGH)
	sleep(timeToKeepRoleOpen)
	#logging.info("Locking the door")
	GPIO.output(role, GPIO.HIGH)


isReadyToReadCard = False
while True:
	if not isReadyToReadCard:
		print("Ready to read a card or a button")
		isReadyToReadCard = True


	new_key = reader.read_id_no_block()
	
	if (new_key == None):
		new_key = 0
	else:
		isReadyToReadCard = False
		#logging.info("Read Card:%s", new_key)
		if (authenticate(new_key)):
			print("Unlocking" + str(new_key))
			unlock()
		else:
			print("read card isnt auth."+ str(new_key))
			#blink()

	

	sleep(0.2)
