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
cards = "/home/pi/cards-test.txt"

isAddingCardInd = 38
i = 0


def addcardToFile(new_key, isim):
	f= open(cards,"a+")
	f.write(str(new_key) + " : " + str(isim) + "\n")
	f.close()

def read_card():
	new_key = None
	i = 0
	while True:
		i=i+1
		sleep(0.1)

		if waitTimeForAddingNewCards*10 is i:
			print("İşlem zaman aşımına uğradı.")

			return False

		new_key = reader.read_id_no_block()

		if new_key != None:
			f = open(cards, "r")
			f1 = f.readlines()
			for x in f1:
				if str(new_key) == x[0:12]:
					print("okunan kart " + str(x[15:-1]) + "\'ye kayıtlı")
					f.close()
					return
			f.close()
			return new_key

islem = input("yeni kullanıcı eklemek ister misin? [y/N]\n")

if (islem == "y") | (islem == "Y"):
	print("lütfen eklenecek kartı okutun.\n")
	new_key = read_card()


	if new_key:
		print("okuma başarılı. kart id:" + str(new_key) + "\n")
		isim = list(map(str,input("lütfen eklenecek kart sahibinin adını girin:\n").split()))
		if input("kart: " + str(new_key) + " isim: " + str(" ".join(isim)) + "\nonaylıyor musunuz? [y/N]") == 'y':
			addcardToFile(new_key, str(" ".join(isim)))


exit()
