# Solution to Matasano Crypto Challenge 3.21 http://cryptopals.com/sets/3/challenges/21/
# Implement MT19937 Mersenne Twister RNG

generator_state = []
for x in xrange(624):
	generator_state.append(0)

index = 0

def initialize_generator(seed):

	global generator_state
	global index

	index = 0
	generator_state[0] = seed

	bitmask_32bits = (1 << 32) - 1

	for i in xrange(1,624):
		generator_state[i] = bitmask_32bits & (0x6c078965 * ((generator_state[i-1]) ^ (generator_state[i-1] >> 30)) + i)

	print generator_state
def extract_number():

	global index

	if index == 0:
		generate_numbers()

	y = generator_state[index]
	y = y ^ (y >> 11)
	y = y ^ ((y << 7) & 0x9d2c5680)
	y = y ^ ((y << 15) & 0xefc60000)
	y = y ^ (y >> 18)

	index = (index + 1) % 624

	return y

def generate_numbers():
	
	bitmask_bit31 = 0x80000000
	bitmas_bits0_30 = 0x7fffffff

	for i in xrange(624):
		y = (generator_state[i] & bitmask_bit31) + ((generator_state[(i + 1) % 624]) & bitmas_bits0_30)
		generator_state[i] = (generator_state[(i + 397) % 624]) ^ (y >> 1)

		if (y % 2) != 0:
			generator_state[i] = generator_state[i] ^ 0x9908b0df

if __name__ == '__main__':
	initialize_generator(0) #3791854820
	for x in xrange(624):
		print extract_number()



