#!/usr/bin/env python

#------------------------------------------------------------------------------
# MIT License
#
# Copyright (C) 2017  Tim Cardenuto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For questions contact the originator at timcardenuto@gmail.com
#------------------------------------------------------------------------------

import operator
import sys
import enchant
import re

# TODO blind digram/trigram search of encrypted characters
# TODO way to keep a 'hangman' screen viewable and constantly updated while I try things, also be nice if last highlight was shown on that

data = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0, 'J':0,
		 'K':0, 'L':0, 'M':0, 'N':0, 'O':0, 'P':0, 'Q':0, 'R':0, 'S':0, 'T':0,
		  'U':0, 'V':0, 'W':0, 'X':0, 'Y':0, 'Z':0}

substitute = {'A':'', 'B':'', 'C':'', 'D':'', 'E':'', 'F':'', 'G':'', 'H':'', 'I':'', 'J':'',
		 'K':'', 'L':'', 'M':'', 'N':'', 'O':'', 'P':'', 'Q':'', 'R':'', 'S':'', 'T':'',
		  'U':'', 'V':'', 'W':'', 'X':'', 'Y':'', 'Z':''}

options = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[],
		 'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[],
		  'U':[], 'V':[], 'W':[], 'X':[], 'Y':[], 'Z':[]}
map = {}

tier1 = ['e']
tier2 = ['t', 'a', 'o', 'i', 'n', 's', 'h', 'r']
tier3 = ['d', 'l']
tier4 = ['c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b']
tier5 = ['v', 'k', 'j', 'x', 'q', 'z']

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def getkey(substitute, value):
	return list(substitute.keys())[list(substitute.values()).index(value)]

def printMap(map):
	for m in map:
		print m + '  expects ' + str(map[m]['expect']) + '  using ' + str(map[m]['using']) + '  with ' + str(map[m]['with']) + (' [locked] ' if map[m]['lock'] else '')

def printUnused(map):
	for m in map:
		if not map[m]['lock']:
			print m + '  expects ' + str(map[m]['expect']) + '  using ' + str(map[m]['using']) + '  with ' + str(map[m]['with'])

def guess(map, cipherletter, plainletter):
	print "guessing: '" + cipherletter + "' is: '" + plainletter
	displaceletter = map[plainletter]['using']
	for key, value in map.iteritems():
		if value['using'] == cipherletter:
			movetoletter = key
	print "displaces: " + displaceletter + "  to: " + movetoletter
	map[movetoletter]['using'] = displaceletter
	map[movetoletter]['with'] = data[displaceletter]
	map[plainletter]['using'] = cipherletter
	map[plainletter]['with'] = data[cipherletter]
	map[plainletter]['lock'] = True


def lock(map, char):
	map[char]['lock'] = True

def unlock(map, char):
	map[char]['lock'] = False

def printlocked(map, plaintext):
	addspace = True
	for c in plaintext:
		if map[c]['lock'] and addspace:
			sys.stdout.write(' ')
			sys.stdout.write(c)
			addspace = False
		elif not map[c]['lock'] and not addspace:
			sys.stdout.write(' ')
			sys.stdout.write(c)
			addspace = True
		else:
			sys.stdout.write(c)


''' I know it's not pretty, but it seems to work
'''
def highlight(lookfor, ciphertext):
	lct = list(ciphertext)
	llf = list(lookfor)
	c1 = []
	for idx, val in enumerate(llf):     # initial fill the length of the string we're looking for -1
		if idx == len(llf):
			continue
		else:
			c1.append(lct[idx])
	spin = 0
	for c2 in lct[len(llf):]:
		if (''.join(c1)) == lookfor:
			sys.stdout.write(bcolors.OKGREEN + str(''.join(c1)))
			spin = len(c1)-1
			sys.stdout.flush()
		elif spin > 0:
			spin -= 1
		else:
			sys.stdout.write(bcolors.OKBLUE + c1[0])

		for idx, val in enumerate(c1):
			if idx == len(c1)-1:
				c1[len(c1)-1] = c2
			else:
				c1[idx] = c1[idx+1]
	if (''.join(c1)) == lookfor:
		sys.stdout.write(bcolors.OKGREEN + str(''.join(c1)))
		spin = len(c1)-1
		sys.stdout.flush()
	else:
		for c in c1:
			if spin > 0:
				spin -= 1
			else:
				sys.stdout.write(bcolors.OKBLUE + c)

