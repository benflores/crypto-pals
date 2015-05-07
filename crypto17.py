# Solution to Matasano Crypto Challenge 3.17 http://cryptopals.com/sets/3/challenges/17/
# CBC Padding Oracle Attack
# Using only the information of whether a ciphertext has valid padding, decrypt the ciphertext.
# Use the XOR properties of a CBC encryption function to discover plaintext values by
# receiving valid padding messages.

import random
import crypto1
from crypto10 import cbc_decrypt #(ciphertext, IV, key)
from crypto10 import cbc_encrypt #(plaintext, IV, key)
from crypto11 import generate_aes_key

def even_length_hex_xor(x, y):
	# Prefix hex strings with 0x in order to enable XOR operation, XOR the strings,
	# then strip the '0x' from the result.
	a = '0x' + x
	b = '0x' + y
	m = int(a, base = 0)
	n = int(b, base = 0)

	result = format(m^n, 'x')
	# Prepend a zero if a leading zero was dropped.
	if len(result) % 2 != 0:
		result = '0' + result

	return result

def validate_padding(plaintext):
	# Detect padding in a plaintext and return True/False if the padding is valid/invalid.
	# Valid padding follows the scheme of 0xn * n.
	padding_amount = ord(plaintext[len(plaintext)-1])

	if padding_amount == 0:
		return False

	correct_padding = chr(padding_amount) * padding_amount
	actual_padding = plaintext[len(plaintext) - padding_amount:]

	if correct_padding != actual_padding:
		return False
	else:
		return True

def validated_decryption(ciphertext, IV, key):
	# This function and validate_padding() compartmentalize the decryption and validation of the text.
	unvalidated_plaintext = cbc_decrypt(ciphertext, IV, key).decode('hex')
	return validate_padding(unvalidated_plaintext)

def find_padding_targets(ciphertext): 
	# Takes a CBC-encrypted hex ciphertext and tests byte-by-byte for correct padding
	h = 32
	current_block = ciphertext[h:h+32]
	previous_block = ciphertext[h-32:h]

	known_decryptions = ''
	padding_fillers = ''

	i = 32
	j = 1 # Increment through valid padding amounts (e.g. 0x01, 0x02, etc.)

	while i > 0:

		for x in xrange(256):

			test_value = chr(x).encode('hex')
			test_block = previous_block[:i-2] + test_value + padding_fillers + current_block
			valid_padding_found = validated_decryption(test_block, IV, key)

			if valid_padding_found == True:

				current_padding = chr(j).encode('hex')
				next_padding = chr(j+1).encode('hex')
				# If valid padding is found, test value XOR padding value yields intermediate
				# decrypted value.
				target_decryption = even_length_hex_xor(test_value, current_padding)
				# Build a string of known intermediate decryptions. Intermediate decryptions XOR
				# next desired padding value result in plaintext for that padding value.
				known_decryptions = target_decryption + known_decryptions
				padding_fillers = even_length_hex_xor(known_decryptions, next_padding*j)

				while len(padding_fillers) != len(known_decryptions):
					# Ensure that two leading zeroes are not dropped due to XOR of identical values
					padding_fillers = '0' + padding_fillers 

				break

		i -= 2
		j += 1

	return known_decryptions

def blockwise_padding_attack(ciphertext):
	# Run find_padding_targets() on each 32-byte block of ciphertext.
	known_plaintext = ''

	for block_start in xrange(0, len(ciphertext)-64, 32):

		test_ciphertext = ciphertext[block_start:block_start+64]
		decrypted_block = find_padding_targets(test_ciphertext)
		# Intermediate decrypted values XOR actual ciphertext values of previous block yields plaintext
		plaintext_block = even_length_hex_xor(decrypted_block, test_ciphertext[:32])
		known_plaintext += plaintext_block

	return known_plaintext

def random_ciphertext_test(text_strings):
	# Choose a random string to encrypt and attack from a file of plaintexts
	ciphertext_strings = []

	for line in text_strings:
		ciphertext_strings.append(line)

	selector = random.randint(0,9)
	chosen_ciphertext = ciphertext_strings[selector]

	return chosen_ciphertext


if __name__ == '__main__':

	text_strings = open('17.txt', 'r')
	chosen_ciphertext = random_ciphertext_test(text_strings)
	# Choose a random plaintext, CBC encrypt it using random IV/key, and attack it
	key = generate_aes_key()
	IV = generate_aes_key()
	ciphertext = cbc_encrypt(chosen_ciphertext, IV, key)
	
	decrypted_text = blockwise_padding_attack(ciphertext).decode('hex')
	
	print crypto1.base64_raw(decrypted_text)

	