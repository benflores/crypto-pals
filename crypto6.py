# Solution to Matasano Crypto Challenge 1.6 http://cryptopals.com/sets/1/challenges/6/
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

from crypto3 import score_keys #score_keys(cipher_text, frequency_dict, scores, sensitivity)
from crypto5 import decrypt_repeating_key
import crypto1
import base64

def hamming(s1, s2):
    # calculate the hamming/edit distance between two strings (total distance between bits)
    i = 0
    counter = 0

    while (i < len(s1)) and (i < len(s2)):
        c1 = bin(ord(s1[i]))[2:]
        c2 = bin(ord(s2[i]))[2:]
        while len(c1) != len(c2):
            if len(c1) < len(c2):
                c1 = '0' + c1
            elif len(c2) < len(c1):
                c2 = '0' + c2
        for x in range(len(c1)):
            counter += int(c1[x])^int(c2[x])
        i += 1

    return counter

def possible_keysize(cipher, start_range, end_range, block_count):
    # cipher = raw cipher text; start_range/end_range = smallest/largest keysizes to try;
    # block_count = how many blocks to test against for possible keysize
    # this function returns a dictionary containing the hamming "score" of each keysize in the attempted range

    key_dict = {}

    for keysize in range(start_range,end_range):
        block_check = []
        hams = []
        for x in range(0, block_count):
            block_check.append(cipher[keysize*x:keysize*(x+1)])

        for y in range(0, block_count, 2):
            hams.append(hamming(block_check[y], block_check[y+1])/float(keysize))
        avg = sum(hams)

        avg = avg/(block_count/2)

        key_dict[keysize] = avg
    return key_dict


def split_blocks(raw_phrase, key_length):
    # split the cipher text into blocks of equal length, with key_length as the possible block length to try
    block_list = []
    for block in range(0, len(raw_phrase)-1, key_length):
        block_list.append(raw_phrase[block:block+key_length])
    return block_list

def blocks_as_strings(cipher_list, block_length):
    # convert the corresponding position of each block in the ciphertext into a string that can be treated as a 
    # single-character key XORed ciphertext
    string_list = []
    for x in range(block_length):
        position_string = ''
        for block in cipher_list[:len(cipher_list)-1]:
            position_string += block[x]
        string_list.append(position_string)
    return string_list

def build_key(string_list, frequency_values, score_values, sensitivity):
    # for each block string (which is built from corresponding positions in the equal size blocks), run score_keys to return
    # the best fit single-character key value for that position in the key, and build up the key from those values
    key_values = ''
    frequencies = frequency_values
    for block_string in string_list:
        current_scores = {' ': 0,'$': 0, '(': 0, ',': 0, '0': 0, '4': 0, '8': 0, '<': 0, '@': 0, 'D': 0, 'H': 0, 'L': 0, 'P': 0, 'T': 0, 'X': 0, '\\': 0, '`': 0, 'd': 0, 'h': 0, 'l': 0, 'p': 0, 't': 0, 'x': 0, '|': 0, '#': 0, "'": 0, '+': 0, '/': 0, '3': 0, '7': 0, ';': 0, '?': 0, 'C': 0, 'G': 0, 'K': 0, 'O': 0, 'S': 0, 'W': 0, '[': 0, '_': 0, 'c': 0, 'g': 0, 'k': 0, 'o': 0, 's': 0, 'w': 0, '{': 0, '"': 0, '&': 0, '*': 0, '.': 0, '2': 0, '6': 0, ':': 0, '>': 0, 'B': 0, 'F': 0, 'J': 0, 'N': 0, 'R': 0, 'V': 0, 'Z': 0, '^': 0, 'b': 0, 'f': 0, 'j': 0, 'n': 0, 'r': 0, 'v': 0, 'z': 0, '!': 0, '%': 0, ')': 0, '-': 0, '1': 0, '5': 0, '9': 0, '=': 0, 'A': 0, 'E': 0, 'I': 0, 'M': 0, 'Q': 0, 'U': 0, 'Y': 0, ']': 0, 'a': 0, 'e': 0, 'i': 0, 'm': 0, 'q': 0, 'u': 0, 'y': 0, '}': 0, '~': 0, ' ': 0}
        likely_value = score_keys(block_string, frequencies, current_scores, sensitivity)[0]
        key_values += likely_value
    return key_values

