#!/usr/bin/env python

"""
    Assumptions:
        * ciphertext is only uppercase English letters that represent lowercase English letters - no spaces, no special characters, no numbers, etc.
"""

import sys
import operator
import scipy as sp
import matplotlib.pyplot as plt
import enchant


def convertLettersToDecimals(string):
    decimals = []
    for char in string:
        if char == 'A': decimals.append(0)
        if char == 'B': decimals.append(1)
        if char == 'C': decimals.append(2)
        if char == 'D': decimals.append(3)
        if char == 'E': decimals.append(4)
        if char == 'F': decimals.append(5)
        if char == 'G': decimals.append(6)
        if char == 'H': decimals.append(7)
        if char == 'I': decimals.append(8)
        if char == 'J': decimals.append(9)
        if char == 'K': decimals.append(10)
        if char == 'L': decimals.append(11)
        if char == 'M': decimals.append(12)
        if char == 'N': decimals.append(13)
        if char == 'O': decimals.append(14)
        if char == 'P': decimals.append(15)
        if char == 'Q': decimals.append(16)
        if char == 'R': decimals.append(17)
        if char == 'S': decimals.append(18)
        if char == 'T': decimals.append(19)
        if char == 'U': decimals.append(20)
        if char == 'V': decimals.append(21)
        if char == 'W': decimals.append(22)
        if char == 'X': decimals.append(23)
        if char == 'Y': decimals.append(24)
        if char == 'Z': decimals.append(25)
    return decimals


def decrypt(decimals_encrypted,key):
    decimals_decrypted = []
    decimals_decrypted.append((decimals_encrypted[0] - key) % 26)                      # first plaintext is based on initial key
    for idx in range(1,len(decimals_encrypted)):
        decimals_decrypted.append((decimals_encrypted[idx] - decimals_decrypted[idx-1]) % 26)   # new keys are last plaintext
    return decimals_decrypted


def convertDecimalsToLetters(decimals):
    string = []
    for decimal in decimals:
    	if decimal == 0: string.append('A')
    	if decimal == 1: string.append('B')
    	if decimal == 2: string.append('C')
    	if decimal == 3: string.append('D')
    	if decimal == 4: string.append('E')
    	if decimal == 5: string.append('F')
    	if decimal == 6: string.append('G')
    	if decimal == 7: string.append('H')
    	if decimal == 8: string.append('I')
    	if decimal == 9: string.append('J')
    	if decimal == 10: string.append('K')
    	if decimal == 11: string.append('L')
    	if decimal == 12: string.append('M')
    	if decimal == 13: string.append('N')
    	if decimal == 14: string.append('O')
    	if decimal == 15: string.append('P')
    	if decimal == 16: string.append('Q')
    	if decimal == 17: string.append('R')
    	if decimal == 18: string.append('S')
    	if decimal == 19: string.append('T')
    	if decimal == 20: string.append('U')
    	if decimal == 21: string.append('V')
    	if decimal == 22: string.append('W')
    	if decimal == 23: string.append('X')
    	if decimal == 24: string.append('Y')
    	if decimal == 25: string.append('Z')
    return ''.join(string)


''' No key argument, uses brute force search of entire key space'''
def decryptAutokeyBruteForce(ciphertext):
    decimals_encrypted = convertLettersToDecimals(ciphertext)
    most_words = 0
    for key in range(26):
        decimals_decrypted = decrypt(decimals_encrypted,key)
        plaintext = convertDecimalsToLetters(decimals_decrypted)
        #print 'For key '+str(key)+' #####################################'
        words = wordSearch(plaintext.lower())
        if len(words) > most_words:
            most_words = len(words)
            probable_key = key
            probable_plaintext = plaintext
    return probable_plaintext.lower()


def decryptAutokey(ciphertext, key):
    decimals = convertLettersToDecimals(ciphertext)
    decimals = decrypt(decimals,key)
    plaintext = convertDecimalsToLetters(decimals)
    return plaintext.lower()


def wordSearch(string):
    # reasonable to ignore word lengths > 7 or 8 or something
    # reasonable to ignore words of 1 or 2 letters, since they will appear randomly
    # start from larger word lengths and work down, since there's less likely to be false positives (smaller words inside bigger words)
    words = []
    for wordlength in range(7,2,-1):
            words += slidingWindowSearch(string, wordlength)     # find the words of this length...
    return words

    ''' This tries to break words out and add spaces.... It sorta works.
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
    '''



''' uses a sliding window to search for words of length 'wordlength' within 'string' '''
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


''' This is an example of how to use the functions.
    Will also allow you to send your own ciphertext file and key from commandline.
    If no key is given from commandline, this will call the brute force routine
'''
if __name__ == "__main__":
    if len(sys.argv) == 3:
        with open(sys.argv[1]) as fh:
    		text = fh.readlines()
    	text = [line.strip() for line in text]  # strips off \r\n characters
    	ciphertext = ''.join(text)  # combines separate lines into single string
        key = int(sys.argv[2])
        if key < 0 or key > 25:
            print "Invalid key"
            exit()
        print "Ciphertext:  " + ciphertext
        plaintext = decryptAutokey(ciphertext, key)
        print "Plaintext:   " + plaintext

    elif len(sys.argv) == 2:
        with open(sys.argv[1]) as fh:
            text = fh.readlines()
        text = [line.strip() for line in text]  # strips off \r\n characters
        ciphertext = ''.join(text)  # combines separate lines into single string
        print "Ciphertext:  " + ciphertext
        plaintext = decryptAutokeyBruteForce(ciphertext)
        print "Plaintext:   " + plaintext

    else:
        ciphertext = 'ZVRQHDUJIM'
        print "Ciphertext:  " + ciphertext
        plaintext = decryptAutokey(ciphertext, key=8)
        print "Plaintext:   " + plaintext
