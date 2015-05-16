def better_hex_xor(x, y):
	a = '0x' + x
	b = '0x' + y
	m = int(a, base = 0)
	n = int(b, base = 0)
	
	result = format(m^n, 'x')
	
	while len(result) != len(x):
		result = '0' + result

	return result

print better_hex_xor('05', '06')