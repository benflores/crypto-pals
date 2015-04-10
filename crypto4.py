# Solution Matasano Crypto Challenge 1.4 http://cryptopals.com/sets/1/challenges/4/
# Use key scoring and decryption tools built in 1.3 to find which line in text file
# was encrypted using a single character XOR
# This solution requires a sensitivity of just the highest rated key to find the correct line,
# but requires human review to identify which line produces an English-language result.
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

from crypto3 import score_keys
from crypto3 import possible_decryptions

if __name__ == '__main__':
    text = open('4.txt', 'r')
    for n,line in enumerate(text):
        frequency_dict = {' ': 1, '"': 0, '$': 0, '&': 0, '(': 0, '*': 0, ',': 0, '.': 0, '0': 0, '2': 0, '4': 0, '6': 0, '8': 0, ':': 0, '<': 0, '>': 0, '@': 0, 'B': 0.11746, 'D': 0.33483, 'F': 0.17541, 'H': 0.47977, 'J': 0.01205, 'L': 0.31688, 'N': 0.53133, 'P': 0.15187, 'R': 0.47134, 'T': 0.71296, 'V': 0.077, 'X': 0.01181, 'Z': 0.00583, '\\': 0, '^': 0, '`': 0, 'b': 0.11746, 'd': 0.33483, 'f': 0.17541, 'h': 0.47977, 'j': 0.01205, 'l': 0.31688, 'n': 0.53133, 'p': 0.15187, 'r': 0.47134, 't': 0.71296, 'v': 0.077, 'x': 0.01181, 'z': 0.00583, '|': 0, '~': 0, '!': 0, '#': 0, '%': 0, "'": 0, ')': 0, '+': 0, '-': 0, '/': 0, '1': 0, '3': 0, '5': 0, '7': 0, '9': 0, ';': 0, '=': 0, '?': 0, 'A': 0.64297, 'C': 0.21902, 'E': 1.0, 'G': 0.15864, 'I': 0.54842, 'K': 0.06078, 'M': 0.18942, 'O': 0.59101, 'Q': 0.00748, 'S': 0.49811, 'U': 0.21713, 'W': 0.1858, 'Y': 0.15541, '[': 0, ']': 0, '_': 0, 'a': 0.64297, 'c': 0.21902, 'e': 1.0, 'g': 0.15864, 'i': 0.54842, 'k': 0.06078, 'm': 0.18942, 'o': 0.59101, 'q': 0.00748, 's': 0.49811, 'u': 0.21713, 'w': 0.1858, 'y': 0.15541, '{': 0, '}': 0}
        scores = {' ': 0, '$': 0, '(': 0, ',': 0, '0': 0, '4': 0, '8': 0, '<': 0, '@': 0, 'D': 0, 'H': 0, 'L': 0, 'P': 0, 'T': 0, 'X': 0, '\\': 0, '`': 0, 'd': 0, 'h': 0, 'l': 0, 'p': 0, 't': 0, 'x': 0, '|': 0, '#': 0, "'": 0, '+': 0, '/': 0, '3': 0, '7': 0, ';': 0, '?': 0, 'C': 0, 'G': 0, 'K': 0, 'O': 0, 'S': 0, 'W': 0, '[': 0, '_': 0, 'c': 0, 'g': 0, 'k': 0, 'o': 0, 's': 0, 'w': 0, '{': 0, '"': 0, '&': 0, '*': 0, '.': 0, '2': 0, '6': 0, ':': 0, '>': 0, 'B': 0, 'F': 0, 'J': 0, 'N': 0, 'R': 0, 'V': 0, 'Z': 0, '^': 0, 'b': 0, 'f': 0, 'j': 0, 'n': 0, 'r': 0, 'v': 0, 'z': 0, '!': 0, '%': 0, ')': 0, '-': 0, '1': 0, '5': 0, '9': 0, '=': 0, 'A': 0, 'E': 0, 'I': 0, 'M': 0, 'Q': 0, 'U': 0, 'Y': 0, ']': 0, 'a': 0, 'e': 0, 'i': 0, 'm': 0, 'q': 0, 'u': 0, 'y': 0, '}': 0, '~': 0}
        cipher_text = line.strip().decode('hex')
        key_list = score_keys(cipher_text, frequency_dict, scores, 1)
        print cipher_text
        print possible_decryptions(cipher_text, key_list)
        print '***'
