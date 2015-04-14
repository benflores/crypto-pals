# Solution to Matasano Crypto Challenge 1.7 http://cryptopals.com/sets/1/challenges/7
# Given a base64-encoded ciphertext encrypted with AES-128 ECB
# encryption, and the 16-byte key, decrypt the ciphertext.
# This solution uses the PyCrypto library to decrypt the ciphertext.
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

from Crypto.Cipher import AES
from crypto9 import pad # (plaintext, block_length)
import base64

def ecb_encrypt(plaintext, key):

	padded_plaintext = pad(plaintext, 16)

	cipher = AES.new(key, AES.MODE_ECB)
	ciphertext = cipher.encrypt(padded_plaintext)

	return ciphertext

def ecb_decrypt(ciphertext, key):

	cipher = AES.new(key, AES.MODE_ECB)
	plaintext = cipher.decrypt(ciphertext)

	return plaintext

if __name__ == '__main__':

	f = open('7.txt', 'r')
	
	ciphertext = ''

	for line in f:
		ciphertext += line.strip()
		
	raw_ciphertext = base64.b64decode(ciphertext)

	key = 'YELLOW SUBMARINE'

	print ecb_decrypt(raw_ciphertext, key)
