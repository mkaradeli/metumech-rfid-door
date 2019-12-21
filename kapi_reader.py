#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
#import logging
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

waitTimeForAddingNewCards = 5
logfile = "/home/pi/kapi_records.log"
cards = "/home/pi/cards.txt"
admin_cards = "/home/pi/admin_cards.txt"
isCardAddMode = 0
cardAddButton = 18
isAdminAddMode = 0
adminAddButton = 16
role = 37
isAddingCardInd = 38
timeToKeepRoleOpen = 1
new_key = 0

#logging.basicConfig(filename=logfile, filemode='a+', level=logging.info, format='%(levelname)s:%(asctime)s:%(message)s')
#logging.info("Started Program.")
GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)


GPIO.setup(role, GPIO.OUT)
GPIO.output(role, GPIO.HIGH)

GPIO.setup(isAddingCardInd, GPIO.OUT)
GPIO.output(isAddingCardInd, GPIO.LOW)

#GPIO.setup(cardAddButton, GPIO.IN)
#GPIO.setup(adminAddButton, GPIO.IN)
#

def authenticate(new_key):
	if not new_key:
		return False
	f = open(cards, "r")
	f1 = f.readlines()
	for x in f1:
		if str(new_key) == x[0:12]:
			return True
 
	return False

def authenticate_admin(new_key):
	f = open(admin_cards, "r")
	f1 = f.readlines()
	for x in f1:
		if str(new_key) == x[0:12]:
			return True
	return False


#def addcardToFile(new_key):
#	f = open(cards, "r")
#	f1 = f.readlines()
#	for x in f1:
#		if str(new_key) == x[0:12]:
#			return
#	f= open(cards,"a+")
#	f.write("\n%s" % (new_key))
#	f.close()
#
#def addAdminCardToFile(new_key):
#	f = open(admin_cards, "r")
#	f1 = f.readlines()
#	for x in f1:
#		if str(new_key) == x[0:12]:
#			return
#	f= open(admin_cards,"a+")
#	f.write("\n%s" % (new_key))
#	f.close()

def blink():
	GPIO.output(isAddingCardInd, GPIO.LOW)
	sleep(0.1)
	GPIO.output(isAddingCardInd, GPIO.HIGH)
	sleep(0.3)
	GPIO.output(isAddingCardInd, GPIO.LOW)
	sleep(0.1)
	GPIO.output(isAddingCardInd, GPIO.HIGH)
	sleep(0.3)
	GPIO.output(isAddingCardInd, GPIO.LOW)
	sleep(0.1)
	GPIO.output(isAddingCardInd, GPIO.HIGH)
	sleep(0.3)
	GPIO.output(isAddingCardInd, GPIO.LOW)
	sleep(0.1)
	return


#def addcard():
#	GPIO.output(isAddingCardInd, GPIO.HIGH)
#	#logging.info("Read addCard button. Waiting for admin card.")
#	print("Read addCard button. Waiting for admin card.")
#	i=0
#	new_key = None
#	while (new_key is None):
#		new_key = reader.read_id_no_block()
#		i=i+1
#		sleep(0.1)
#		if waitTimeForAddingNewCards*10 is i:
#			print("took too long to add card")
#			blink()
#			return
#	GPIO.output(isAddingCardInd, GPIO.LOW)
#	sleep(1)
#	GPIO.output(isAddingCardInd, GPIO.HIGH)
#	if (authenticate_admin(new_key)):
#		#logging.info("Admin card(%s) authenticated. Waiting for new user card.", new_key)
#		print("Admin card(%s) authenticated. Waiting for new user card.", new_key)
#		admin_key = new_key
#		new_key = None
#		i = 0
#		while ((admin_key == new_key) | (new_key is None)):
#			new_key = reader.read_id_no_block()
#			print(new_key)
#			i=i+1
#			sleep(0.1)
#			if waitTimeForAddingNewCards*10 is i:
#				print("took too long to add card")
#				blink()
#				return
#
#		addcardToFile(new_key)
#		print("added new user")
#		GPIO.output(isAddingCardInd, GPIO.LOW)
#	else:
#		blink()
#		#logging.info("Read card isnt admin!")
#		print("Read card isnt admin!")
#	return
#	
#
#	
#
#def addAdminCard():
#	GPIO.output(isAddingCardInd, GPIO.HIGH)
#	#logging.info("Read addAdminCard button. Waiting for admin card.")
#	print("Read addAdminCard button. Waiting for admin card.")
#	i=0
#	new_key = None
#	while (new_key is None):
#		new_key = reader.read_id_no_block()
#		i=i+1
#		sleep(0.1)
#		if waitTimeForAddingNewCards*10 is i:
#			print("took too long to add card")
#			blink()
#			return
#	
#	GPIO.output(isAddingCardInd, GPIO.LOW)
#	sleep(1)
#	GPIO.output(isAddingCardInd, GPIO.HIGH)
#
#	if (authenticate_admin(new_key)):
#		#logging.info("Admin card(%s) authenticated. Waiting for new admin card.", new_key)
#		print("Admin card(%s) authenticated. Waiting for new admin card.", new_key)
#		admin_key = new_key
#		new_key = None
#		i = 0
#		while ((admin_key == new_key) | (new_key is None)):
#			new_key = reader.read_id_no_block()
#			print(new_key)
#			i=i+1
#			sleep(0.1)
#			if waitTimeForAddingNewCards*10 is i:
#				print("took too long to add card")
#				blink()
#				return
#
#		addAdminCardToFile(new_key)
#		addcardToFile(new_key)
#		print("added new admin card.")
#		GPIO.output(isAddingCardInd, GPIO.LOW)
#	else:
#		#logging.info("Read card isnt admin!")
#		print("Read card isnt admin!")
#		blink()

isReadyToReadCard = False
while True:
	if not isReadyToReadCard:
		#logging.info("Ready to read a card or a button")
		print("Ready to read a card or a button")
		isReadyToReadCard = True

#	isAdminAddMode = GPIO.input(adminAddButton) #check if button pressed to add admin
#	if (isAdminAddMode):
#		isReadyToReadCard = False
#		addAdminCard()
#
#	isCardAddMode = GPIO.input(cardAddButton) #check if button pressed to add card
#	if (isCardAddMode):
#		isReadyToReadCard = False
#		addcard()

	new_key = reader.read_id_no_block()
	
	if (new_key == None):
		new_key = 0
	else:
		isReadyToReadCard = False
		#logging.info("Read Card:%s", new_key)
		if (authenticate(new_key)):
			print("Unlocking" + str(new_key))
			#logging.info("Unlocking the door")
			GPIO.output(role, GPIO.LOW)
			GPIO.output(isAddingCardInd, GPIO.HIGH)
			sleep(timeToKeepRoleOpen)
			#logging.info("Locking the door")
			GPIO.output(role, GPIO.HIGH)
			GPIO.output(isAddingCardInd, GPIO.LOW)
		else:
			print("read card isnt auth."+ str(new_key))
			blink()

	

		sleep(0.2)
