# Solution to Matasano Crypto Challenge 2.11
# http://cryptopals.com/sets/2/challenges/11/
# ECB/CBC Detection Oracle - (psuedo)randomly encrypt plaintext using ECB or
# CBC and then using only ciphertext, detect which method was used

from crypto7 import ecb_encrypt #(plaintext, key)
from crypto7 import ecb_decrypt #(ciphertext, key)
from crypto10 import cbc_encrypt #(plaintext, iv, key)
from crypto10 import cbc_decrypt #(plaintext, iv, key)
from crypto8 import ecb_detect #(ciphertext, n) (larger n is less sensitive)
from random import randint

def generate_aes_key():
	# Choose random value between 0 and 255 for each of 16 bytes
	random_aes_key = ''

	for x in range(16):
		x = chr(randint(0,255))
		random_aes_key += x

	return random_aes_key

def modify_plaintext(plaintext):

	modified_plaintext = ''
	# Prepend random 5-10 bytes to plaintext
	prepend_length = randint(5,10)

	for x in range(prepend_length):
		x = chr(randint(0,255))
		modified_plaintext += x

	# Insert plaintext into modified_plaintext
	modified_plaintext += plaintext

	# Append random 5-10 bytes to plaintext
	append_length = randint(5,10)

	for y in range(append_length):
		y = chr(randint(0,255))
		modified_plaintext += y

	return modified_plaintext


def random_encryption(plaintext):

	random_aes_key = generate_aes_key()
	#print random_aes_key.encode('hex')
	modified_plaintext = modify_plaintext(plaintext)
	#print modified_plaintext.encode('hex')
	choose_encryption = randint(0,1)

	if choose_encryption == 0:
		mode = 'ECB'
		ciphertext = ecb_encrypt(modified_plaintext, random_aes_key)
	else:
		mode = 'CBC'
		IV = generate_aes_key()
		ciphertext = cbc_encrypt(modified_plaintext, IV, random_aes_key)

	return mode, ciphertext

def encryption_oracle(ciphertext, n):
	# n is substring length to check in ecb_detect
	# ecb_detect returns a count of identical substrings in the ciphertext
	count = ecb_detect(ciphertext, n)

	if count == 0:
		#print 'Identical Substrings:', count
		#print 'Probable AES.MODE: CBC'
		return 'CBC'
	else:
		#print 'Identical Substrings', count
		#print 'Probable AES.MODE: ECB' 
		return 'ECB'
	

if __name__ == '__main__':

	hit_count = 0
	false_ecb = 0
	file_list = ['cogdis.txt', 'confucius_say.txt', 'excuse30.txt', 'computer.txt', 'cops.txt', 'luvstory.txt', 'conan.txt', 'corporat.txt', 'practica.txt']

	j = 8
	while j < 9:
		f = open('/Users/benflores/text_files/%s' % file_list[j], 'r')
		plaintext = f.read()

		k = 0
		while k < 1:

			mode, ciphertext = random_encryption(plaintext)
			oracle_output = encryption_oracle(ciphertext, 32)

			if mode == oracle_output:
				hit_count += 1
			elif mode != oracle_output:
				if mode == 'CBC':
					false_ecb += 1

			k += 1

		f.close()
		j += 1

	print 'overll hit/false ecb ratio: %d:%d' % (hit_count, false_ecb)
	print 'false ecb count:', float(false_ecb)/(hit_count + false_ecb)

	# Performed 50 times each over 7 text files, this function return zero false
	# positive ECB identifications (~.25 error rate in failing to detect ECB, but 0 
	# errors in falsely detecting ECB when CBC ws used)
