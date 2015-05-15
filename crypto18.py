# Solution to Matasano Crypto Challenge 3.18 http://cryptopals.com/sets/3/challenges/18/
# Implement CTR encryption/decryption

import crypto1
import struct
from Crypto.Cipher import AES
from random import randint
from crypto2 import hex_xor
from crypto11 import generate_aes_key


def ecb_no_padding(plaintext, key):
	# Encrypt using ECB but don't add extra 16 bytes of padding
	cipher = AES.new(key, AES.MODE_ECB)
	result = cipher.encrypt(plaintext)
	hex_result = result.encode('hex')

	return hex_result

def generate_keystream(text, nonce, key):
	# Generate a keystream dict by concatenating the nonce with the block-count-padding
	# for each block and encrypting under AES-ECB.
	keystream_dict = {}

	i = 0
	while i*32 < len(text):
		nonce_padding = struct.pack('Q', i)
		# The nonce_padding is an unsigned integer that increments with each block of text
		current_block_key = nonce + nonce_padding
		keystream = ecb_no_padding(current_block_key, key)
		# The key is used to encrypt the current nonce + block-count-padding using AES-ECB
		keystream_dict[i] = keystream
		i += 1
	
	return keystream_dict

def generate_blocks(text):
	# Create a dictionary of 16-byte blocks of text (other than the last block, if shorter)
	block_dict = {}

	i = 0
	while i*32 < len(text):
		block_dict[i] = text[(i*32):(i*32)+32]
		i += 1

	return block_dict

def truncate_keystream(block_dict, keystream_dict):
	# If the text is not a multiple of 16 bytes, the last block will be shorter than the last chunk
	# of keystream. Check if this is the case, and truncate the final piece of keystream if needed.
	last_block_count = max(block_dict)
	keystream_dict[last_block_count] = keystream_dict[last_block_count][:len(block_dict[last_block_count])]
	
	return keystream_dict

def ctr_mode(text, nonce, key):
	# Generate the blocks and keystream, truncate the keystream, and then encrypt/decrypt the text
	# by taking the XOR of each block with the corresponding piece of keystream.
	text_result = ''
	block_dict = generate_blocks(text)
	keystream_dict = generate_keystream(text, nonce, key)
	truncated_keystream_dict = truncate_keystream(block_dict, keystream_dict)

	j = 0
	while j <= max(block_dict):
		current_result = hex_xor(block_dict[j], keystream_dict[j])
		while len(current_result) != len(block_dict[j]):
			current_result = '0' + current_result
		text_result += current_result
		j += 1

	return text_result

def generate_nonce():

	random_nonce = ''

	for x in range(8):
		x = chr(randint(0,255))
		random_nonce += x

	return random_nonce


if __name__ == '__main__':

	nonce = chr(0)*8
	key = 'YELLOW SUBMARINE'
	ciphertext = crypto1.base64_hex('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
	print ctr_mode(ciphertext, nonce, key).decode('hex')
	# The following is a test using a randomly generated nonce and key that were stored for decryption. Generate_nonce and
	# generate_key allow for one-time nonce use.
	"""
	nonce = generate_nonce()
	print nonce.encode('hex')
	key = generate_aes_key()
	print key.encode('hex')
	plaintext = 'This is a secret message. Encrypt it using CTR mode, then decrypt it the same way!'.encode('hex')
	text_result = ctr_mode(plaintext, nonce, key)
	print text_result
	"""
	"""
	nonce = '40ac78e45de812d7'.decode('hex')
	key = '5d037f0db5e125b524c110ea6e630356'.decode('hex')
	ciphertext = 'd106362149ec347cc12bad507158273c941bd089af1d4875711aefba7e4716a84ef05dd8eb1bc5d8f9470acf37fbf114459d9e3a3b7f3e5319a0aaeedc5d6a6ffbbff0ffed9e9626e529bcb11f73282f958e'
	text_result = ctr_mode(ciphertext, nonce, key)
	print text_result.decode('hex')
	"""



