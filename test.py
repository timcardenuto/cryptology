#!/usr/bin/env python

import re
import enchant
import sys
import operator


expected_freq = {'A':0.082, 'B':0.015, 'C':0.028, 'D':0.043, 'E':0.127, 'F':0.022, 'G':0.020, 'H':0.061, 'I':0.070, 'J':0.002,
		 'K':0.008, 'L':0.040, 'M':0.024, 'N':0.067, 'O':0.075, 'P':0.019, 'Q':0.001, 'R':0.060, 'S':0.063, 'T':0.091,
		  'U':0.028, 'V':0.010, 'W':0.023, 'X':0.001, 'Y':0.020, 'Z':0.001}


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
		print y
		# calculate the IOC of each y[i]
		ioc.append(0)
		for c in expected_freq:
			ioc[i] += y[i].count(c)/float(len(y[i])) * (y[i].count(c)-1)/(float(len(y[i]))-1)
			print ioc
	return ioc


''' This checks for keywords up to some max, could just look until IOC is near expected '''
def findKeywordLength(ciphertext, maximum=20):
	ioc = []
	ioc.append(0)
	ioc.append(0)
	ioc.append(0)
	for keylength in range(3,maximum):
		print keylength
		ioc.append(sum(getIndexOfCoincidence(keylength, ciphertext))/keylength)
	print ioc
	index, value = max(enumerate(ioc), key=operator.itemgetter(1))
	print "Largest average Index of Coincidence is " + str(value) + " for key length " + str(index)
	return index




# vigenere variant test
plaintext = 'HELLOWORLDWHATSUPQ'
keyword =   'SUMMERTVNNFSUWOOGT'
ciphertext ='ZYXXSNHMYQBZUPGIVJ'
findKeywordLength(ciphertext, maximum=7)





def slidingWindowSearch(string, wordlength):
	d = enchant.Dict("en_US")
	words = []
	for i in range(wordlength):
		for idx in range(0,len(string), wordlength):
			#print "index " + str(idx)
			#print string
			word = string[idx:idx+wordlength]
			if len(word)==wordlength and d.check(word):
				words.append(word)
				#print("English word found: "+word)
		string = string[1:]
	# when words are found, need to have a way to ignore them in future searchs of smaller lengths
	return words


def problem2 ():
	strings = ['thereisnotimelikethepresentthereisnotimelikethepresent']
	words = ['time', 'present']


	words = []
	for wordlength in range(7,2,-1):
		newwords = []
		for string in strings:
			if string not in words:  # if this string has not already been determined to *be* a word, then check it for new words
				newwords += slidingWindowSearch(string, wordlength)     # find the words of this length...

		# splits all words in 'newwords' out from all strings in 'strings', keeps the order of the remaining substrings
		# basically break out all 'newwords' we just found
		for word in newwords:
			newstrings = []
			for string in strings:
				if string not in words:
					newstrings += filter(None, re.split('('+word+')',string))  # snip a word out of the substring, replace substring with the return (could be multiple additional substrings)
				else: # just keep the string that's probably already a word, don't split it
					newstrings.append(string)
			strings = newstrings
			words.append(word)
	print strings
	strings_withspaces = ['{0} '.format(elem) for elem in strings]
	print ''.join(strings_withspaces)
