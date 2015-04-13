# Solution to Matasano Crypto Challenge 1.2 http://cryptopals.com/sets/1/challenges/2/
# Given two hex string inputs of equal length, XOR and return result
# Bonus - result translation to ASCII
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

from crypto1 import hex_raw

def hex_xor(x, y):
	a = '0x' + x
	b = '0x' + y
	m = int(a, base = 0)
	n = int(b, base = 0)

	return format(m^n, 'x')

def front_padding(hex_string):
	front_padded_hex_string = ''
	if len(hex_string) < 32:
		padding = 32 - len(hex_string)
		front_padded_hex_string += '0'*padding
		front_padded_hex_string += hex_string
		return front_padded_hex_string
	else:
		return hex_string


if __name__ == '__main__':
	result = hex_xor('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965')
	print result

	check = hex_xor('756e6b79206d75736963200a04040404', '')