# Solution to Matasano Crypto Challenge 1.8 http://cryptopals.com/sets/1/challenges/8
# Given a file with multiple cipher texts, detect the one encrypted with AES-ECB
# Look for identical 16-byte strings within each cipher text (this is the weakness of AES-ECB)
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

import crypto1
from Crypto.Cipher import AES

def make_blocks(hex_text):
	block_list = []
	for x in range(0, len(hex_text), 32):
		block_list.append(hex_text[x:x+32])
	return block_list

def pattern_check(block_list):
	for x in range(len(block_list)):
		for y in range(len(block_list)):
			if x != y:
				if block_list[x] == block_list[y]:
					return True

if __name__ == '__main__':
	f = open('8.txt', 'r')

	for line in f:
		stripped_line = line.strip()
		block_list = make_blocks(stripped_line)
		if pattern_check(block_list):
			print stripped_line

	f.close()
