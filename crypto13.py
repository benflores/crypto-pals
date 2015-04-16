# Solution to Matasano Crypto Challenge 2.13 http://cryptopals.com/sets/2/challenges/13/
# Implement ECB Cut-and-Paste Attack on structured cookie

import re
from random import randint
from crypto7 import ecb_decrypt
from crypto7 import ecb_encrypt
from crypto11 import generate_aes_key
from crypto12 import prepend_to_plaintext # (partial_block, plaintext, insertion_point)

def parse(user_cookie):
	# Parse user cookie by splitting at '&' characters and then splitting each
	# result at '=' character to get email, uid, and role
	# Cookie example: 'email=foo@bar.com&uid=10&role=user'
	user_profile = {}
	pairs = re.split('&', user_cookie)

	for item in pairs:
		item_list = re.split('=', item)
		user_profile[item_list[0]] = item_list[1]

	return user_profile

def profile_for(user_email):
	# Scrub email to make sure metacharacters '&' and '=' are not used
	scrubbed_email = re.sub('&', '', user_email)
	scrubbed_email = re.sub('=', '', scrubbed_email)

	user_profile = {}
	user_profile['email'] = scrubbed_email
	user_profile['uid'] = '10'
	user_profile['role'] = 'user'
	# Build user_profile_string from dictionary of user_profile info
	user_profile_string = 'email=%s&uid=%s&role=%s' % (user_profile['email'], user_profile['uid'], user_profile['role'])

	return user_profile_string

def encrypt_user_profile(user_profile_string, key):

	encrypted_profile = ecb_encrypt(user_profile_string, key)

	return encrypted_profile

def decrypt_user_profile(encrypted_profile, key):

	user_profile_string = ecb_decrypt(encrypted_profile.decode('hex'), key)
	print user_profile_string
	# Detect and remove padding
	padding_amount = ord(user_profile_string[len(user_profile_string)-1])
	user_profile_string = user_profile_string[:len(user_profile_string) - padding_amount]
	user_profile = parse(user_profile_string)
	
	return user_profile


if __name__ == '__main__':
	# Generate random AES key
	key = 'bc0a0a62756c8103a0db9020d5314201'.decode('hex')

	my_profile = profile_for('xxxxxxxx@.com')
	secure_profile = encrypt_user_profile(my_profile, key)

	blocks = [secure_profile[:32].decode('hex'), secure_profile[32:64].decode('hex'), secure_profile[64:96].decode('hex'), secure_profile[96:128].decode('hex')]


	for block in blocks:
		print block.encode('hex')
		print ecb_decrypt(block, key)

	answer_string = '2d892f62193cff5668eac7cbb7dfd312ee28bd592d461c50910ed99273d72df9fb2e97c187ea16e796831f073283fdc960a26a9c26547f45ace86b952cd2ea49c0452f76d4cc4c89ff7dbde6e1c69fef'
	#print ecb_decrypt(secure_profile, key)
	print decrypt_user_profile(answer_string, key)

"""
Scratch pad for aligning blocks from ciphertext. It is possible to do this without running through the decryption
function, as if there was actually not access. Just line up in 16 byte chunks and keep track of the ciphertext returned.
'#' marks what could not actually be seen, but simply lined up with cipher text.

email=xxxxxxxx@.                 com&uid=10&role=                 admin&uid=10&rol                 email=xxxxxxxxxx
2d892f62193cff5668eac7cbb7dfd312 ee28bd592d461c50910ed99273d72df9 fb2e97c187ea16e796831f073283fdc9 60a26a9c26547f45ace86b952cd2ea49
"""