def get_key(cipher, start_range, end_range, block_count, k):
    # cipher = raw cipher text; start_range/end_range = smallest/largest keysizes to try;
    # block_count = how many blocks to test against for possible keysize; k = which "best fit" key to attempt
    # as generated by the possible_keysize function (0 is the technical "best fit" - possible_keysize produces)
    # a dictionary of keysizes, which are then reverse sorted by "best fit" in this function
    keysizes = possible_keysize(cipher, start_range, end_range, block_count)
    sorted_keysizes = sorted(keysizes, key=keysizes.get)
    try_key = sorted_keysizes[k]

    cipher_list = split_blocks(cipher, try_key) # take the list of equal length blocks from split_blocks
    string_list = blocks_as_strings(cipher_list, try_key)

    freqtry = {' ': 1, '$': -1, '(': -1, ',': -1, '0': -1, '4': -1, '8': -1, '<': -1, '@': -1, 'D': 0.33483, 'H': 0.47977, 'L': 0.31688, 'P': 0.15187, 'T': 0.71296, 'X': 0.01181, '\\': -1, '`': -1, 'd': 0.33483, 'h': 0.47977, 'l': 0.31688, 'p': 0.15187, 't': 0.71296, 'x': 0.01181, '|': -1, '#': -1, "'": -1, '+': -1, '/': -1, '3': -1, '7': -1, ';': -1, '?': -1, 'C': 0.21902, 'G': 0.15864, 'K': 0.06078, 'O': 0.59101, 'S': 0.49811, 'W': 0.1858, '[': -1, '_': -1, 'c': 0.21902, 'g': 0.15864, 'k': 0.06078, 'o': 0.59101, 's': 0.49811, 'w': 0.1858, '{': -1, '"': -1, '&': -1, '*': -1, '.': -1, '2': -1, '6': -1, ':': -1, '>': -1, 'B': 0.11746, 'F': 0.17541, 'J': 0.01205, 'N': 0.53133, 'R': 0.47134, 'V': 0.077, 'Z': 0.00583, '^': -1, 'b': 0.11746, 'f': 0.17541, 'j': 0.01205, 'n': 0.53133, 'r': 0.47134, 'v': 0.077, 'z': 0.00583, '~': -1, '!': -1, '%': -1, ')': -1, '-': -1, '1': -1, '5': -1, '9': -1, '=': -1, 'A': 0.64297, 'E': 1.0, 'I': 0.54842, 'M': 0.18942, 'Q': 0.00748, 'U': 0.21713, 'Y': 0.15541, ']': -1, 'a': 0.64297, 'e': 1.0, 'i': 0.54842, 'm': 0.18942, 'q': 0.00748, 'u': 0.21713, 'y': 0.15541, '}': -1, ' ': 1}
    scoretry = {'$': 0, '(': 0, ',': 0, '0': 0, '4': 0, '8': 0, '<': 0, '@': 0, 'D': 0, 'H': 0, 'L': 0, 'P': 0, 'T': 0, 'X': 0, '\\': 0, '`': 0, 'd': 0, 'h': 0, 'l': 0, 'p': 0, 't': 0, 'x': 0, '|': 0, '#': 0, "'": 0, '+': 0, '/': 0, '3': 0, '7': 0, ';': 0, '?': 0, 'C': 0, 'G': 0, 'K': 0, 'O': 0, 'S': 0, 'W': 0, '[': 0, '_': 0, 'c': 0, 'g': 0, 'k': 0, 'o': 0, 's': 0, 'w': 0, '{': 0, '"': 0, '&': 0, '*': 0, '.': 0, '2': 0, '6': 0, ':': 0, '>': 0, 'B': 0, 'F': 0, 'J': 0, 'N': 0, 'R': 0, 'V': 0, 'Z': 0, '^': 0, 'b': 0, 'f': 0, 'j': 0, 'n': 0, 'r': 0, 'v': 0, 'z': 0, '!': 0, '%': 0, ')': 0, '-': 0, '1': 0, '5': 0, '9': 0, '=': 0, 'A': 0, 'E': 0, 'I': 0, 'M': 0, 'Q': 0, 'U': 0, 'Y': 0, ']': 0, 'a': 0, 'e': 0, 'i': 0, 'm': 0, 'q': 0, 'u': 0, 'y': 0, '}': 0, '~': 0, ' ': 0}
    
    best_fit_key = build_key(string_list, freqtry, scoretry, 1) 
    return best_fit_key

if __name__ == '__main__':
    f = open('sample_encrypted.txt', 'r') # open('6.txt', 'r')

    cipher_text = f.read()

    raw_cipher = crypto1.hex_raw(cipher_text)

    best_fit_key = get_key(raw_cipher, 2, 41, 12, 0) 

    print best_fit_key
    print
    print decrypt_repeating_key(raw_cipher, best_fit_key)

    f.close()
