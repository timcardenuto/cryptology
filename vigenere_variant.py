#!/usr/bin/env python

""" This is almost identical to the regular vigenere cipher,
	except the keyword changes on each reuse by shifting each keyword character
	to the subsequent letter. So if the keyword was 'SUMMER' the second use would
	be 'TVNNFS'.

	Because the keyword 'length' is not changing, we can still calculate the IOC
	for the length the same way.
"""

import sys
import operator
import scipy as sp
import matplotlib.pyplot as plt

ciphertext=''

expected_freq = {'A':0.082, 'B':0.015, 'C':0.028, 'D':0.043, 'E':0.127, 'F':0.022, 'G':0.020, 'H':0.061, 'I':0.070, 'J':0.002,
		 'K':0.008, 'L':0.040, 'M':0.024, 'N':0.067, 'O':0.075, 'P':0.019, 'Q':0.001, 'R':0.060, 'S':0.063, 'T':0.091,
		  'U':0.028, 'V':0.010, 'W':0.023, 'X':0.001, 'Y':0.020, 'Z':0.001}

expected = sp.array([0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070, 0.002,
		 0.008, 0.040, 0.024, 0.067, 0.075, 0.019, 0.001, 0.060, 0.063, 0.091,
		  0.028, 0.010, 0.023, 0.001, 0.020, 0.001])

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def variantShift(string):
	print string
	shiftstring = []
	for idx,val in enumerate(string):
		for i in range(idx % 27):	# applies increasing shift on a repeating 26 letter cycle
			#val = shiftLettersLeft(val)
			val = shiftLettersRight(val)
		shiftstring.append(val)
	print ''.join(shiftstring)
	return ''.join(shiftstring)


# looking for numbers close to 0.065
''' This part will be different from the regular vigenere,
	the shift will increase by 1 for each letter up to 26 letters and then reset
	for each letter
'''
def getShiftWithIOCClosestToExpected(string):
	plt.ion()
	plt.show()

	last = 0
	shift = 0
	shiftstring = string

	# additional shift applied here. Every character on 26 character cycle has +1 shift
	shiftstring = variantShift(shiftstring)

	plaintext_substring = ''
	for i in range(26):
		if i is not 0:
			shiftstring = shiftLettersLeft(shiftstring)
			#shiftstring = shiftLettersRight(shiftstring)

		# calculate ioc
		ioc = 0
		x2 = 0
		for c in expected_freq:
			ioc += expected_freq[c] * (shiftstring.count(c)/float(len(shiftstring)))
			x2 += pow(((shiftstring.count(c)/float(len(shiftstring))) - expected_freq[c]),2)/expected_freq[c]

		'''
		# print comparison chart
		#print 'shift ' + str(i)
		#print 'x2 ' + str(x2)
		frequencies = frequencyAnalysis(shiftstring)
		plt.clf()
		plt.plot(range(1,27),expected,'or')
		plt.plot(range(1,27),expected,'r')
		plt.plot(range(1,27),frequencies,'ok')
		plt.plot(range(1,27),frequencies,'k')
		plt.draw()
		plt.pause(0.001)
		#raw_input("paused...")
		'''

		if ioc > last:
			last = ioc
			shift = i
			plaintext_substring = shiftstring
	print "Highest IOC for substring is " + str(last) + " with shift of " + str(shift)
	return plaintext_substring,shift


def shiftLettersLeft(string):
	shiftstring = []
	for char in string:		# substitute for shifted letters
		if char == 'A': shiftstring.append('Z')
		if char == 'B': shiftstring.append('A')
		if char == 'C': shiftstring.append('B')
		if char == 'D': shiftstring.append('C')
		if char == 'E': shiftstring.append('D')
		if char == 'F': shiftstring.append('E')
		if char == 'G': shiftstring.append('F')
		if char == 'H': shiftstring.append('G')
		if char == 'I': shiftstring.append('H')
		if char == 'J': shiftstring.append('I')
		if char == 'K': shiftstring.append('J')
		if char == 'L': shiftstring.append('K')
		if char == 'M': shiftstring.append('L')
		if char == 'N': shiftstring.append('M')
		if char == 'O': shiftstring.append('N')
		if char == 'P': shiftstring.append('O')
		if char == 'Q': shiftstring.append('P')
		if char == 'R': shiftstring.append('Q')
		if char == 'S': shiftstring.append('R')
		if char == 'T': shiftstring.append('S')
		if char == 'U': shiftstring.append('T')
		if char == 'V': shiftstring.append('U')
		if char == 'W': shiftstring.append('V')
		if char == 'X': shiftstring.append('W')
		if char == 'Y': shiftstring.append('X')
		if char == 'Z': shiftstring.append('Y')
	return ''.join(shiftstring)


