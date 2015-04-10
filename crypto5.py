# Solution to Matasano Crypto Challenge 1.5 http://cryptopals.com/sets/1/challenges/5/
# Implement repeating key cipher - given a plaintext string, encrypt using a repeating key
# XOR each byte of plaintext with corresponding byte of key, repeated through length of plaintext
# Also implemented a decryption function (symmetrical encryption/decryption)
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

def encrypt_repeating_key(plaintext, key):
	encrypted = ''
	key_length = len(key)
	i = 0
	j = 0
	while i <= len(plaintext)-1:
		encrypted += chr(ord(plaintext[i])^ord(key[j % key_length]))
		j += 1
		i += 1
	return encrypted.encode('hex')

def decrypt_repeating_key(ciphertext, key):
	decrypted = ''
	key_length = len(key)
	i = 0
	j = 0
	while i <= len(ciphertext)-1:
		decrypted += chr(ord(ciphertext[i])^ord(key[j % key_length]))
		j += 1
		i += 1	
	return decrypted

if __name__ == '__main__':
	plaintext_file = open('sample.txt', 'r') # open('5.txt', 'r')
	ciphertext_file = open('sample_encrypted.txt', 'w+') # open('5_encrypted.txt', 'w+')
	plaintext = plaintext_file.read()
	key = 'p4ndemonium!' # 'ICE'
	encrypted_phrase = encrypt_repeating_key(plaintext, key)
	ciphertext_file.write(encrypted_phrase)
	print decrypt_repeating_key(encrypted_phrase.decode('hex'), key)
	plaintext_file.close()
	ciphertext_file.close()

