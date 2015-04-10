# Solution to Matasano Crypto Challenge 1.7 http://cryptopals.com/sets/1/challenges/7
# Given a base64-encoded ciphertext encrypted with AES-128 ECB
# encryption, and the 16-byte key, decrypt the ciphertext.
# This solution uses the PyCrypto library to decrypt the ciphertext.
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

from Crypto.Cipher import AES
import base64

cipher_text_file = open('7.txt', 'r')
plain_text_file = open('7_decrypted.txt', 'w+')

encrypted_text = ''
key = 'YELLOW SUBMARINE'

for line in cipher_text_file:
	encrypted_text += line.strip()
	
raw_encrypted_text = base64.b64decode(encrypted_text)

cipher = AES.new(key, AES.MODE_ECB)

plain_text = cipher.decrypt(raw_encrypted_text)
plain_text_file.write(plain_text)

cipher_text_file.close()
plain_text_file.close()


