#!/usr/bin/env python


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


if __name__ == "__main__":

    ## Protocol failure example
    # each message encrypted by RSA is a single alphabet letter, so the total
    # search space per ciphertext number is only 25, and the key never changes
    ciphertext = [365, 0, 4845, 14930, 2608, 2608, 0]
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

    print ''.join(plaintext)
