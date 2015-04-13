# Solution to Matasano Crypto Challenge 2.10 
# http://cryptopals.com/sets/2/challenges/10/
# Use an AES-ECB encryption function to implement AES-CBC encryption

from Crypto.Cipher import AES
from crypto1 import base64_hex
from crypto9 import pad
import base64
import crypto2

def cbc_encrypt_block(first_block, next_block, key):
	# Perform CBC encryption on single block (using previous block)
	hex_xor_block = crypto2.hex_xor(first_block, next_block) 
	# If the first bits of first and next blocks were the same, 
	# front-pad the result to 16 bytes with zeroes
	padded_hex_xor_block = crypto2.front_padding(hex_xor_block) 
	raw_xor_block = padded_hex_xor_block.decode('hex')
	# Run result of XORed blocks through AES-ECB
	cipher = AES.new(key, AES.MODE_ECB)
	raw_cipher_block = cipher.encrypt(raw_xor_block)
	hex_cipher_block = raw_cipher_block.encode('hex')

	return hex_cipher_block

def cbc_decrypt_block(first_block, next_block, key):
	# Perform CBC decryption on single block in a reversed list of blocks
	# Decrypt the block using AES-ECB and XOR with next ciphertext block to 
	# return plaintext block
	raw_cipher_block = first_block.decode('hex')
	cipher = AES.new(key, AES.MODE_ECB)
	raw_xor_block = cipher.decrypt(raw_cipher_block)
	hex_xor_block = raw_xor_block.encode('hex')
	hex_plaintext_block = crypto2.hex_xor(hex_xor_block, next_block)

	return hex_plaintext_block

def split_into_blocks(plaintext, n_bytes):
	# Split plaintext into blocks of 16 bytes
	block_list = []

	for x in range(0,len(plaintext),n_bytes):
		block_list.append(plaintext[x:x+n_bytes])

	return block_list

def hex_block_list(block_list):
	# Convert list of blocks into a list of hex encoded blocks
	hex_blocks = []

	for y in block_list:
		hex_blocks.append(y.encode('hex'))

	return hex_blocks

def cbc_encrypt(plaintext, iv, key):
	# Encrypts entire plaintext using CBC
	padded_plaintext = pad(plaintext, 16) 
	plaintext_blocks = split_into_blocks(padded_plaintext, 16)
	hex_blocks = hex_block_list(plaintext_blocks)

	cipher_blocks = [] # XORed and AES-ECB encrypted blocks go here
	hex_iv = iv.encode('hex')
	cipher_blocks.append(hex_iv) # Seed list of cipher blocks with hex-encoded IV
	# Run cbc_encrypt_block on each XORed, AES-ECB encrypted block and the 
	# corresponding next block from the plaintext
	i = 0
	while i < len(hex_blocks): 
		cipher_blocks.append(cbc_encrypt_block(cipher_blocks[i], hex_blocks[i], key))
		i += 1

	ciphertext = ''.join(cipher_blocks[1:])

	return ciphertext

def cbc_decrypt(ciphertext, iv, key):
	# Decrypts entire CBC-encrypted ciphertext
	ciphertext_blocks = split_into_blocks(ciphertext, 32)
	ciphertext_blocks.reverse()
	hex_iv = iv.encode('hex') 
	ciphertext_blocks.append(hex_iv) # put IV at end of blocks to finish decryption

	plaintext_blocks = []
	# Run cbc_decrypt_block on each ciphertext block and send result to plaintext_blocks
	i = 0
	while i < len(ciphertext_blocks)-1:
		plaintext_blocks.append(cbc_decrypt_block(ciphertext_blocks[i], ciphertext_blocks[i+1], key))
		i += 1

	plaintext_blocks.reverse()
	plaintext = ''.join(plaintext_blocks)

	return plaintext

if __name__ == '__main__':
	
	f = open('10.txt', 'r')
	base64_ciphertext = f.read().strip()
	ciphertext = base64_hex(base64_ciphertext)

	IV = '\x00'*16
	key = 'YELLOW SUBMARINE'
	
	decrypted_text = cbc_decrypt(ciphertext, IV, key)
	padded_decrypted_text = decrypted_text + '0'
	print padded_decrypted_text

	f.close()
	# Comment out the above and uncomment the below to see full test
	"""
	f = open('10_sample.txt', 'r')
	plaintext = f.read()
	print pad(plaintext, 16).encode('hex')
	encrypted_text = cbc_encrypt(plaintext, '0000000000000000', 'YELLOW SUBMARINE')
	print encrypted_text
	decrypted_text = cbc_decrypt(encrypted_text, '0000000000000000', 'YELLOW SUBMARINE')
	print decrypted_text.decode('hex')
	f.close()
	"""




