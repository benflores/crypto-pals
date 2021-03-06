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
	a = '0x' + x
	b = '0x' + y
	m = int(a, base = 0)
	n = int(b, base = 0)

	result = format(m^n, 'x')

	if len(result) % 2 != 0:
		result = '0' + result

	return result

def validate_padding(plaintext):
	# Detect and remove padding
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

	unvalidated_plaintext = cbc_decrypt(ciphertext, IV, key).decode('hex')
	return validate_padding(unvalidated_plaintext)

def find_padding_targets(ciphertext): # this uses a CBC hex ciphertext 32 bytes long
	
	h = 32
	current_block = ciphertext[h:h+32]
	previous_block = ciphertext[h-32:h]

	known_decryptions = ''
	padding_fillers = ''

	i = 32
	j = 1 # increment through valid padding amounts (e.g. 0x01, 0x02, etc.)

	while i > 0:

		for x in range(256):

			test_value = chr(x).encode('hex')
			test_block = previous_block[:i-2] + test_value + padding_fillers + current_block
			valid_padding_found = validated_decryption(test_block, IV, key)

			if valid_padding_found == True:

				current_padding = chr(j).encode('hex')
				next_padding = chr(j+1).encode('hex')
				target_decryption = even_length_hex_xor(test_value, current_padding)
				# test_value xor plaintext padding value gives intermediate decrypted text
				# xor this with actual previous ciphertext block to get plaintext
				known_decryptions = target_decryption + known_decryptions
				padding_fillers = even_length_hex_xor(known_decryptions, next_padding*j)
				# intermediate decrypted text XOR next padding value gives next padding value				
				while len(padding_fillers) != len(known_decryptions):
					print known_decryptions, next_padding*j, padding_fillers
					print 'MODIFICATION MADE!!!'
					padding_fillers = '0' + padding_fillers
					print padding_fillers

				break

		i -= 2
		j += 1

	return known_decryptions

def blockwise_padding_attack(ciphertext):

	known_plaintext = ''

	for block_start in range(0, len(ciphertext)-64, 32):

		test_ciphertext = ciphertext[block_start:block_start+64]
		decrypted_block = find_padding_targets(test_ciphertext)
		plaintext_block = even_length_hex_xor(decrypted_block, test_ciphertext[:32])
		known_plaintext += plaintext_block

	return known_plaintext

def random_ciphertext_test(ciphertext_file):

	ciphertext_strings = []

	for line in ciphertext_file:
		ciphertext_strings.append(line)

	selector = random.randint(0,9)

	chosen_ciphertext = ciphertext_strings[selector]

	return chosen_ciphertext

if __name__ == '__main__':

	ciphertext_strings = []
	ciphertext_file = open('17.txt', 'r')

	chosen_ciphertext = random_ciphertext_test(ciphertext_file)

	key = generate_aes_key()
	IV = generate_aes_key()

	ciphertext = cbc_encrypt(chosen_ciphertext, IV, key)
	
	decrypted_text = blockwise_padding_attack(ciphertext).decode('hex')
	
	print crypto1.base64_raw(decrypted_text)

	