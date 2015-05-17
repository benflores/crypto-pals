# Solution to Matasano Crypto Challenge 4.27 http://cryptopals.com/sets/4/challenges/27/
# CBC identical IV/Key Attack

from crypto2 import better_hex_xor
from crypto10 import cbc_decrypt
from crypto11 import generate_aes_key
from crypto16 import modified_cbc_encrypt #(plaintext, IV, key)

def verify_ascii(ciphertext, IV, key):

	plaintext = cbc_decrypt(ciphertext, IV, key).decode('hex')

	for character in plaintext:
		if ord(character) > 127:
			print 1
			return plaintext.encode('hex')

	return 0

if __name__ == '__main__':
	
	plaintext = ''
	key = generate_aes_key()
	print key.encode('hex')
	IV = key

	ciphertext = modified_cbc_encrypt(plaintext, IV, key)
	modified_ciphertext = ciphertext[:32] + '00'*16 + ciphertext[:32]
	modified_plaintext = verify_ascii(modified_ciphertext, IV, key)

	print better_hex_xor(modified_plaintext[:32], modified_plaintext[64:])

