#!/usr/bin/env python
""" Merkle-Hellman Knapsack Encryption System Example """

def gcdExtended(a, b):
	if a == 0:
		x = 0
		y = 1
		return b, x, y

	gcd, x1, y1 = gcdExtended(b%a, a)
	x = y1 - (b/a) * x1
	y = x1
	return gcd, x, y


def findModularInverse(a, m):
	# extended Eclidean algorithm
	gcd, x, y = gcdExtended(a, m)
	if gcd != 1:
		print "Inverse doesn't exist"
		res = ''
	else:
		res = (x%m + m) % m
	return res


def calculatePublicKey(W, A, M):
	publickey = []
	for a in A:
		publickey.append((W*a)%M)
	return publickey


def decimalToBinary(decimal):
	binary = []
	for i in reversed(range(10)):
		if decimal >= pow(2,i):
			binary.append(1)
			decimal = decimal - pow(2,i)
		else:
			binary.append(0)
	return binary


# encodes using the digraphs ij, with equation (26*i)+j = decimal
def encode(plaintext):
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	binary = []
	for idx in xrange(0,len(plaintext),2):
		i = alphabet.find(plaintext[idx])
		j = alphabet.find(plaintext[idx+1])
		decimal = (26*i)+j
		binary.append(decimalToBinary(decimal))
	return binary


def encrypt(B, X):
	c = 0
	for idx,val in enumerate(X):
		c = c + (val*B[idx])
	return c


def decrypt(W_inverse_modM, ciphertext, M):
	knapsack = []
	for c in ciphertext:
		knapsack.append((W_inverse_modM*c)%M)
	return knapsack


def decodeKnapsack(A, knapsack):
	A.reverse()
	result = []
	for k in knapsack:
		#print "knapsack value: " + str(k)
		digraph = []
		for a in A:
			if k-a > -1:
				digraph.insert(0,1)
				k = k - a
			else:
				digraph.insert(0,0)
			#print k
		#print digraph
		result.append(digraph)
	return result


# This reads the binary from MSB left to LSB right (big endian)
def BigEndianBinaryToDecimal(binary):
	b = list(binary)	# actually copy, not reference since we're mucking it up
	b.reverse()
	decimal = 0
	for idx,val in enumerate(b):
		decimal = decimal + val*pow(2,idx)
	return decimal


# (26*i) + j = decimal
# we can search for possible pairs by subtracting j, guessing 25 thru 0, dividing by 26
# and tracking results that are NOT fractions. These pairs are viable.
def findDigraph(decimal):
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	guess = []
	for j in range(26):
		i = (decimal - j) / 26.0
		if i.is_integer():
			guess.append(alphabet[int(i)]+alphabet[int(j)])
	return guess


if __name__ == "__main__":
	print "Merkle-Hellman Knapsack System Example"
	# superincreasing set of integers
	A = [3, 5, 10, 19, 41, 79, 161, 320, 641, 1311]
	# integer such that M > sum(A)
	M = 2629
	# integer such that 1 < W < M and gcd(M,W) = 1
	W = 1036

	W_inverse_modM = findModularInverse(W,M)
	#print W_inverse_modM

	# TODO supposed to include permutation as well?
	B = calculatePublicKey(W, A, M)


	pt = 'goddoesnotplaydice'
	pb = encode(pt)
	print pb
	ciphertext = []
	for p in pb:
		ciphertext.append(encrypt(B, p))

	# was originally given ciphertext instead of plaintext for this problem
	#ciphertext = [5622, 3258, 4589, 8349, 9224, 7001, 1514, 3460, 1926]
	print "\nCiphertext: " + str(ciphertext)

	knapsack = decrypt(W_inverse_modM, ciphertext, M)
	#print knapsack

	plainbits = decodeKnapsack(A, knapsack)
	#print plainbits

	plaintext = ''
	for binary in plainbits:
		plaindecimal = BigEndianBinaryToDecimal(binary)
		digraph = findDigraph(plaindecimal)
		if len(digraph)==1:
			plaintext = plaintext + digraph[0]
		else:
			print "Multiple possible digraphs: " + str(digraph)

	print "Plaintext: " + str(plaintext) + "\n"