def printHighlight(map,ciphertext):
	# rebuild substitute based on new map
	global substitute
	for key, value in map.iteritems():
		substitute[value['using']] = key
	# decipher
	plaintext = decipher(substitute, ciphertext)
	# print
	start = 0
	pcount = 0
	for c in plaintext:
		if map[c]['lock']:
			sys.stdout.write(c)
		else:
			sys.stdout.write('-')
		pcount += 1
		if pcount%83 == 0:						# switch to printing a line of ciphertext
			sys.stdout.write('\n')
			for c2 in ciphertext[start:pcount]:
				sys.stdout.write(c2)
			sys.stdout.write('\n')
			start = pcount
	# get the remainder
	sys.stdout.write('\n')
	for c2 in ciphertext[start:pcount]:
		sys.stdout.write(c2)
	sys.stdout.write('\n')
	start = pcount


# if I find many occurrences of these then their letters are likely correct
digram = [{'th':0},{'he':0},{'in':0},{'er':0},{'an':0},{'re':0},{'ed':0},{'on':0},{'es':0},
			 {'st':0},{'en':0},{'at':0},{'to':0},{'nt':0},{'ha':0},{'nd':0},{'ou':0},{'ea':0},
			  {'ng':0},{'as':0},{'or':0},{'ti':0},{'is':0},{'et':0},{'it':0},{'ar':0},{'te':0},
			   {'se':0},{'hi':0},{'of':0}]
def digramSearch(plaintext):
	digram[0]['th']=plaintext.count('th')
	digram[1]['he']=plaintext.count('he')
	digram[2]['in']=plaintext.count('in')
	digram[3]['er']=plaintext.count('er')
	digram[4]['an']=plaintext.count('an')
	digram[5]['re']=plaintext.count('re')
	digram[6]['ed']=plaintext.count('ed')
	digram[7]['on']=plaintext.count('on')
	digram[8]['es']=plaintext.count('es')
	digram[9]['st']=plaintext.count('st')
	digram[10]['en']=plaintext.count('en')
	digram[11]['at']=plaintext.count('at')
	digram[12]['to']=plaintext.count('to')
	digram[13]['nt']=plaintext.count('nt')
	digram[14]['ha']=plaintext.count('ha')
	digram[15]['nd']=plaintext.count('nd')
	digram[16]['ou']=plaintext.count('ou')
	digram[17]['ea']=plaintext.count('ea')
	digram[18]['ng']=plaintext.count('ng')
	digram[19]['as']=plaintext.count('as')
	digram[20]['or']=plaintext.count('or')
	digram[21]['ti']=plaintext.count('ti')
	digram[22]['is']=plaintext.count('is')
	digram[23]['et']=plaintext.count('et')
	digram[24]['it']=plaintext.count('it')
	digram[25]['ar']=plaintext.count('ar')
	digram[26]['te']=plaintext.count('te')
	digram[27]['se']=plaintext.count('se')
	digram[28]['hi']=plaintext.count('hi')
	digram[29]['of']=plaintext.count('of')
	return digram

def printDigram(plaintext):
	keys = []
	for i in digram:
		keys.append(i.keys()[0])
	lpt = list(plaintext)
	c1 = lpt[0]
	for c2 in lpt[1:]:
		if (c1+c2) in keys:
			#sys.stdout.write(' ')
			sys.stdout.write(bcolors.OKGREEN + str(c1+c2))
			#sys.stdout.write(' ')
			sys.stdout.flush()
		else:
			sys.stdout.write(bcolors.OKBLUE + c1)
		c1 = c2
	sys.stdout.write(c1)

