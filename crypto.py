import sys
import os
import random
import string

from Crypto.Cipher import AES

key = 'abcdefghijklmnop'


def init():
	backup_cipher = AES.new(key, AES.MODE_ECB) 
        #known to server to encrypt backup files
	resp1_key1 = 'hfjdkslqpaozieur'
	resp2_key1 = 'jdkslqmapzoeirut'
	#encrypt key1 and store in usb as backup
	pass1 = 'youcannotguessit'
	pass2 = 'youcannevaguesss'
	#pass3 = 'improxyonehelloo'
	#pass4 = 'improxytwohelloo'
	#encyrpt pass and store in usb as backup
	global en_resp1_key1
	en_resp1_key1 = backup_cipher.encrypt(resp1_key1)
	global en_resp2_key1
	en_resp2_key1 = backup_cipher.encrypt(resp2_key1)
	global en_pass1
	en_pass1 = backup_cipher.encrypt(pass1)
	print(en_pass1)
	global en_pass2
	en_pass2 = backup_cipher.encrypt(pass2)
	print(en_pass2)
	#write all key1 and pass1 usb/backup
	usb1 = open("USB1/backup1.txt",'wb')
	usb1.write(en_resp1_key1)
	usb1.write('\n'.encode('utf-8'))
	usb1.write(en_pass1)
	usb1.write('\n'.encode('utf-8'))
	usb1.close()
	
	usb2 = open("USB2/backup2.txt",'wb')
	usb2.write(en_resp2_key1)
	usb2.write('\n'.encode('utf-8'))
	usb2.write(en_pass2)
	usb2.close()
	
	key2_cipher1 = AES.new(pass1, AES.MODE_ECB)
	key2_cipher2 = AES.new(pass2, AES.MODE_ECB)
	resp1_key2 = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	resp2_key2 = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	#encrypt key2 using pass and store in ramdisk
	global en_resp1_key2
	en_resp1_key2 = key2_cipher1.encrypt(resp1_key2)
	global en_resp2_key2
	en_resp2_key2 = key2_cipher2.encrypt(resp2_key2)
	#store encrypted key2 in ramdisk/key2
	key2_file = open("RAMDISK/key2.txt",'wb')
	key2_file.write(en_resp1_key2)
	key2_file.write('\n'.encode('utf-8'))
	key2_file.write(en_resp2_key2)
	key2_file.close()
	
	new_key1 = resp1_key1[0:8] + resp1_key2[0:8]
	print(new_key1)
	new_key2 = resp2_key1[8:16] + resp2_key2[8:16]
	keya_cipher = AES.new(new_key1, AES.MODE_ECB)
	keyb_cipher = AES.new(new_key2, AES.MODE_ECB)
	resp1_keya = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	resp2_keyb = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	#encrypt keya and keyb using key1+key2 and store in ramdisk
	global en_resp1_keya
	en_resp1_keya = keya_cipher.encrypt(resp1_keya)
	global en_resp2_keyb
	en_resp2_keyb = keyb_cipher.encrypt(resp2_keyb)
	#store encrypted keya,keyb in ramdisk/keya_keyb
	keyab = open("RAMDISK/keyab.txt",'wb')
	keyab.write(en_resp1_keya)
	keyab.write('\n'.encode('utf-8'))
	keyab.write(en_resp2_keyb)
	keyab.close()
	
	final_key = resp1_keya[8:16] + resp2_keyb[0:8]
	mainkey_cipher = AES.new(final_key, AES.MODE_ECB)
	mainkey = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	#encrypt using keya+keyb and store in ramdisk
	global en_mainkey
	en_mainkey = mainkey_cipher.encrypt(mainkey)
	#store in ramdisk/mainkey
	mainkey_file = open("RAMDISK/mainkey.txt",'wb')
	mainkey_file.write(en_mainkey)
	mainkey_file.close()
	
	file_encrypt(mainkey) 
	#file_decrypt(mainkey)
	#encrypt using mainkey and store in disk using file_encrypt() function

