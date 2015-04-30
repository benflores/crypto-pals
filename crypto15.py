# Solution to Matasano Crypto Challenge 2.15 http://cryptopals.com/sets/2/challenges/15/
# PKCS#7 Padding Validation

class PaddingValueError(Exception):
	# Exception raised for padding value errors
	pass

def validate_padding(plaintext):
	# Detect and remove padding
	padding_amount = ord(plaintext[len(plaintext)-1])

	correct_padding = chr(padding_amount) * padding_amount
	actual_padding = plaintext[len(plaintext) - padding_amount:]

	if correct_padding != actual_padding:
		raise PaddingValueError('Invalid Padding')
		return False
	else:
		return True

def strip_padding(plaintext):
	if validate_padding(plaintext):
		# Detect and remove padding
		padding_amount = ord(plaintext[len(plaintext)-1])
		plaintext = plaintext[:len(plaintext) - padding_amount]
		return plaintext

if __name__ == '__main__':
	print strip_padding("ICE ICE BABY\x04\x04\x04\x04")