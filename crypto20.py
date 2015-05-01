
from crypto1 import hex_raw 
from crypto2 import hex_xor
import crypto6 #(cipher, start_range, end_range, block_count, k)
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
	
	raw_cipher = hex_raw(cipher_text)
	
	best_fit_key = crypto6.get_key(raw_cipher, 53, 54, 24, 0) 
	print best_fit_key
	hex_key = best_fit_key.encode('hex')
	print hex_key
	
	# key '387e42576742277e3b7b317e7e7e307e494d7e7e647e767e7e7e263b377e5e7e7e4e7e5b677e7e787e7e7e3a7e337e4a392f7e7e7e'
	key = '38db42576742277e3b7b317e7e7e307e494d7e7e647e767e7e7e263b377e5e7e7e4e7e5b677e7e787e7e7e3a7e337e4a392f7e7e7e'
	freqtry = {' ': 1, '$': -1, '(': -1, ',': -1, '0': -1, '4': -1, '8': -1, '<': -1, '@': -1, 'D': 0.33483, 'H': 0.47977, 'L': 0.31688, 'P': 0.15187, 'T': 0.71296, 'X': 0.01181, '\\': -1, '`': -1, 'd': 0.33483, 'h': 0.47977, 'l': 0.31688, 'p': 0.15187, 't': 0.71296, 'x': 0.01181, '|': -1, '#': -1, "'": -1, '+': -1, '/': -1, '3': -1, '7': -1, ';': -1, '?': -1, 'C': 0.21902, 'G': 0.15864, 'K': 0.06078, 'O': 0.59101, 'S': 0.49811, 'W': 0.1858, '[': -1, '_': -1, 'c': 0.21902, 'g': 0.15864, 'k': 0.06078, 'o': 0.59101, 's': 0.49811, 'w': 0.1858, '{': -1, '"': -1, '&': -1, '*': -1, '.': -1, '2': -1, '6': -1, ':': -1, '>': -1, 'B': 0.11746, 'F': 0.17541, 'J': 0.01205, 'N': 0.53133, 'R': 0.47134, 'V': 0.077, 'Z': 0.00583, '^': -1, 'b': 0.11746, 'f': 0.17541, 'j': 0.01205, 'n': 0.53133, 'r': 0.47134, 'v': 0.077, 'z': 0.00583, '~': -1, '!': -1, '%': -1, ')': -1, '-': -1, '1': -1, '5': -1, '9': -1, '=': -1, 'A': 0.64297, 'E': 1.0, 'I': 0.54842, 'M': 0.18942, 'Q': 0.00748, 'U': 0.21713, 'Y': 0.15541, ']': -1, 'a': 0.64297, 'e': 1.0, 'i': 0.54842, 'm': 0.18942, 'q': 0.00748, 'u': 0.21713, 'y': 0.15541, '}': -1, ' ': 1}
	scoretry = {'$': 0, '(': 0, ',': 0, '0': 0, '4': 0, '8': 0, '<': 0, '@': 0, 'D': 0, 'H': 0, 'L': 0, 'P': 0, 'T': 0, 'X': 0, '\\': 0, '`': 0, 'd': 0, 'h': 0, 'l': 0, 'p': 0, 't': 0, 'x': 0, '|': 0, '#': 0, "'": 0, '+': 0, '/': 0, '3': 0, '7': 0, ';': 0, '?': 0, 'C': 0, 'G': 0, 'K': 0, 'O': 0, 'S': 0, 'W': 0, '[': 0, '_': 0, 'c': 0, 'g': 0, 'k': 0, 'o': 0, 's': 0, 'w': 0, '{': 0, '"': 0, '&': 0, '*': 0, '.': 0, '2': 0, '6': 0, ':': 0, '>': 0, 'B': 0, 'F': 0, 'J': 0, 'N': 0, 'R': 0, 'V': 0, 'Z': 0, '^': 0, 'b': 0, 'f': 0, 'j': 0, 'n': 0, 'r': 0, 'v': 0, 'z': 0, '!': 0, '%': 0, ')': 0, '-': 0, '1': 0, '5': 0, '9': 0, '=': 0, 'A': 0, 'E': 0, 'I': 0, 'M': 0, 'Q': 0, 'U': 0, 'Y': 0, ']': 0, 'a': 0, 'e': 0, 'i': 0, 'm': 0, 'q': 0, 'u': 0, 'y': 0, '}': 0, '~': 0, ' ': 0}

	# print repeating_hex_xor(cipher_text[:len(key)*2], key).decode('hex')
	cipher_list = crypto6.split_blocks(raw_cipher, 53)
	string_list = crypto6.blocks_as_strings(cipher_list, 53)
	best_fit_key = crypto6.build_key(string_list, freqtry, scoretry, 0) 
	print best_fit_key

	result = repeating_hex_xor(best_fit_key.encode('hex')[:106], cipher_text[:106])
	print result
	print result.decode('hex')
	

	
	f.close()
