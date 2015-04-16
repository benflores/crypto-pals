# Solution to Matasano Crypto Challenge 2.12 http://cryptopals.com/sets/2/challenges/12/
# Byte-at-a-time ECB Decryption (Simple)
# Appends plaintext to a known block of text (one byte shorter than full block), then
# brute-force matches the last byte of the encrypted block to get a byte of the plaintext

from crypto1 import base64_hex
from crypto7 import ecb_encrypt
from crypto8 import ecb_detect
from crypto11 import generate_aes_key
import base64

def prepend_to_plaintext(partial_block, plaintext, insertion_point):
	# This function modifies plaintext by prepending a known, repeating partial block
	# to the unknown portion of the plaintext (starting at insertion_point)
	modified_plaintext = ''
	modified_plaintext += partial_block
	modified_plaintext += plaintext[insertion_point:]

	return modified_plaintext

def match_bytes(plaintext, key, block_start):
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
			partial_block = 'A'*16
			modified_plaintext = prepend_to_plaintext(partial_block[:i], plaintext, 0)
			ciphertext = ecb_encrypt(modified_plaintext, key) 
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

def check_block_length(plaintext, key):
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
	# print generate_aes_key().encode('hex')
	# Hardcode key below
	key = 'ae1905271d3ffe6243d4238d5d0fd503'.decode('hex')

	plaintext = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

	print check_block_length(plaintext, key) # In this case, blocks begin to duplicate at 16 bytes.

	print match_bytes(plaintext, key, 0)	