# to keep these ordered, I'd need to [{},{}] each one
trigram = [{'the':0},{'ing':0},{'and':0},{'her':0},{'ere':0},{'ent':0},
			 {'tha':0},{'nth':0},{'was':0},{'eth':0},{'for':0},{'dth':0}]
def trigramSearch(plaintext):
	trigram[0]['the']=plaintext.count('the')
	trigram[1]['ing']=plaintext.count('ing')
	trigram[2]['and']=plaintext.count('and')
	trigram[3]['her']=plaintext.count('her')
	trigram[4]['ere']=plaintext.count('ere')
	trigram[5]['ent']=plaintext.count('ent')
	trigram[6]['tha']=plaintext.count('tha')
	trigram[7]['nth']=plaintext.count('nth')
	trigram[8]['was']=plaintext.count('was')
	trigram[9]['eth']=plaintext.count('eth')
	trigram[10]['for']=plaintext.count('for')
	trigram[11]['dth']=plaintext.count('dth')
	return trigram

def printTrigram(plaintext):
	keys = []
	for i in trigram:
		keys.append(i.keys()[0])
	lpt = list(plaintext)
	c1 = lpt[0]
	c2 = lpt[1]
	for c3 in lpt[2:]:
		if (c1+c2+c3) in keys:
			sys.stdout.write(' ')
			sys.stdout.write(bcolors.OKGREEN + str(c1+c2+c3))
			sys.stdout.write(' ')
			sys.stdout.flush()
		else:
			sys.stdout.write(bcolors.OKBLUE + c1)
		c1 = c2
		c2 = c3
	sys.stdout.write(c1+c2)

def t2search(substitute, jump):
	scrambleTier2(substitute,jump)
	plaintext = decipher(substitute,ciphertext)
	printTrigram(plaintext)

def t3search(substitute, jump):
	scrambleTier3(substitute,jump)
	plaintext = decipher(substitute,ciphertext)
	printTrigram(plaintext)

def t4search(substitute, jump):
	scrambleTier4(substitute,jump)
	plaintext = decipher(substitute,ciphertext)
	printTrigram(plaintext)

def printHangman(map,ciphertext):
	# rebuild substitute based on new map
	global substitute
	for key, value in map.iteritems():
		substitute[value['using']] = key
	# decipher
	plaintext = decipher(substitute, ciphertext)
	# print
	start = 0
	pcount = 0
	for c in plaintext:
		if map[c]['lock']:
			sys.stdout.write(c)
		else:
			sys.stdout.write('-')
		pcount += 1
		if pcount%83 == 0:
			sys.stdout.write('\n')
			for c2 in ciphertext[start:pcount]:
				sys.stdout.write(c2)
			sys.stdout.write('\n')
			start = pcount
	# get the remainder
	sys.stdout.write('\n')
	for c2 in ciphertext[start:pcount]:
		sys.stdout.write(c2)
	sys.stdout.write('\n')
	start = pcount

# swap a single pair of letters
def swap(substitute, char1, char2):
	substitute[getkey(substitute,char1)] = char2
	substitute[getkey(substitute,char2)] = char1

# scramble letters that I'm still not confident are correct
def scrambleTier2(substitute, i=0):
	keyt = getkey(substitute,'t')
	keya = getkey(substitute,'a')
	keyo = getkey(substitute,'o')
	keyi = getkey(substitute,'i')
	keyn = getkey(substitute,'n')
	keys = getkey(substitute,'s')
	keyh = getkey(substitute,'h')
	keyr = getkey(substitute,'r')
	substitute[keyt] = tier2[(0+(i%8))%8]
	substitute[keya] = tier2[(1+(i%8))%8]
	substitute[keyo] = tier2[(2+(i%8))%8]
	substitute[keyi] = tier2[(3+(i%8))%8]
	substitute[keyn] = tier2[(4+(i%8))%8]
	substitute[keys] = tier2[(5+(i%8))%8]
	substitute[keyh] = tier2[(6+(i%8))%8]
	substitute[keyr] = tier2[(7+(i%8))%8]

