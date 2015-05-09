# Solution to Matasano Crypto Challenge 3.22 http://cryptopals.com/sets/3/challenges/22/
# Crack an MT19937 seed
# Seed MT19937 PRNG with Unix Timestamp seed, then test seed values to discover the seed used

import crypto21
import random
import time

def get_target_number():
	first_wait = random.randint(40, 1000)
	time.sleep(first_wait)
	time_seed = int(time.time())
	crypto21.initialize_generator(time_seed)
	next_wait = random.randint(40, 1000)
	time.sleep(next_wait)
	target_number = crypto21.extract_number()
	print "target number..."
	return target_number

def find_seed_time(target_number):

	i = int(time.time() - 5000)
	seed_match = 0
	seed_found = False
	while seed_found == False:
		crypto21.initialize_generator(i)
		test_number = crypto21.extract_number()
		if test_number == target_number:
			seed_match = i
			seed_found = True
		else:
			i += 1
	print "seed was..."
	return seed_match

if __name__ == '__main__':

	target_number = get_target_number()
	print target_number
	print find_seed_time(target_number)

