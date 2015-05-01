# Solution to Matasano Crypto Challenge 3.19 http://cryptopals.com/sets/3/challenges/19/
# Break fixed-nonce CTR mode using substitutions

from crypto1 import base64_hex
from crypto2 import hex_xor
from crypto11 import generate_aes_key
from crypto18 import ctr_mode

def ctr_texts(plaintext_file, ciphertext_file):

	nonce = chr(0)*8
	key = generate_aes_key()
	print key.encode('hex')

	for line in plaintext_file:
		
		hex_line = base64_hex(line)
		ciphertext = ctr_mode(hex_line, nonce, key)
		ciphertext_file.write(ciphertext + '\n')
		

if __name__ == '__main__':

	plaintext_file = open('19.txt', 'r')
	ciphertext_file = open('19_ciphertexts.txt', 'r') # 'w+')
	
	# Encrypt a file of base64 plaintexts using CTR mode with a fixed (random) nonce and key.
	"""
	nonce = chr(0)*8
	key = generate_aes_key() #7e05a49023240ede8adb5350f11a58f1
	print key.encode('hex')

	for line in plaintext_file:
		
		hex_line = base64_hex(line)
		ciphertext = ctr_mode(hex_line, nonce, key)
		ciphertext_file.write(ciphertext + '\n')
	"""
	# Locate common starting pattern in ciphertexts. In this case, '4889' simply appears
	# to be common. Guessed that these two letters would be "Th" because that's a common
	# digram. So, XOR ciphertext '4889' with 'Th', which yields a resulting chunk of keystream,
	# '1cf0'. XOR this piece of keystream with with first 'xxxx' of all other ciphertexts. 
	# If the results make sense, use a decrypted ciphertext chunk to predict another chunk.
	# Change the plaintext guess to reflect this, and expand the test_length appropriately.
	# Rinse and repeat.
	"""
	keystream_chunk = '5495cc97743ea1f69fb6dcb16822f0df946fe319ecedba205457aa0212686a46fb22037077c0'
	plaintext_guess = 'He, too, has been changed in his turn,'
	keystream_byte = hex_xor(keystream_chunk, plaintext_guess.encode('hex'))
	print keystream_byte
	for line in ciphertext_file:
		test_length = 76
		if len(line) >= test_length:
			print hex_xor(line[:test_length], keystream_byte).decode('hex')
			print line[:test_length]
	"""

	keystream = '1cf0e0b70051cedabfdebdc2484095bafa4f80718d83dd453077c36c32000335db56760219ec'
	chunk = '5495cc97743ea1f69fb6dcb16822f0df946fe319ecedba205457aa0212686a46fb22037077c0'

	for line in ciphertext_file:
		cipher_line = line.strip()
		if len(cipher_line) < len(keystream):
			print hex_xor(cipher_line, keystream[:len(cipher_line)]).decode('hex')
		else:
			print hex_xor(cipher_line[:len(keystream)], keystream).decode('hex')
	
	plaintext_file.close()
	ciphertext_file.close()
