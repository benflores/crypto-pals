# Solution to Matasano Crypto Challenge 4.26 http://cryptopals.com/sets/4/challenges/26/
# CTR bitflipping attack

from crypto2 import hex_xor
from crypto11 import generate_aes_key
from crypto16 import modify_plaintext
from crypto18 import generate_nonce
from crypto18 import ctr_mode #(text, nonce, key)
import re

def ctr_cookie(text, nonce, key):
	# Like a structured cookie, some portion of the plaintext might be known or guessable
	# Take an arbitrary input string and prepend/append strings below
	prepend_string = 'comment1=cooking%20MCs;userdata='
	append_string = ';comment2=%20like%20a%20pound%20of%20bacon'
	# Quote out any ';' or '=' characters
	modified_text = modify_plaintext(prepend_string, text, append_string).encode('hex')
	ctr_text = ctr_mode(modified_text, nonce, key)

	return ctr_text

def ctr_admin_status(ciphertext, nonce, key):

	plaintext = ctr_mode(ciphertext, nonce, key).decode('hex')
	is_admin = False
	if re.search(';admin=true;', plaintext):
		is_admin = True

	return is_admin

def recover_keystream(known_string, ciphertext):
	# If plaintext and ciphertext are both known, XOR together to recover keystream
	recovered_keystream = hex_xor(ciphertext[:len(known_string)], known_string)

	return recovered_keystream

def flip_token(ciphertext, admin_token, recovered_keystream):
	# XOR desired text injection with recovered keystream and replace that portion of ciphertext
	cipher_token = hex_xor(admin_token, recovered_keystream[:len(admin_token)])
	modified_ciphertext = cipher_token + ciphertext[len(cipher_token):]

	return modified_ciphertext

if __name__ == '__main__':

	nonce = chr(0)*8
	key = 'YELLOW SUBMARINE'
	plaintext = ''.encode('hex')
	ciphertext = ctr_cookie(plaintext, nonce, key)

	known_string = 'comment1"="cooking%20MCs";"userdata"="'.encode('hex')
	recovered_keystream = recover_keystream(known_string, ciphertext)
	admin_token = ';admin=true;'.encode('hex')
	flipped_ciphertext = flip_token(ciphertext, admin_token, recovered_keystream)
	
	print ctr_admin_status(flipped_ciphertext, nonce, key)