def user_interface():

	#Responsible person 1 check
	
	print("Responsible 1, your username please? \n")
	user_name_1 = input()
	print("Responsible 1, your password please? \n")
	pass1 = input()
	backup_cipher = AES.new(key, AES.MODE_ECB)
	print(en_pass1)
	password = (backup_cipher.decrypt(en_pass1)).decode()
	print(password)
	if(pass1 == password):
		print("Welcome manager 1 \n")
		print("Enter you key \n")
		resp1_key1 = input()
	else: 
		print("Wrong password, terminating service...\n")
		return
		
	key2_cipher = AES.new(password, AES.MODE_ECB)
	resp1_key2 = (key2_cipher.decrypt(en_resp1_key2)).decode()
	resp1_newkey = resp1_key1[0:8] + resp1_key2[0:8]
	keya_cipher = AES.new(resp1_newkey, AES.MODE_ECB)
	resp1_keya = (keya_cipher.decrypt(en_resp1_keya)).decode()
	print("Decryption key A - PHASE OVER")
	
	#Responsible person 2 check
	
	print("Responsible 2, your username please? \n")
	user_name_2 = input()
	print("Responsible 2, your password please? \n")
	pass2 = input()
	backup_cipher = AES.new(key, AES.MODE_ECB)
	
	password = (backup_cipher.decrypt(en_pass2)).decode()
	if(pass2 == password):
		print("Welcome manager 2 \n")
		print("Enter you key \n")
		resp2_key1 = input()
	else: 
		print("Wrong password, terminating service...\n")
		return
		
	key2_cipher = AES.new(password, AES.MODE_ECB)
	resp2_key2 = (key2_cipher.decrypt(en_resp2_key2)).decode()
	
	resp2_newkey = resp2_key1[8:16] + resp2_key2[8:16]
	keyb_cipher = AES.new(resp2_newkey, AES.MODE_ECB)
	resp2_keyb = (keyb_cipher.decrypt(en_resp2_keyb)).decode()
	print("Decryption key B - PHASE OVER")
	
	#decrypt main key
	
	finalkey = resp1_keya[8:16] + resp2_keyb[0:8]
	print("final key"+finalkey+"\n")
	mainkey_cipher = AES.new(finalkey, AES.MODE_ECB)
	mainkey = (mainkey_cipher.decrypt(en_mainkey)).decode()
	print(mainkey)
	print("Decryption main key - PHASE OVER")
	
	file_decrypt(mainkey)
	#decrypt mainfile calling file_decrypt() function using mainkey
	#give access to add, delete, find pairs
	
	print("Access granted to customer data file")
	print("Would you like to ADD, DELETE or FIND for customer details?")
	command = input()
	if(command == 'ADD'):
		print("Enter card number")
		card = input()
		print("Enter customer name")
		name = input()
		add_pair(card, name)
	elif(command == 'DELETE'):
		print("Enter card number")
		card = input()
		print("Enter customer name")
		name = input()
		delete_pair(card, name)
	elif(command == 'FIND'):
		print("Enter customer name")
		name = input()
		find_pair(name)
	#file_encrypt(mainkey)

def add_pair(card, name):
	datafile = open("DISK/data_file.txt", "a")
	datafile.write(card+" "+name+"\n")
	datafile.close()

def delete_pair(card, name):
        datafile = open("DISK/data_file.txt", "r")
        lines = datafile.read().splitlines()
        
        for i in range(len(lines)):
        	if(lines[i].startswith(card+" "+name)):
        		del lines[i]
        		break
        datafile.close()
        datafile = open("DISK/data_file.txt", "w")
        datafile.truncate(0)
        
        for line in lines:
        	datafile.write(line)
        	datafile.write("\n")
        datafile.close()

def find_pair(name):
	datafile = open("DISK/data_file.txt", "r")
	lines = datafile.readlines()
	cards = []
        
	for line in lines:
		l = line.split(" ")
		if(l[1] == name):
			cards.append(l[0])
        		
	for card in cards:
		print("Card number : "+card)
        	
#Encrypt data file and store in en_data_file, clear data_file
def file_encrypt(key):
	
	encrypt_cipher = AES.new(key, AES.MODE_ECB)
	
	decrypted = open("DISK/data_file.txt",'r')
	encrypted = open("DISK/en_data_file.txt",'wb')
	lines = decrypted.read().splitlines()
	
	for line in lines:
		n = len(line)
		print(line)
		if n==0:
			break
		elif n%16 != 0:
			line+=' '*(16 - n % 16)   #Padding
		encrypted_data = encrypt_cipher.encrypt(line)
		print(encrypted_data)
		encrypted.write(encrypted_data)
		encrypted.write('\r\n'.encode('utf-8'))
			
	encrypted.close()
	decrypted.close()
	#decrypted = open("DISK/data_file.txt",'w')		
	#decrypted.truncate(0)
	#decrypted.close()

	
#Decrypt en_data_file and store in data_file, clear en_data_file
def file_decrypt(key):

	decrypted = open("DISK/data_file.txt",'w')
	encrypted = open("DISK/en_data_file.txt",'rb')
	lines = encrypted.read().splitlines()
		
	decrypt_cipher = AES.new(key, AES.MODE_ECB)
	
	print(len(lines))
	for line in lines:
		n = len(line)
		print(line)
		if n==0 :
			break;
		decrypted_data = decrypt_cipher.decrypt(line)
		print(decrypted_data)
		decrypted.write(decrypted_data.decode())
		decrypted.write('\n')
		
	encrypted.close()
	decrypted.close()
	#encrypted = open("DISK/en_data_file.txt",'w')		
	#encrypted.truncate(0)
	#encrypted.close()

def main():
	print("Shall we begin?")
	init()
	user_interface()

if __name__ == "__main__":
	main()
