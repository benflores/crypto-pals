# Solution to Matasano Crypto Challenge 1.1 http://cryptopals.com/sets/1/challenges/1/
# Given a hex string input, convert to base64 output
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

import base64

def hex_raw(hex_phrase):
	return hex_phrase.decode('hex')

def raw_hex(raw_phrase):
	return raw_phrase.encode('hex')

def raw_base64(raw_phrase):
	return base64.b64encode(raw_phrase)

def hex_base64(hex_phrase):
	raw_phrase = hex_raw(hex_phrase)
	return raw_base64(raw_phrase)

def base64_raw(base64_phrase):
	return base64.b64decode(base64_phrase)

def base64_hex(base64_phrase):
	raw_phrase = base64.b64decode(base64_phrase)
	return raw_hex(raw_phrase)

if __name__ == '__main__':
	hex_string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
	print hex_base64(hex_string)