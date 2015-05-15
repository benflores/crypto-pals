# Solution to Matasano Crypto Challenge 4.25 http://cryptopals.com/sets/4/challenges/25/
# Implement random access read/write CTR mode and break it

from crypto2 import hex_xor
from crypto11 import generate_aes_key
from crypto18 import generate_nonce
from crypto18 import ctr_mode #(text, nonce, key)

def ctr_edit(ciphertext, nonce, key, offset, newtext):
	# Decrypts ciphertext, modifies plaintext, and returns re-encrypted ciphertext
	plaintext = ctr_mode(ciphertext, nonce, key).decode('hex')
	modified_plaintext = (plaintext[:offset] + newtext + plaintext[offset:]).encode('hex')
	modified_ciphertext = ctr_mode(modified_plaintext, nonce, key)

	return modified_ciphertext

def get_ctr_keystream(ciphertext, nonce, key):
	"""
	The ctr_edit function could be given to an attacker as an "edit" function without giving them the key
	This function modifies the beginning of the plaintext with a known piece of text the same length
	as the ciphertext, then XORs this with the beginning of the new ciphertext to recover the keystream
	"""
	controlled_text = 'A'*len(ciphertext.decode('hex'))
	modified_ciphertext = ctr_edit(ciphertext, nonce, key, 0, controlled_text)
	controlled_ciphertext = modified_ciphertext[:len(ciphertext)]
	keystream = hex_xor(controlled_text.encode('hex'), controlled_ciphertext)

	while len(keystream) != len(ciphertext):
		keystream = '0' + keystream

	return keystream

if __name__ == '__main__':

	f = open('7_decrypted.txt', 'r')
	plaintext = f.read().encode('hex')
	nonce = generate_nonce() 
	key = generate_aes_key()
	# plaintext = 'This is a secret message. Encrypt it using CTR mode, then decrypt it the same way!'.encode('hex')
	ciphertext = ctr_mode(plaintext, nonce, key)
	recovered_keystream = get_ctr_keystream(ciphertext, nonce, key)
	print hex_xor(recovered_keystream, ciphertext).decode('hex')
	f.close()
