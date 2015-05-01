# Solution to Matasano Crypto Challenge 3.18 http://cryptopals.com/sets/3/challenges/18/
# Implement CTR encryption/decryption

from Crypto.Cipher import AES
from crypto2 import hex_xor #(x, y)
from random import randint
import crypto1
import struct

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
		text_result += current_result
		j += 1

	return text_result

if __name__ == '__main__':

	nonce = chr(0)*8

	key = 'YELLOW SUBMARINE'
	ciphertext = crypto1.base64_hex('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
	text_result = ctr_mode(ciphertext, nonce, key)
	print text_result.decode('hex')



