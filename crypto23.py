# Solution to Matasano Crypto Challenge 3.23 http://cryptopals.com/sets/3/challenges/23/
# Clone an MT19937 RNG from its output
"""
The MT19337 RNG creates an array of 624 "tempered" values using the bitshifting/XOR operations
found in crypto21.py. This script captures each tempered value (which is the random number output)
624 times, then "untempers" the number. This untempered number is captured into an array that is
used as the generator state for a cloned generator, which then outputs the same values as the original
generator, without needing to crack the seed directly. I wrote a skeleton for this program but couldn't
figure out how to invert the y = y ^ (y >> 11) and y = y ^ ((y << 7) & 0x9d2c5680) steps of the tempering.
I had to turn to a few different resources, lots of printing out the binary, etc., but ultimately resorted
to basically copying the math from http://b10l.com/?p=24 or 
https://github.com/gaganpreet/matasano-crypto-3/blob/ab1f8684d3730eb67029e0d6c9e53113a2dedcee/src/clone_mt.py
"""

import crypto21
import time

clone_index = 0

def clone_extract_number(clone_generator_state):

	global clone_index

	y = clone_generator_state[clone_index]
	y = y ^ (y >> 11)
	y = y ^ ((y << 7) & 0x9d2c5680)
	y = y ^ ((y << 15) & 0xefc60000)
	y = y ^ (y >> 18)

	clone_index = (clone_index + 1) % 624

	return y

def untemper_output(tempered_output):
	# I only vaguely understand how this works. I copied this bitwise math from:
	# https://github.com/lt/php-cryptopals/blob/master/03-block-and-stream-crypto/23-clone-an-mt19937-rng-from-its-output.php
	a = tempered_output
	y = a ^ (a >> 18)
	y = y ^ (y << 15) & 0xefc60000
	x = y ^ ((y << 7) & 0x9d2c5680)
	x = y ^ ((x << 7) & 0x9d2c5680)
	x = y ^ ((x << 7) & 0x9d2c5680)
	y = y ^ (x << 7) & 0x9d2c5680
	x = y ^ (y >> 11)
	y = y ^ (x >> 11)
	untempered_number = y
	return untempered_number

if __name__ == '__main__':

	crypto21.initialize_generator(int(time.time()))

	tempered_outputs = []
	untempered_numbers = []

	for x in xrange(624):
		tempered_output = crypto21.extract_number()
		tempered_outputs.append(tempered_output)
	print tempered_outputs

	for y in tempered_outputs:
		untempered_number = untemper_output(y)
		untempered_numbers.append(untempered_number)
	print untempered_numbers

	cloned_outputs = []
	for z in xrange(624):
		cloned_output = clone_extract_number(untempered_numbers)
		cloned_outputs.append(cloned_output)
	print cloned_outputs


