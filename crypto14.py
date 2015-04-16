# Solution to Matasano Crypto Challenge 2.14 http://cryptopals.com/sets/2/challenges/14/
# Byte-at-a-time ECB Decryption (Harder)
# Appends plaintext to a known block of text (one byte shorter than full block), then
# brute-force matches the last byte of the encrypted block to get a byte of the plaintext.
# The whole thing is prepended by a fixed, but randomly generated count of random bytes.
# Run increasing repeated bytes through the encryption function and examine the ciphertexts
# to determine the prefix length, then lop the prefix off of the final ciphertext before checking.

from crypto1 import base64_hex
from crypto7 import ecb_encrypt
from crypto8 import ecb_detect
from crypto11 import generate_aes_key
from crypto12 import prepend_to_plaintext #(partial_block, plaintext, insertion_point)
from random import randint
import base64

def generate_prefix():
	# Choose random value between 0 and 32 for number of bytes
	w = randint(0,33)
	# Choose random value between 0 and 255 for each of 16 bytes
	prefix = ''

	for x in range(w):
		x = chr(randint(0,255))
		prefix += x

	return prefix

def prepend_to_plaintext(prefix, partial_block, plaintext):
	# This function modifies plaintext by prepending a known, repeating partial block
	# to the unknown portion of the plaintext
	modified_plaintext = ''
	modified_plaintext += prefix
	modified_plaintext += partial_block
	modified_plaintext += plaintext

	return modified_plaintext

def match_bytes(prefix, plaintext, key):
	# This function appends plaintext to a known block of text (shorter than one block), 
	# then brute-force matches a single byte at a time
	decrypted_text = ''
	known_block = 'A'*16

	h = 0
	while h < len(plaintext)*2:

		match = ''
		i = 15
		while i >= 0:
			# Each time a plaintext byte is discovered, decrease the partial_block
			# size - the plaintext will shift over to fill the empty positions in order to 
			# allow for the building of the test blocks below.
			partial_block = 'A'*(8)+'A'*16 # Put 8 extra bytes of padding in to negate the effect of the 24 byte prefix
			modified_plaintext = prepend_to_plaintext(prefix, partial_block[:i+8], plaintext)
			# In if name==main below, hypothesized that prefix is 24 bytes. Put in 8 extra bytes to the partial_block,
			# then lop the first two blocks off of the ciphertext before running the check.
			ciphertext = ecb_encrypt(modified_plaintext, key)[64:]
			current_ciphertext_block = ciphertext[h:h+32]

			byte_dictionary = {}
			# Test all possible byte values
			for x in range(255):
				# Build a test block out of i known bytes, the known portion of current block,
				# and a single byte value. Try for each single-byte value until a match is found
				# with the current block of the ciphertext.
				test_block = known_block[16-i:] + match + chr(x)
				encrypted_test_block = ecb_encrypt(test_block, key)
				byte_dictionary[x] = encrypted_test_block[:32]

				if byte_dictionary[x] == current_ciphertext_block:
					match += chr(x)
					break

			i -= 1

		known_block = match
		decrypted_text += known_block
		h += 32

	return decrypted_text

def check_block_length(key):
	ciphertext_length = 0
	# Detect the block length of the cipher by feeding text to the function until it rolls over
	# to double the size and repeats itself. 
	for x in range(2,33):
		ciphertext = ecb_encrypt('A'*x, key)
		ciphertext_length += len(ciphertext)
		block_sizes = [128, 64, 32, 16, 8, 4] # Try hex byte multiples greater than one byte
		# If at some point, blocks begin to duplicate, the block length tried is likely
		# to be the block length
		for y in block_sizes:
			is_match = ecb_detect(ciphertext, y)

			if is_match:
				return y, ':', is_match


if __name__ == '__main__':
	# Generate random AES key: 
	#print generate_aes_key().encode('hex')
	# Hardcode key below
	key = 'a126b69e9959d10ea7978d4f7f581822'.decode('hex')
	# Generate prefix (random count of random bytes)
	#print generate_prefix().encode('hex')
	# Hardcode random prefix below
	prefix = '1c2740b790bf0fa525e365acb1e2eaf82ec1c2540e20eb22'.decode('hex')

	plaintext = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

	# print check_block_length(key) # In this case, blocks begin to duplicate at 16 bytes.

	print match_bytes(prefix, plaintext, key)
	# Below, started with a value of 64, then looked at the pattern. The ciphertext added another full
	# block once x hit a value of 8, which suggests that the prefix is 24 bytes.
	"""
	for x in range(64): # Chose 64 simply because it seems high enough - if no pattern is detected, go higher
		plaintext = '' # Empty but using it for the sake of clear arguments for the function
		partial_block = 'A'*x # This is really a known block
		test_text = prepend_to_plaintext(prefix, 'A'*x, plaintext)
		ciphertext = ecb_encrypt(test_text, key)
		print ciphertext, len(ciphertext), x
	"""
	
	