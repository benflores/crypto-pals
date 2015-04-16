from crypto7 import ecb_encrypt #(plaintext, key)
from crypto7 import ecb_decrypt #(ciphertext, key)


key = 'YELLOW SUBMARINE'

for x in range(1,33):
	print ecb_encrypt('A'*x, key)