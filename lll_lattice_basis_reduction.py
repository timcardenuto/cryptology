#!/usr/bin/env python

from liblll import *


# This reads the binary from MSB left to LSB right (big endian)
def BigEndianBinaryToDecimal(binary):
	b = list(binary)	# actually copy, not reference since we're mucking it up
	b.reverse()
	decimal = 0
	for idx,val in enumerate(b):
		decimal = decimal + val*pow(2,idx)
	return decimal


# This part assumes this is how the human readable text is encoded, could be done a different way.
def decode(bits_array):
	text = ''
	for bits in bits_array:
		decimal = BigEndianBinaryToDecimal(bits)
		digraph = findDigraph(decimal)
		if len(digraph)==1:
			text = text + digraph[0]
		else:
			print "Multiple possible digraphs: " + str(digraph)
	return text

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


# Included as a check on LLL output, should be able to recreate cipherdecimals from plainbits
# Bit and Key size must be equal
def encrypt(bits, key):
	decimal = 0
	for idx,val in enumerate(bits):
		decimal = decimal + (val*key[idx])
	return decimal



if __name__ == "__main__":

	# Given public key and ciphertext (decimal values)
	publickey = [479, 2551, 2473, 1281, 412, 345, 1169, 266, 1568, 1632]
	ciphertext = [5622, 3258, 4589, 8349, 9224, 7001, 1514, 3460, 1926]

	# recover plaintext through LLL algorithm
	plainbits_array = []
	for cipherdecimal in ciphertext:
		M = create_matrix_from_knapsack(publickey,cipherdecimal)
		M_reduced = lll_reduction(M)
		plainbits = best_vect_knapsack(M_reduced)

		# check output by re-encrypting
		if encrypt(plainbits[:10], publickey) != cipherdecimal:
			print "Error in calculation, recovered plaintext '" + ''.join(str(x) for x in plainbits) + "' does not encrypt to ciphertext '" + str(cipherdecimal) + "'"

		#print "binary from LLL " + str(plainbits)
		plaintext = decode([plainbits[:10]])
		print plaintext
		plainbits_array.append(plainbits[:10])



	print ""
	plaintext = decode(plainbits_array)
	print "Plaintext: " + str(plaintext) + "\n"
