# Solution to Matasano Crypto Challenge 1.2 http://cryptopals.com/sets/1/challenges/2/
# Given two hex string inputs of equal length, XOR and return result
# Bonus - result translation to ASCII

from crypto1 import hex_raw

def hex_xor(x, y):
	a = '0x' + x
	b = '0x' + y
	m = int(a, base = 0)
	n = int(b, base = 0)
	return format(m^n, 'x')

result = hex_xor('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965')

#print result

print hex_raw(result)