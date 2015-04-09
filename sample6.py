import crypto6

if __name__ == '__main__':
    f = open('sample_encrypted.txt', 'r') # open('6.txt', 'r')

    cipher_text = f.read()

    raw_cipher = crypto6.hex_raw(cipher_text)

    best_fit_key = crypto6.get_key(raw_cipher, 2, 41, 12, 0) 

    print best_fit_key
    print
    print crypto6.decrypt_repeating_key(raw_cipher, best_fit_key)

    f.close()