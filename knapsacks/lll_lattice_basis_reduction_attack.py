#!/usr/bin/env python
""" Lenstra–Lenstra–Lovász lattice basis reduction algorithm wrapper
	for Merkle-Hellman Knapsack encrypted ciphertext
"""

from __future__ import print_function
import sys
from liblll import *
from copy import deepcopy

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
			print("Multiple possible digraphs: " + str(digraph))
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


# The matrix formats expected are different for different libraries,
# this translates liblll format to that expected by ntl and fplll
def fixMatrixForLLL(M):
	# guy wrote liblll to use Fraction class, even though they're all over 1... this converts it back to normal matrix
	nonFracMatrix = deepcopy(M)
	for row in range(len(M)):
		for column in range(len(M[0])):
			nonFracMatrix[row][column] = int(M[row][column]*1.0)
	# ... and this rotates it to match what most other implementations of LLL expect
	for row in range(len(M)-1):
		nonFracMatrix[len(M)-1].insert((len(nonFracMatrix[len(M)-1])-1),0)	# add zeros to bottom row
		nonFracMatrix[row].pop(len(nonFracMatrix[row])-1)	# get rid of last zero of each other row
		nonFracMatrix[row].append(nonFracMatrix[len(M)-1].pop(0))	# pop first element from bottom row and append to new row
	return nonFracMatrix


verbose = True	# level 1 output, shows input plaintext, ciphertext, public key, and final decoded plaintext
verbose2 = False # level 2 output, shows pretty much everything
pipe_plaintext_out = True # only shows raw plaintext output, useful if you're piping between things


if __name__ == "__main__":
	if verbose: print("LLL Attack on Merkle-Hellman Knapsack Cryptosystem")

	# allows you to pipe in plaintext from command line, use stdin if it's full
	if not sys.stdin.isatty():
		input_stream = sys.stdin
		text = [line.strip() for line in input_stream]  # strips off \r\n characters
		cipherstring = ''.join(text)  # combines separate lines into single string
		cipherstring = cipherstring.replace(" ","") # remove spaces
		cipherstring = cipherstring[1:] # strip left '['
		cipherstring = cipherstring[:len(cipherstring)-1] # strip right ']'
		ciphertext = cipherstring.split(',') # strip ',', add each element to array
		ciphertext = [int(x) for x in ciphertext] # turn into int values

	# else use command line args
	elif len(sys.argv) == 2:
		with open(sys.argv[1]) as fh:
			text = fh.readlines()
		text = [line.strip() for line in text]  # strips off \r\n characters
		cipherstring = ''.join(text)  # combines separate lines into single string
		cipherstring = cipherstring.replace(" ","") # remove spaces
		cipherstring = cipherstring[1:] # strip left '['
		cipherstring = cipherstring[:len(cipherstring)-1] # strip right ']'
		ciphertext = cipherstring.split(',') # strip ',', add each element to array
		ciphertext = [int(x) for x in ciphertext] # turn into int values

	else:
		ciphertext = [8960, 2304, 7592, 9799, 4839, 2192, 4652, 4940, 6233, 5346, 7166,
					  8960, 5041, 7656, 4595, 7366, 6233, 5612, 5734, 8960, 2038, 5745,
					  1980, 4797, 2313, 6221, 8960, 6328, 1090, 3067, 3832, 6075, 8497,
					  2849, 10674,5238, 3545, 2862, 5764, 7366, 8484, 7390, 8630, 6142,
					  9454, 5238, 6064, 3872, 5745, 7001, 1568, 7299, 5734, 5899, 6075,
					  6221, 5933, 4244, 8518, 4443, 2038, 6142, 5967, 3832, 1693, 8497,
					  5673, 5899, 3760, 7819, 1913, 6221, 7166, 5210, 6914, 2313, 3067,
					  3460, 745,  1913, 4244, 9799, 2862, 6142, 8960, 3545, 1760, 11019,
					  5024, 4595, 1236, 2517, 2885, 4041, 9372, 5967, 8484, 4365, 4443,
					  4775, 2862, 5126, 10183,8518, 7166, 7166, 3151, 6914, 479,  6592,
					  6075, 5798, 4430, 8896, 7390, 5064, 2725, 6233, 8960, 4839, 8497,
					  5064, 8139, 6062, 3561, 4797, 2111, 4531, 3415, 479,  5758, 6062,
					  1514, 8960, 5504, 4365, 2192, 5346, 8497, 2885, 8960, 4839, 6221,
					  3460, 8551, 7247, 4099, 8630, 2795, 4244, 5226, 6062, 2885, 2026,
					  5764, 8958, 3936, 4290, 7886, 5126, 8630, 10674,5997, 3686, 5346,
					  3628, 10183,1913, 6221, 8784, 4369, 7366, 2517, 6075, 6221, 5024,
					  10416,7873, 6085, 10262,4024, 5635, 8085, 8896, 7390, 8960, 4839,
					  2038, 6142, 5064, 745,  4775, 5064, 5764, 2038, 8960, 4839, 5622,
					  4477, 4826, 7474, 8201, 5967, 8784, 2725, 5899, 8896, 7390, 7656,
					  5540, 3128, 6018, 5758, 8960, 5238, 5933, 6555, 7166, 8497, 8960,
					  5504, 2862, 1926, 3067, 1693, 1898, 6407, 5520, 4041, 6011, 5871,
					  1977, 2817, 2885]

	if verbose: print("\n### Using ciphertext: \n"+str(ciphertext))
	# Given public key and ciphertext (decimal values)
	publickey = [479, 2551, 2473, 1281, 412, 345, 1169, 266, 1568, 1632]
	if verbose: print("\n### Using publickey: \n"+str(publickey))

	# recover plaintext through LLL algorithm
	plainbits_array = []
	plaintext_array = []
	curiousciphers = []
	for cipherdecimal in ciphertext:

		M = create_matrix_from_knapsack(publickey,cipherdecimal)

		nonFracMatrix = fixMatrixForLLL(M)
		if verbose2: print("\n### Matrix to use for LLL reduction: \n"+str(nonFracMatrix))

		M_reduced = lll_reduction(M)
		plainbits = best_vect_knapsack(M_reduced)

		# check output by re-encrypting
		if encrypt(plainbits[:10], publickey) != cipherdecimal:
			if verbose: print("Error in calculation, recovered plaintext '" + ''.join(str(x) for x in plainbits) + "' does not encrypt to ciphertext '" + str(cipherdecimal) + "'")
			curiousciphers.append(cipherdecimal)

		if verbose2: print("\n### Binary from LLL: \n" + str(plainbits))
		temppt = decode([plainbits[:10]])
		#if sum(plainbits[:10]) == 0:
		if temppt == 'aa':
			plaintext_array.extend('--')
		else:
			plaintext_array.extend(temppt)
		#plainbits_array.append(plainbits[:10])

	#plaintext = decode(plainbits_array)
	#print("Plaintext: " + str(plaintext) + "\n"
	if pipe_plaintext_out: print("\n### Recovered plaintext: \n" + ''.join(plaintext_array))

	#print(curiousciphers)
