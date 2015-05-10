y0 = 2443250962
print ' '*(48-len(bin(y0))) + bin(y0)[2:], 'y0'
a0 = y0 >> 3
print ' '*(48-len(bin(a0))) + bin(a0)[2:], 'y0 >> 3'
y1 = y0 ^ a0
print ' '*(48-len(bin(y1))) + bin(y1)[2:], 'y1 = y0 ^ (y0 >> 3)'
a1 = y1 << 7
print ' '*(48-len(bin(a1))) + bin(a1)[2:], 'y1 << 7'
b0 = 0x9d2c5680
print ' '*(48-len(bin(b0))) + bin(b0)[2:], '0x9d2c5680'
a2 = a1 & b0
print ' '*(48-len(bin(a2))) + bin(a2)[2:], '(y1 << 7) & 0x9d2c5680'
y2 = y1 ^ a2
print ' '*(48-len(bin(y2))) + bin(y2)[2:], 'y2 = y1 ^ ((y1 << 7) & 0x9d2c5680)'
a3 = y2 << 15
print ' '*(48-len(bin(a3))) + bin(a3)[2:], 'y2 << 15'
b1 = 0xefc60000
print ' '*(48-len(bin(b0))) + bin(b1)[2:], '0xefc60000'
a4 = a3 & b1
print ' '*(48-len(bin(a4))) + bin(a4)[2:], '(y2 << 15) & 0xefc60000'
y3 = y2 ^ a4
print ' '*(48-len(bin(y3))) + bin(y3)[2:], 'y3 = y2 ^ ((y2 << 15) & 0xefc60000)'
a5 = y3 >> 18
print ' '*(48-len(bin(a5))) + bin(a5)[2:], 'y3 >> 18'
y4 = y3 ^ a5
print ' '*(48-len(bin(y4))) + bin(y4)[2:], 'y3 ^ (y3 >> 18)'
w0 = y4
print w0
print ' '*(48-len(bin(w0))) + bin(w0)[2:], 'w0'
z0 = w0 >> 18
print ' '*(48-len(bin(z0))) + bin(z0)[2:], 'w0 >> 18'
w1 = w0 ^ z0
print ' '*(48-len(bin(w1))) + bin(w1)[2:], 'w1 = w0 ^ (w0 >> 18)'
z1 = w1 << 15
print ' '*(48-len(bin(z1))) + bin(z1)[2:], 'w1 << 15'
print ' '*(48-len(bin(b0))) + bin(b1)[2:], '0xefc60000'
z2 = z1 & b1
w2 = w1 ^ z2
print ' '*(48-len(bin(z2))) + bin(z2)[2:], '(w1 << 15) & 0xefc60000'
print ' '*(48-len(bin(w2))) + bin(w2)[2:], 'w2 = w1 ^ (w1 << 15)'
w3 = w2 << 15
print ' '*(48-len(bin(w3))) + bin(w3)[2:], 'w3 = (w2 << 15)'
c1 = w3 << 7
print ' '*(48-len(bin(c1))) + bin(c1)[2:], 'w3 << 7'
print ' '*(48-len(bin(b0))) + bin(b0)[2:], '0x9d2c5680'
d0 = c1 & b0
print ' '*(48-len(bin(d0))) + bin(d0)[2:], '(w3 << 7) & 0x9d2c5680'
z3 = w3 ^ (c1 & b0)
print ' '*(48-len(bin(z3))) + bin(z3)[2:], 'z3 = w3 ^ ((w3 << 7) & 0x9d2c5680'
z4 = w3 ^ ((z3 << 7) & b0)
print ' '*(48-len(bin(z4))) + bin(z4)[2:], 'z4 = w3 ^ ((z3 << 7) & b0)'
z5 = w3 ^ ((z4 << 7) & b0)
print ' '*(48-len(bin(z5))) + bin(z5)[2:], 'z5 = w3 ^ ((z4 << 7) & b0)'
w4 = (z5 << 7) & b0
print ' '*(48-len(bin(w4))) + bin(w4)[2:], 'z5 = w3 ^ ((z4 << 7) & b0)'
w5 = w4 ^ (w4 >> 11)
print ' '*(48-len(bin(w5))) + bin(w5)[2:], 'z5 = w3 ^ ((z4 << 7) & b0)'
w6 = w4 ^ (w5 >> 11)
print ' '*(48-len(bin(w6))) + bin(w6)[2:], 'z5 = w3 ^ ((z4 << 7) & b0)'