def shiftLettersRight(string):
	shiftstring = []
	for char in string:		# substitute for shifted letters
		if char == 'A': shiftstring.append('B')
		if char == 'B': shiftstring.append('C')
		if char == 'C': shiftstring.append('D')
		if char == 'D': shiftstring.append('E')
		if char == 'E': shiftstring.append('F')
		if char == 'F': shiftstring.append('G')
		if char == 'G': shiftstring.append('H')
		if char == 'H': shiftstring.append('I')
		if char == 'I': shiftstring.append('J')
		if char == 'J': shiftstring.append('K')
		if char == 'K': shiftstring.append('L')
		if char == 'L': shiftstring.append('M')
		if char == 'M': shiftstring.append('N')
		if char == 'N': shiftstring.append('O')
		if char == 'O': shiftstring.append('P')
		if char == 'P': shiftstring.append('Q')
		if char == 'Q': shiftstring.append('R')
		if char == 'R': shiftstring.append('S')
		if char == 'S': shiftstring.append('T')
		if char == 'T': shiftstring.append('U')
		if char == 'U': shiftstring.append('V')
		if char == 'V': shiftstring.append('W')
		if char == 'W': shiftstring.append('X')
		if char == 'X': shiftstring.append('Y')
		if char == 'Y': shiftstring.append('Z')
		if char == 'Z': shiftstring.append('A')
	return ''.join(shiftstring)


def frequencyAnalysis(ciphertext):
	data = sp.zeros(26, dtype = sp.double)
	# find numbers of character occurrences
	for c in ciphertext:
		if c=='A': data[0] += 1.0/float(len(ciphertext))  # could also do without loop: data['A']=ciphertext.count('A')/float(len(ciphertext))
		if c=='B': data[1] += 1.0/float(len(ciphertext))
		if c=='C': data[2] += 1.0/float(len(ciphertext))
		if c=='D': data[3] += 1.0/float(len(ciphertext))
		if c=='E': data[4] += 1.0/float(len(ciphertext))
		if c=='F': data[5] += 1.0/float(len(ciphertext))
		if c=='G': data[6] += 1.0/float(len(ciphertext))
		if c=='H': data[7] += 1.0/float(len(ciphertext))
		if c=='I': data[8] += 1.0/float(len(ciphertext))
		if c=='J': data[9] += 1.0/float(len(ciphertext))
		if c=='K': data[10] += 1.0/float(len(ciphertext))
		if c=='L': data[11] += 1.0/float(len(ciphertext))
		if c=='M': data[12] += 1.0/float(len(ciphertext))
		if c=='N': data[13] += 1.0/float(len(ciphertext))
		if c=='O': data[14] += 1.0/float(len(ciphertext))
		if c=='P': data[15] += 1.0/float(len(ciphertext))
		if c=='Q': data[16] += 1.0/float(len(ciphertext))
		if c=='R': data[17] += 1.0/float(len(ciphertext))
		if c=='S': data[18] += 1.0/float(len(ciphertext))
		if c=='T': data[19] += 1.0/float(len(ciphertext))
		if c=='U': data[20] += 1.0/float(len(ciphertext))
		if c=='V': data[21] += 1.0/float(len(ciphertext))
		if c=='W': data[22] += 1.0/float(len(ciphertext))
		if c=='X': data[23] += 1.0/float(len(ciphertext))
		if c=='Y': data[24] += 1.0/float(len(ciphertext))
		if c=='Z': data[25] += 1.0/float(len(ciphertext))
	return data


def getKeywordSubstrings(keywordlength, ciphertext):
	substrings = []
	for i in range(keywordlength):
		temp = []
		pick = i
		for idx,val in enumerate(ciphertext):
			if idx == pick:
				pick += keywordlength
				temp.append(val)
		substrings.append(''.join(temp))
	return substrings