def scrambleTier3(substitute, i=0):
	keyd = getkey(substitute,'d')
	keyl = getkey(substitute,'l')
	substitute[keyd] = tier3[(0+(i%2))%2]
	substitute[keyl] = tier3[(1+(i%2))%2]

def scrambleTier4(substitute, i=0):
	ckey = getkey(substitute,'c')
	ukey = getkey(substitute,'u')
	mkey = getkey(substitute,'m')
	wkey = getkey(substitute,'w')
	fkey = getkey(substitute,'f')
	gkey = getkey(substitute,'g')
	ykey = getkey(substitute,'y')
	pkey = getkey(substitute,'p')
	bkey = getkey(substitute,'b')
	substitute[ckey] = tier4[(0+(i%9))%9]
	substitute[ukey] = tier4[(1+(i%9))%9]
	substitute[mkey] = tier4[(2+(i%9))%9]
	substitute[wkey] = tier4[(3+(i%9))%9]
	substitute[fkey] = tier4[(4+(i%9))%9]
	substitute[gkey] = tier4[(5+(i%9))%9]
	substitute[ykey] = tier4[(6+(i%9))%9]
	substitute[pkey] = tier4[(7+(i%9))%9]
	substitute[bkey] = tier4[(8+(i%9))%9]


def decipher(substitute, ciphertext):
	plaintext = list(ciphertext)
	for idx, val in enumerate(plaintext):
		plaintext[idx] = substitute[val]
	plaintext = ''.join(plaintext)
	return plaintext

def seperate(decrypted_str):
	d = enchant.Dict("en_US")
	wordlength = 6
	leftover = []
	breakout = ['']
	#while wordlength > 0:
	lct = list(decrypted_str)
	c1 = []
	for idx in range(wordlength):     # initial fill the length of the string we're looking for -1
		if idx == wordlength:
			continue
		else:
			c1.append(lct[idx])
	spin = 0
	for c2 in lct[wordlength:]:
		#print ''.join(c1)
		if (d.check(''.join(c1))):
			breakout.append(str(''.join(c1)))
			breakout.append('')
			spin = len(c1)-1
		elif spin > 0:
			spin -= 1
		else:
			breakout[len(breakout)-1] = breakout[len(breakout)-1] + c1[0]
		for idx, val in enumerate(c1):
			if idx == len(c1)-1:
				c1[len(c1)-1] = c2
			else:
				c1[idx] = c1[idx+1]
	if (d.check(''.join(c1))):
		breakout.append(str(''.join(c1)))
		breakout.append('')
		spin = len(c1)-1
	else:
		for c in c1:
			if spin > 0:
				spin -= 1
			else:
				breakout[len(breakout)-1] = breakout[len(breakout)-1] + c1[0]
	print breakout
	return breakout

	# there are no delimiters...
	'''
	alphabetSize = 26
	for key in range(alphabetSize):
		# If you get some possible words check against dictionary / english grammer ...
		d = enchant.Dict("en_US")
		#decrypted_split = decrypted_str.split(' ')
		temp_split = re.split('[!;@#$%^&*()?., ]',decrypted_str)
		decrypted_split = list(filter(None, temp_split))
		check = False
		for word in decrypted_split:
			print(word, " = ", d.check(word))
			if (len(word) > 1 and d.check(word)):
				check = True
				print("English word found: ", word)

		if (check):
			print("Possible decrypted msg:  ", ''.join(decrypted_char))
			print("Initial register fill: ",fill)
			print("Alphabet shift key: ", key)
			print('')
	'''


