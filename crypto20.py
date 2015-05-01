
from crypto1 import hex_raw 
from crypto2 import hex_xor
from crypto6 import get_key #(cipher, start_range, end_range, block_count, k)
from crypto5 import decrypt_repeating_key #(ciphertext, key)
from crypto19 import ctr_texts #(plaintext_file, ciphertext_file)

def repeating_hex_xor(text, key):

	result = ''
	key_length = len(key)
	i = 0 
	while (i * key_length) < len(text):
		result += hex_xor(text[i*key_length:(i*key_length)+key_length], key)
		i += 1
	return result


if __name__ == '__main__':

	"""
	plaintext_file = open('20.txt', 'r')
	ciphertext_file = open('20_ciphertexts.txt', 'r')
	truncated_file = open('20_truncated.txt', 'w+')

	# key = 69ba5979e97a34f8e7ec8641ae46c353 (don't use this! not even to check!)
	# ctr_texts(plaintext_file, ciphertext_file)

	line_lengths = []

	for line in ciphertext_file:
		line_lengths.append(len(line.strip()))

	shortest_line = sorted(line_lengths)[0]
	print shortest_line #106

	ciphertext_file.seek(0)
	for line in ciphertext_file:
		truncated_file.write(line[:shortest_line])

	plaintext_file.close()
	ciphertext_file.close()
	truncated_file.close()
	"""

	f = open('20_truncated.txt', 'r')

	
	cipher_text = f.read()
	"""
	raw_cipher = hex_raw(cipher_text)

	best_fit_key = get_key(raw_cipher, 2, 64, 64, 0) 

	hex_key = best_fit_key.encode('hex')
	print hex_key
	"""
	# key '387e42576742277e3b7b317e7e7e307e494d7e7e647e767e7e7e263b377e5e7e7e4e7e5b677e7e787e7e7e3a7e337e4a392f7e7e7e'
	key = '38db42576742277e3b7b317e7e7e307e494d7e7e647e767e7e7e263b377e5e7e7e4e7e5b677e7e787e7e7e3a7e337e4a392f7e7e7e'

	print repeating_hex_xor(cipher_text[:len(key)*2], key).decode('hex')
	
	for x in range(256):
		test_length = 4
		test_value = chr(x).encode('hex')
		test_key = key[:test_length-2] + test_value
		print hex_xor(cipher_text[:test_length], test_key).decode('hex'), test_key
	
	f.close()
