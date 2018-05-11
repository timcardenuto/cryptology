#!/usr/bin/env python
""" Merkle-Hellman Knapsack Cryptosystem """

from __future__ import print_function
import sys


def gcdExtended(a, b):
	if a == 0:
		x = 0
		y = 1
		return b, x, y

	gcd, x1, y1 = gcdExtended(b%a, a)
	x = y1 - int(b/a) * x1
	y = x1
	return gcd, x, y

# extended Eclidean algorithm
def findModularInverse(a, m):
	gcd, x, y = gcdExtended(a, m)
	if gcd != 1:
		print("Inverse doesn't exist")
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
	for idx in range(0,len(plaintext),2):
		i = alphabet.find(plaintext[idx])
		j = alphabet.find(plaintext[idx+1])
		decimal = (26*i)+j
		binary.append(decimalToBinary(decimal))
	return binary

# the Merkle-Hellman encryption function
# B = public key decimals, aka knapsack, length N
# X = plaintext bits, length N
# c = ciphertext decimal
def encrypt(B, X):
	c = 0
	for idx,val in enumerate(X):
		c = c + (val*B[idx])
	return c

# the Merkle-Hellman decryption function
# M = secret modulus
# C = ciphertext decimals
# D = intermediate decrypted decimals, need to be unpacked with easy knapsack A
def decrypt(W_inverse_modM, C, M):
	D = []
	for c in C:
		D.append((W_inverse_modM*c)%M)
	return D

# solves the easy knapsack problem
# A = easy knapsack, super-increasing
# D = decimal values to unpack
def unpackEasyKnapsack(A, D):
	A.reverse()
	plaintext_array = []
	for d in D:
		plaintext = []
		for a in A:
			if d-a > -1:
				plaintext.insert(0,1)
				d = d - a
			else:
				plaintext.insert(0,0)
		plaintext_array.append(plaintext)
	return plaintext_array


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

'''
A = ''
M = ''
W = ''

def setPrivateKeys(_A, _M, _W):
	global A
	A = _A
	global M
	M = _M
	global W
	W = _W
'''

verbose = False	# level 1 output, shows input plaintext, ciphertext, and final decoded plaintext
verbose2 = False # level 2 output, shows pretty much everything
pipe_ciphertext_out = True # only shows raw ciphertext, usevul if you're piping between things

if __name__ == "__main__":
	if verbose: print("Merkle-Hellman Knapsack Cryptosystem")

	# allows you to pipe in plaintext from command line, use stdin if it's full
	if not sys.stdin.isatty():
		input_stream = sys.stdin
		text = [line.strip() for line in input_stream]  # strips off \r\n characters
		plaintext = ''.join(text)  # combines separate lines into single string

	# else use command line args
	elif len(sys.argv) == 2:
		with open(sys.argv[1]) as fh:
			text = fh.readlines()
		text = [line.strip() for line in text]  # strips off \r\n characters
		plaintext = ''.join(text)  # combines separate lines into single string

	else:
		plaintext = 'goddoesnotplaydice'

	# superincreasing set of integers
	A = [3, 5, 10, 19, 41, 79, 161, 320, 641, 1311]
	# integer such that M > sum(A)
	M = 2629
	# integer such that 1 < W < M and gcd(M,W) = 1
	W = 1036

	plaintext = plaintext.replace(" ","") # remove spaces
	if verbose: print("\n### Input plaintext: \n" + plaintext)

	# TODO supposed to include permutation as well?
	B = calculatePublicKey(W, A, M)
	if verbose2: print("\n### Public key: \n" + str(B))

	plainbits_array = encode(plaintext)
	if verbose2: print("\n### Encoded plaintext: \n" + str(plainbits_array))

	ciphertext = []
	for plainbits in plainbits_array:
		ciphertext.append(encrypt(B, plainbits))
	if verbose: print("\n### Ciphertext: \n" + str(ciphertext))
	if pipe_ciphertext_out: print(str(ciphertext))

	W_inverse_modM = findModularInverse(W,M)
	if verbose2: print("\n### W_inverse_modM: \n" + str(W_inverse_modM))

	D = decrypt(W_inverse_modM, ciphertext, M)
	if verbose2: print("\n### Decrypted decimals: \n" + str(D))

	plainbits_array = unpackEasyKnapsack(A, D)
	if verbose2: print("\n### Unpacked plaintext: \n" + str(plainbits_array))

	plaintext = ''
	for binary in plainbits_array:
		plaindecimal = BigEndianBinaryToDecimal(binary)
		digraph = findDigraph(plaindecimal)
		if len(digraph)==1:
			plaintext = plaintext + digraph[0]
		else:
			if verbose2: print("Multiple possible digraphs: " + str(digraph))
	if verbose: print("\n### Decoded plaintext: \n" + str(plaintext) + "\n")
