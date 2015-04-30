# Solution to Matasano Crypto Challenge 2.16 http://cryptopals.com/sets/2/challenges/16/
# CBC Bitflipping Attacks
# Flip bits in a ciphertext to produce a target value (e.g. a cookie to submit ;admin=true;)
# Method: XOR user-controlled porition of plaintext with target value, then XOR the corresponding
# ciphertext with this result and replace it into a modified ciphertext before decryption

from crypto2 import hex_xor #(x, y)
from crypto10 import cbc_decrypt #(ciphertext, IV, key)
from crypto10 import cbc_encrypt #(plaintext, IV, key)
from crypto11 import generate_aes_key
import re

def modify_plaintext(prepend_string, plaintext, append_string):
	# Prepend and append known strings to plaintext
	modified_plaintext = ''
	modified_plaintext += prepend_string + plaintext + append_string
	modified_plaintext = re.sub(';','";"', modified_plaintext)
	modified_plaintext = re.sub('=','"="', modified_plaintext)

	return modified_plaintext

def modified_cbc_encrypt(plaintext, IV, key):
	# Prepend and append known strings and encrypt under CBC
	prepend_string = 'comment1=cooking%20MCs;userdata='
	append_string = ';comment2=%20like%20a%20pound%20of%20bacon'
	modified_plaintext = modify_plaintext(prepend_string, plaintext, append_string)

	ciphertext = cbc_encrypt(modified_plaintext, IV, key)

	return ciphertext

def admin_status(ciphertext, IV, key):
	# Decrypt under CBC and search for ';admin=true;'
	plaintext = cbc_decrypt(ciphertext, IV, key).decode('hex')
	is_admin = False
	if re.search(';admin=true;', plaintext):
		is_admin = True

	return is_admin

if __name__ == '__main__':
	# Generate unknown random AES key and IV
	key = generate_aes_key()
	IV = generate_aes_key()
	# User-entered text starts at 86; 'A' string starts at 96
	# comment1"="cooking%20MCs";"userdata"="zzzzzzzzzz = [:96]
	test_text = 'z'*10 + 'A'*32 # Enter 'z's before 'A's to delineate start
	test_ciphertext = modified_cbc_encrypt(test_text, IV, key)
	# XOR the plaintext of the target phrase with the filler phrase
	target = ';admin=true;'.encode('hex')
	filler_text = ('A'*12).encode('hex') # test_text[10:22]
	plain_xor = hex_xor(target, filler_text)
	# Then XOR the result with the filler block of ciphertext and replace it into the ciphertext
	cipher_xor = hex_xor(test_ciphertext[96:120], plain_xor)
	modified_ciphertext = test_ciphertext[:96] + cipher_xor + test_ciphertext[120:]

	is_admin = admin_status(modified_ciphertext, IV, key)
	print is_admin