def runFA(ciphertext):
	print "\n#### Running frequency analysis on ciphertext ##################"

	global data
	# find numbers of character occurrences
	for c in ciphertext:
		if c=='A': data['A'] += 1.0/float(len(ciphertext))  # could also do without loop: data['A']=ciphertext.count('A')/float(len(ciphertext))
		if c=='B': data['B'] += 1.0/float(len(ciphertext))
		if c=='C': data['C'] += 1.0/float(len(ciphertext))
		if c=='D': data['D'] += 1.0/float(len(ciphertext))
		if c=='E': data['E'] += 1.0/float(len(ciphertext))
		if c=='F': data['F'] += 1.0/float(len(ciphertext))
		if c=='G': data['G'] += 1.0/float(len(ciphertext))
		if c=='H': data['H'] += 1.0/float(len(ciphertext))
		if c=='I': data['I'] += 1.0/float(len(ciphertext))
		if c=='J': data['J'] += 1.0/float(len(ciphertext))
		if c=='K': data['K'] += 1.0/float(len(ciphertext))
		if c=='L': data['L'] += 1.0/float(len(ciphertext))
		if c=='M': data['M'] += 1.0/float(len(ciphertext))
		if c=='N': data['N'] += 1.0/float(len(ciphertext))
		if c=='O': data['O'] += 1.0/float(len(ciphertext))
		if c=='P': data['P'] += 1.0/float(len(ciphertext))
		if c=='Q': data['Q'] += 1.0/float(len(ciphertext))
		if c=='R': data['R'] += 1.0/float(len(ciphertext))
		if c=='S': data['S'] += 1.0/float(len(ciphertext))
		if c=='T': data['T'] += 1.0/float(len(ciphertext))
		if c=='U': data['U'] += 1.0/float(len(ciphertext))
		if c=='V': data['V'] += 1.0/float(len(ciphertext))
		if c=='W': data['W'] += 1.0/float(len(ciphertext))
		if c=='X': data['X'] += 1.0/float(len(ciphertext))
		if c=='Y': data['Y'] += 1.0/float(len(ciphertext))
		if c=='Z': data['Z'] += 1.0/float(len(ciphertext))


	# in the order of likelyhood
	letters = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']
	letters.reverse()

	global substitute
	global options

	sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
	tier = 1
	count = 0
	for sd in sorted_data:
		substitute[sd[0]] = letters.pop()
		if tier == 1:
			options[sd[0]] = ['e']
			tier = 2
		elif tier == 2:
			options[sd[0]] = ['t', 'a', 'o', 'i', 'n', 's', 'h', 'r']
			count += 1
			if count == 8:
				tier = 3
				count = 0
		elif tier == 3:
			options[sd[0]] = ['d', 'l']
			count += 1
			if count == 2:
				tier = 4
				count = 0
		elif tier == 4:
			options[sd[0]] = ['c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b']
			count += 1
			if count == 9:
				tier = 5
				count = 0
		elif tier == 5:
			options[sd[0]] = ['v', 'k', 'j', 'x', 'q', 'z']
			count += 1
			if count == 6:
				tier = 6
				count = 0

	global map
	map = {'e':{'expect':0.127, 'using':getkey(substitute,'e'), 'with':data[getkey(substitute,'e')], 'lock':False, 'guess':[]},
			't':{'expect':0.091, 'using':getkey(substitute,'t'), 'with':data[getkey(substitute,'t')], 'lock':False, 'guess':[]},
			'a':{'expect':0.082, 'using':getkey(substitute,'a'), 'with':data[getkey(substitute,'a')], 'lock':False, 'guess':[]},
			'o':{'expect':0.075, 'using':getkey(substitute,'o'), 'with':data[getkey(substitute,'o')], 'lock':False, 'guess':[]},
			'i':{'expect':0.070, 'using':getkey(substitute,'i'), 'with':data[getkey(substitute,'i')], 'lock':False, 'guess':[]},
			'n':{'expect':0.067, 'using':getkey(substitute,'n'), 'with':data[getkey(substitute,'n')], 'lock':False, 'guess':[]},
			's':{'expect':0.063, 'using':getkey(substitute,'s'), 'with':data[getkey(substitute,'s')], 'lock':False, 'guess':[]},
			'h':{'expect':0.061, 'using':getkey(substitute,'h'), 'with':data[getkey(substitute,'h')], 'lock':False, 'guess':[]},
			'r':{'expect':0.060, 'using':getkey(substitute,'r'), 'with':data[getkey(substitute,'r')], 'lock':False, 'guess':[]},
			'd':{'expect':0.043, 'using':getkey(substitute,'d'), 'with':data[getkey(substitute,'d')], 'lock':False, 'guess':[]},
			'l':{'expect':0.040, 'using':getkey(substitute,'l'), 'with':data[getkey(substitute,'l')], 'lock':False, 'guess':[]},
			'c':{'expect':0.028, 'using':getkey(substitute,'c'), 'with':data[getkey(substitute,'c')], 'lock':False, 'guess':[]},
			'u':{'expect':0.028, 'using':getkey(substitute,'u'), 'with':data[getkey(substitute,'u')], 'lock':False, 'guess':[]},
			'm':{'expect':0.024, 'using':getkey(substitute,'m'), 'with':data[getkey(substitute,'m')], 'lock':False, 'guess':[]},
			'w':{'expect':0.023, 'using':getkey(substitute,'w'), 'with':data[getkey(substitute,'w')], 'lock':False, 'guess':[]},
			'f':{'expect':0.022, 'using':getkey(substitute,'f'), 'with':data[getkey(substitute,'f')], 'lock':False, 'guess':[]},
			'g':{'expect':0.020, 'using':getkey(substitute,'g'), 'with':data[getkey(substitute,'g')], 'lock':False, 'guess':[]},
			'y':{'expect':0.020, 'using':getkey(substitute,'y'), 'with':data[getkey(substitute,'y')], 'lock':False, 'guess':[]},
			'p':{'expect':0.019, 'using':getkey(substitute,'p'), 'with':data[getkey(substitute,'p')], 'lock':False, 'guess':[]},
			'b':{'expect':0.015, 'using':getkey(substitute,'b'), 'with':data[getkey(substitute,'b')], 'lock':False, 'guess':[]},
			'v':{'expect':0.010, 'using':getkey(substitute,'v'), 'with':data[getkey(substitute,'v')], 'lock':False, 'guess':[]},
			'k':{'expect':0.008, 'using':getkey(substitute,'k'), 'with':data[getkey(substitute,'k')], 'lock':False, 'guess':[]},
			'j':{'expect':0.002, 'using':getkey(substitute,'j'), 'with':data[getkey(substitute,'j')], 'lock':False, 'guess':[]},
			'x':{'expect':0.001, 'using':getkey(substitute,'x'), 'with':data[getkey(substitute,'x')], 'lock':False, 'guess':[]},
			'q':{'expect':0.001, 'using':getkey(substitute,'q'), 'with':data[getkey(substitute,'q')], 'lock':False, 'guess':[]},
			'z':{'expect':0.001, 'using':getkey(substitute,'z'), 'with':data[getkey(substitute,'z')], 'lock':False, 'guess':[]}}

	printMap(map)
	print "#### Completed #################################################\n"
	return map

if __name__ == "__main__":
	if len(sys.argv) == 2:
			with open(sys.argv[1]) as fh:
				text = fh.readlines()
			text = [line.strip() for line in text]  # strips off \r\n characters
			ciphertext = ''.join(text)  # combines separate lines into single string
	else:
		ciphertext = 'KXZBGSLHCNNZLFZSQBKCMKSYAFGPKXZZCFKXCMLKXZFZKEFEMDAGDFZWZCSZLCMCFPYNKFZKBXZLGQKGMKXZXESSNFZNKEMDCNKXZSCMLNBCHZBXCMDZLAFGPJFGRMKGDFZZMKXZCFPYCRCOZMZLCMLJZDCMKGKFZPJSZREKXZCDZFMZNNCKKXZMGENZGAFQPGFN'
	map = runFA(ciphertext)
