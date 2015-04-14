# Solution to Matasano Crypto Challenge 1.8 http://cryptopals.com/sets/1/challenges/8
# Given a file with multiple cipher texts, detect the one encrypted with AES-ECB
# Look for identical 16-byte strings within each cipher text (this is the weakness of AES-ECB)
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

import crypto1
from Crypto.Cipher import AES

def ecb_detect(ciphertext, n):
	# Operates on a hex ciphertext
	# Returns a count of the number of identical substrings, where n is the
	# length of the substrings to check
	block_list = []
	# Split the ciphertext into blocks of n length
	for x in range(0, len(ciphertext), n):
		block_list.append(ciphertext[x:x+n])

	count = 0
	# Check to see if there are any identical blocks of n length
	for x in range(len(block_list)):
		for y in range(len(block_list)):
			if block_list[x] == block_list[y]:
				if x != y:
					count += 1
					return count
	return count


if __name__ == '__main__':
	
	f = open('8.txt', 'r')

	for line in f:
		stripped_line = line.strip()
		if ecb_detect(stripped_line, 32):
			print ecb_detect(stripped_line, 32)
			print stripped_line

	f.close()