''' Same as getKeywordSubstrings() but also calculates IOC for each substring '''
def getIndexOfCoincidence(keywordlength, ciphertext):
	y = []
	ioc = []
	for i in range(keywordlength):
		temp = []
		pick = i
		# pull out substrings y[i] for each keyword character
		for idx,val in enumerate(ciphertext):
			if idx == pick:
				pick += keywordlength
				temp.append(val)
		y.append(''.join(temp))

		# calculate the IOC of each y[i]
		ioc.append(0)
		for c in expected_freq:
			ioc[i] += y[i].count(c)/float(len(y[i])) * (y[i].count(c)-1)/(float(len(y[i]))-1)
	return ioc


''' This checks for keywords up to some max, could just look until IOC is near expected '''
def findKeywordLength(ciphertext, maximum=20):
	ioc = []
	ioc.append(0)
	ioc.append(0)
	ioc.append(0)
	for keylength in range(3,maximum):
		ioc.append(sum(getIndexOfCoincidence(keylength, ciphertext))/keylength)
	print ioc
	index, value = max(enumerate(ioc), key=operator.itemgetter(1))
	print "Largest average Index of Coincidence is " + str(value) + " for key length " + str(index)
	return index


# len(substrings) = keylength
def deinterleave(ciphertext,substrings):
	plaintext = []
	substrings_list = []
	for s in substrings:					# convert the substrings to lists
		substrings_list.append(list(s))
	for idx,val in enumerate(ciphertext):	# pop off char's in round robin fashion to rebuild plaintext
		plaintext.append(substrings_list[idx%len(substrings)].pop(0))
	return ''.join(plaintext)


def keyDecode(string, key):
	base = 0
	shiftedstring = []
	print key
	print string
	for i in range(0,len(string),len(key)):
		# convert key char to shift number?
		shifts = key
		for idx,val in enumerate(shifts):
			for i in range(val):
				shiftedchar = shiftLettersLeft(string[base+idx])
			shiftedstring.append(shiftedchar)
		base += len(key)
		print i
	return ''.join(shiftedstring)


def decryptVigenere(ciphertext):
	keylength = findKeywordLength(ciphertext)
	substrings = getKeywordSubstrings(keylength, ciphertext)

	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	shifts = range(keylength)
	plaintext_substrings = range(keylength)
	keyword = []
	for idx,val in enumerate(substrings):
		plaintext_substrings[idx], shifts[idx] = getShiftWithIOCClosestToExpected(val)
		keyword.append(alphabet[shifts[idx]])

	print "Keyword recovered: " + str(''.join(keyword))
	plaintext = deinterleave(ciphertext,plaintext_substrings)	# this is quicker since I already found plaintext substrings
	#plaintext = keyDecode(ciphertext,key)
	return plaintext.lower()


if __name__ == "__main__":
	if len(sys.argv) == 2:
		with open(sys.argv[1]) as fh:
			text = fh.readlines()
		text = [line.strip() for line in text]  # strips off \r\n characters
		ciphertext = ''.join(text)  # combines separate lines into single string
	else:
		ciphertext = 'JKBNJGFNFUZZWKBCGSFCQLHPWUXMICRYQNOOPYXGIMBIFLCRYJTISZSTWWDFZMEKWMFHQEQLXCSILDVNUPLQJNOWYGHBCHEBLAKEVGWHXZAPFIXLJAYUUMRZIMABLLPKIOXBQXUAEIMRRXGZKGDRXYWHXKIXOLPAEBKBHFFCWYPPREBEUQNEJBVRYWVBFNPWOSKKZSUTMHRNVURPDTPFNNVLCQXNEQFBMYQOXHNIOORBELSFUKSUJFILOTZUZLJJOOLXSLSCXWGWOELFOMSJJHABPZEJPZEMFQYKENYSMBHCDXPDDNEUASJLIIIELQGUSTKEDMIUXLFZMLHHTGKXCGAFWKQOVBXY'
	plaintext = decryptVigenere(ciphertext)
	print "Plaintext decrypted: "
	print plaintext
