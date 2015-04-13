# Solution to Matasano Crypto Challenge 2.9 http://cryptopals.com/sets/2/challenges/9/
# Given a cipher text and a block length, pad the cipher text so that it is divisible
# into equal size blocks of the given block length without remainder.

def pad(cipher_text, block_length):
	
	class BlockSizeError(Exception):
		# Raise exception if block length <2 or block length >255
		pass
		
	if (block_length < 2) or (block_length > 255):
		raise BlockSizeError('Invalid block size')
		
	padded_cipher_text = cipher_text
	padding_length = block_length - (len(cipher_text) % block_length)
	
	#print padding_length
	#print chr(padding_length)

	if padding_length != 0:
		padded_cipher_text += chr(padding_length)*padding_length
	
	#print padded_cipher_text.encode('hex')
	return padded_cipher_text
