# Solution to Matasano Crypto Challenge 1.3 http://cryptopals.com/sets/1/challenges/4/
# Given a string that has been XORed with a key of a single ASCII character, find the key
# This is a work of slow-cooked eggplant brought to you by Benjamin Flores straight from 2015.

def score_keys(cipher_text, frequency_dict, scores, sensitivity):
    i = 32 
    while i < 126: # iterate through ASCII values of all printable characters

        k = 0
        while k < len(cipher_text): # XOR value of each character in encrypted string with current test value i
            c_xor_i = ord(cipher_text[k])^i
            if (c_xor_i < 32) or (c_xor_i > 126):
                scores[chr(i)] -= 1
                k += 1
            elif (c_xor_i >= 32) and (c_xor_i <= 126):
                scores[chr(i)] += frequency_dict[chr(c_xor_i)] 
                #score the possible key with values of english language char freq.
                k += 1
            else:
                break

        i += 1

    key_scores = sorted(scores, key=scores.get)
    highest_key_scores = key_scores[len(key_scores)-sensitivity:len(key_scores)] #10 hardcoded as number of best possible keys - change if needed
    # print highest_key_scores
    return highest_key_scores

#run decryption using best scored possible keys
def possible_decryptions(cipher_text, key_list):
    j = 0
    while j < len(key_list):
        decrypt = ''
        for c in cipher_text:
            c_xor_key = ord(c)^ord(key_list[j])
            decrypt += chr(c_xor_key)
        print 'key:', key_list[j]
        print decrypt
        j += 1
    return 0

if __name__ == '__main__':
    num = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736".decode("hex") # hex decode encrypted string
    frequency_dict = {' ': 1, '"': 0, '$': 0, '&': 0, '(': 0, '*': 0, ',': 0, '.': 0, '0': 0, '2': 0, '4': 0, '6': 0, '8': 0, ':': 0, '<': 0, '>': 0, '@': 0, 'B': 0.11746, 'D': 0.33483, 'F': 0.17541, 'H': 0.47977, 'J': 0.01205, 'L': 0.31688, 'N': 0.53133, 'P': 0.15187, 'R': 0.47134, 'T': 0.71296, 'V': 0.077, 'X': 0.01181, 'Z': 0.00583, '\\': 0, '^': 0, '`': 0, 'b': 0.11746, 'd': 0.33483, 'f': 0.17541, 'h': 0.47977, 'j': 0.01205, 'l': 0.31688, 'n': 0.53133, 'p': 0.15187, 'r': 0.47134, 't': 0.71296, 'v': 0.077, 'x': 0.01181, 'z': 0.00583, '|': 0, '~': 0, '!': 0, '#': 0, '%': 0, "'": 0, ')': 0, '+': 0, '-': 0, '/': 0, '1': 0, '3': 0, '5': 0, '7': 0, '9': 0, ';': 0, '=': 0, '?': 0, 'A': 0.64297, 'C': 0.21902, 'E': 1.0, 'G': 0.15864, 'I': 0.54842, 'K': 0.06078, 'M': 0.18942, 'O': 0.59101, 'Q': 0.00748, 'S': 0.49811, 'U': 0.21713, 'W': 0.1858, 'Y': 0.15541, '[': 0, ']': 0, '_': 0, 'a': 0.64297, 'c': 0.21902, 'e': 1.0, 'g': 0.15864, 'i': 0.54842, 'k': 0.06078, 'm': 0.18942, 'o': 0.59101, 'q': 0.00748, 's': 0.49811, 'u': 0.21713, 'w': 0.1858, 'y': 0.15541, '{': 0, '}': 0}
    scores = {' ': 0, '$': 0, '(': 0, ',': 0, '0': 0, '4': 0, '8': 0, '<': 0, '@': 0, 'D': 0, 'H': 0, 'L': 0, 'P': 0, 'T': 0, 'X': 0, '\\': 0, '`': 0, 'd': 0, 'h': 0, 'l': 0, 'p': 0, 't': 0, 'x': 0, '|': 0, '#': 0, "'": 0, '+': 0, '/': 0, '3': 0, '7': 0, ';': 0, '?': 0, 'C': 0, 'G': 0, 'K': 0, 'O': 0, 'S': 0, 'W': 0, '[': 0, '_': 0, 'c': 0, 'g': 0, 'k': 0, 'o': 0, 's': 0, 'w': 0, '{': 0, '"': 0, '&': 0, '*': 0, '.': 0, '2': 0, '6': 0, ':': 0, '>': 0, 'B': 0, 'F': 0, 'J': 0, 'N': 0, 'R': 0, 'V': 0, 'Z': 0, '^': 0, 'b': 0, 'f': 0, 'j': 0, 'n': 0, 'r': 0, 'v': 0, 'z': 0, '!': 0, '%': 0, ')': 0, '-': 0, '1': 0, '5': 0, '9': 0, '=': 0, 'A': 0, 'E': 0, 'I': 0, 'M': 0, 'Q': 0, 'U': 0, 'Y': 0, ']': 0, 'a': 0, 'e': 0, 'i': 0, 'm': 0, 'q': 0, 'u': 0, 'y': 0, '}': 0, '~': 0}
    key_list = score_keys(num, frequency_dict, scores, 1)
    print possible_decryptions(num, key_list)