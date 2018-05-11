#!/usr/bin/env python
import math


def decimalToBinary(decimal):
	# find # of bits needed to fit decimal value
	msb_value = 0
	count = 0
	while (msb_value < decimal):
		count += 1
		msb_value = pow(2,count)

	binary = []
	for i in reversed(range(count)):
		if decimal >= pow(2,i):
			binary.append(1)
			decimal = decimal - pow(2,i)
		else:
			binary.append(0)
	return binary

# repeated squaring method
# a^k mod n
def modularExponentiation(a,k,n):
	kbinary = decimalToBinary(k)
	kbinary.reverse()

	b = 1
	A = a
	if kbinary[0] == 1:
		b = a

	for i in range(len(kbinary))[1:]:
		A = (A*A)%n
		if kbinary[i] == 1:
			b = (A*b)%n
	return b


def gcdExtended(a, b):
	if a == 0:
		x = 0
		y = 1
		return b, x, y

	gcd, x1, y1 = gcdExtended(b%a, a)
	x = y1 - (b/a) * x1
	y = x1
	return gcd, x, y

# a^-1 mod m
def findModularInverse(a, m):
	# extended Eclidean algorithm
	gcd, x, y = gcdExtended(a, m)
	if gcd != 1:
		res = ''
	else:
		res = (x%m + m) % m
	return res


def decrypt(p,a,ciphertext_pair):
	temp1 = modularExponentiation(ciphertext_pair[0],(p-1-a),p)
	plaintext = temp1 * ciphertext_pair[1]%p
	return plaintext


# In this example, the decimal values are encoded/decoded a particular way,
# but this does not NEED to be the way it's done
# Each decimal = 3 letters
def decode(decimal):
	if decimal - 17575 > 0:
		print "Decimal out-of-bounds for decoder"
		return '???'

	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	letters = []
	temp = 0
	count = 0
	while temp <= decimal:
		temp += 676
		count += 1
	letters.append(alphabet[count-1])
	decimal = decimal - (temp-676)

	temp = 0
	count = 0
	while temp <= decimal:
		temp += 26
		count += 1
	letters.append(alphabet[count-1])
	decimal = decimal - (temp-26)

	letters.append(alphabet[decimal%26])
	return letters


def decrypt_signature(m1,m2,s1,s2,p):
	temp1 = (m1-m2)%(p-1)
	temp2 = findModularInverse((s1-s2),(p-1))
	k = (temp1*temp2) % (p-1)
	return k


if __name__ == "__main__":
	# Problem 6.9 in Stinson's "Cryptography: Theory and Practice Third Edition"
	print "\n#### ElGammal Cryptosystem Example"

	# public key
	p = 31847
	alpha = 5
	beta = 18074
	# private key
	a = 7899

	ciphertext = [[3781,14409],[31552,3930],[27214,15442]]
	print "Ciphertext:"
	print ciphertext


	plaintext = []
	for ciphertext_pair in ciphertext:
		plaindecimal = decrypt(p,a,ciphertext_pair)
		plaintext.extend(decode(plaindecimal))

	print "Plaintext:"
	print ''.join(plaintext)

	# Made up problem, assuming 2 messages use same key for each signature"
	print "\n#### ElGammal Signature Scheme Example"
	# public keys
	p = 31847
	alpha = 5
	beta = 25703

	# intercepted messages and signatures
	m1 = 8990
	sig = [23972,31396]
	r = 23972
	s1 = 31396
	m2 = 31415
	sig = [23972,20481]
	s2 = 20481

	k = decrypt_signature(m1,m2,s1,s2,p)
	print "Calculated Signature Key:"
	print k

	# check
	rtest = modularExponentiation(alpha,k,p)
	if rtest==r:
		print "Success"
	else:
		print rtest
