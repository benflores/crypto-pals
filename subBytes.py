f = open('sbox.txt', 'r')

s_box = []

for i in xrange(16):
	row = (f.readline().strip()).split()
	s_box.append(row)

for row in s_box:
	print row
	
f.close()