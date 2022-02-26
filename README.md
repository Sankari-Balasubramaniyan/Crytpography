## **Cryptography**
**Encryption and decryption using AES algorithm**

**OBJECTIVE**

Created an encryption/decryption system for safe storage of Bank Customer details. 
The details of the customer (NAME and CARD NUMBER) can only be modified 
- ADD customer details
- DELETE customer details
- FIND customer card number by their name 
if the 2 responsible people of the bank are present.

The program is implemented in python language using pycrypto library.

**EXECUTION**

- Create a folder RAMDISK - to store encrypted key as a backup (key2.txt, keyab.txt, mainkey.txt).
- Create a folder DISK - to store encrypted bank customer file (en_data_file.txt), add a text file (data_file.txt) to store the name and card number of customer in decrypted form which will be encrypted and erased.
- Create a folder USB1 - to store the key1 of responsible person 1 (backup1.txt) in encrypted form.
- Create a folder USB2 - to store the key1 of responsible person 2 (backup2.txt) in encrypted form.

EXECUTION - python3 ./crypto.py
