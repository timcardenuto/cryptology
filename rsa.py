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


def findModularInverse(a, m):
	# extended Eclidean algorithm
	gcd, x, y = gcdExtended(a, m)
	if gcd != 1:
		res = ''
	else:
		res = (x%m + m) % m
	return res


# Returns all pairs of factors that multiplied will equal n
# Stops at the square root of n, since all pairs found after that will just be mirror copies of the ones already found
def factor(n):
    p = []
    q = []
    for val in range(1,int(math.floor(math.sqrt(n)))):
        if n%val is 0:
            print str(val) + "," + str(n/val)
            p.append(val)
            q.append(n/val)
    return p,q


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


def commonModulusDecrypt(n, b1, b2, y1, y2):
    c1 = findModularInverse(b1,b2)
    c2 = (c1*b1 - 1)/b2
    temp1 = modularExponentiation(y1,c1,n)
    temp2 = findModularInverse(pow(y2,c2),n)
    x1 = (temp1 * temp2) % n
    return x1


if __name__ == "__main__":
    print "####     RSA Protocol Failure Example 1"
    ## Protocol failure example
    # each message encrypted by RSA is a single alphabet letter, so the total
    # search space per ciphertext number is only 25, and the key never changes
    ciphertext = [365, 0, 4845, 14930, 2608, 2608, 0]
    print "\nCiphertext: " + str(ciphertext)
    # m^b mod n
    n = 18721
    b = 25

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    cipherdecimals = []
    for letter in alphabet:
        # calculate ciphertext decimal value of each possible plaintext letter in the alphabet since it never changes
        # populate list in the order of the letters, so we can use a common index
        cipherdecimal = modularExponentiation(alphabet.find(letter),b,n)
        cipherdecimals.append(cipherdecimal)

    plaintext = []
    for c in ciphertext:
        # use the common index to find the plaintext letter for each ciphertext decimal value
        plaintext.append(alphabet[cipherdecimals.index(c)])

    print "Plaintext: " + ''.join(plaintext) + "\n"


    # Brute Force
    print "#### RSA Brute Force"
    ciphertext = [12423, 11524, 7243, 7459, 14303, 6127, 10964, 16399,
                    9792, 13629, 14407, 18817, 18830, 13556, 3159, 16647,
                    5300, 13951, 81, 8986, 8007, 13167, 10022, 17213]
    n = 18923
    b = 1261
    print "n = " + str(n)
    print "b = " + str(b)

    # factor the public key 'n'. This only works because it's so small,
    # real world examples should be impossible to factor in a brute force manner like this
    print "Factors:"
    p,q = factor(n)

    print "Ciphertext: " + str(ciphertext)

    # could ignore the first factor - why would anyone pick p=1 and q=n? This always results in an imposible 'a'
    # this decrypts the ciphertext for every pair of factors, so you'll end up with len(p) plaintext with only one likely to make any sense
    for idx in range(len(p)):
        possible_phi = (p[idx]-1)*(q[idx]-1)
        possible_a = findModularInverse(b,possible_phi)
        if not possible_a:
            print "Inverse doesn't exist for " + str(b) + "^-1 mod " + str(possible_phi)
            continue

        print "Private key: " + str(possible_a)

        plaintext = []
        for cipherdecimal in ciphertext:
            plaindecimal = modularExponentiation(cipherdecimal,possible_a,n)
            plaintext.extend(decode(plaindecimal))

        print "Plaintext: " + ''.join(plaintext) + "\n"


    print "#### RSA Protocol Failure Example 2"
    n = 18721
    b1 = 43
    b2 = 7717
    y1 = 12677
    y2 = 14702
    x1 = commonModulusDecrypt(n, b1, b2, y1, y2)
    print "Calculated x as " + str(x1)
    # check result by calculating encrypted output from recovered plaintext
    checky1 = modularExponentiation(x1, b1, n)
    checky2 = modularExponentiation(x1, b2, n)
    if (checky1 == y1) and (checky2 == y2):
        print "Success"
    else:
        print "Calculated x1 is not equal to x"
