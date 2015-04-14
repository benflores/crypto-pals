# Solution to Matasano Crypto Challenge 2.11
# http://cryptopals.com/sets/2/challenges/11/
# ECB/CBC Detection Oracle

from crypto7 import ecb_encrypt #(plaintext, key)
from crypto7 import ecb_decrypt #(ciphertext, key)
from crypto10 import cbc_encrypt #(plaintext, iv, key)
from crypto10 import cbc_decrypt #(plaintext, iv, key)
from crypto8 import ecb_detect #(ciphertext, n) (larger n is less sensitive)

def generate_aes_key():
	# Choose random value between 0 and 255...16 times, combine into string
	# Key will be hex
	# This can also be used to generate a random IV
	pass

def add_bytes():
	# Choose random number between 5-10
	# Prepend this number of bytes to plaintext
	# Choose random number between 5-10
	# Append this number of bytes to plaintext
	pass

def random_encryption():
	# Get random value 0 or 1
	# If 0 - encrypt plaintext under ecb
	# If 1 - generate IV and encrypt under CBC
	pass

def encryption_oracle(plaintext):
	# generate_aes_key
	# add_bytes
	# random_encryption
	# run ecb_detect
	pass