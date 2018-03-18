#!/usr/bin/env python

# Feistel Cipher
# maps a 2 l-bit plaintext (Lo, Ro) to a 2 l-bit ciphertext (Rr, Lr), through an r-round procedure
# 'l' is bit length, so 2 l means the input plaintext and output ciphertext both have a Left and Right section of the same bit length
# K[i] is the 'round key' derived from the cipherkey K via a 'key schedule'

# Encrypt
# Plaintext is Lo+Ro
# For l <= i <= r,
#	L[i] = R[i-1]
#	R[i] = L[i-1] xor f(R[i-1], K[i])
# Swap LiRi at the end to be RiLi as ciphertext

# Decrypt
# Ciphertext is RiLi from last stage but just treat as LiRi and the same system will decrypt. The only difference is that you input the keys (K) in reverse
# For l <= i <= r,
#	L[i] = R[i-1]
#	R[i] = L[i-1] xor f(R[i-1], K[i])
# Swap LiRi at the end to be RiLi as plaintext

'''
# DES
# 64 bit plaintext string 'x' and 56 bit key 'K'
# difference in size is due to parity bit for each byte of plaintext
# based on Feistel except:
#	Encrypt plaintext 'x'
#	LoRo = IP(x), where IP is Initial Permutation
#	For i = 1 thru 16
#		generate K[i] from K
#		L[i] = R[i-1]
#		R[i] = L[i-1] xor f(R[i-1], K[i])
#
#	Decrypt ciphertext 'y'
#	y = IP^-1(R[16]L[16])

# DES 'f' function
#
# R[i-1]     K[i]
#    | 32      | 48
#    E         |
#    | 48      |
#    xor -------
#    |
#    8 S boxes of 6 bits
#    |
#    4 bits out of each box
#    |
#    bit permutation of 8x4 bits into 32 bit output


# in function form:  f(R[i-1],K[i]) = P(S(E(R[i-1])xor(K[i])))

# E is expansion function:  1 2 3 4       5 6 7 8    ...     29 30 31 32
#                                                     |
#						 32 1 2 3 4 5   4 5 6 7 8 9  ...  28 29 30 31 32 1

# S is S-box function
# each S-box is a 4x16 table, each entry is a 4 bit number
# 6 input bits, bit 1 and 6 specify row, bits 2-5 specify column
'''

#M = '1011010001110101001001011101010101111011010100110111110010010111'
#C = '1001010100101001101001101001100010011101001101001111111010100100'

def decimalTo4Bits(decimal):
    binary = []
    for i in reversed(range(4)):
        if decimal >= pow(2,i):
            binary.append(1)
            decimal = decimal - pow(2,i)
        else:
            binary.append(0)
    return binary


# This reads the binary from MSB left to LSB right (big endian)
def BigEndianBinaryToDecimal(binary):
	binary.reverse()
	decimal = 0
	for idx,val in enumerate(binary):
		decimal = decimal + val*pow(2,idx)
	return decimal


E =[32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1]

def expand(bits_32):
    expanded_bits = []
    for idx in E:
        expanded_bits.append(bits_32[idx-1])
    return ''.join(expanded_bits)


S1 =   [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]

S2 =   [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]

S3 =   [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]

S4 =   [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 7],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]

S5 =   [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]

S6 =   [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]

S7 =   [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]

S8 =   [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

def sbox1(bits_6):
    row = BigEndianBinaryToDecimal([bits_6[0], bits_6[5]])
    column = BigEndianBinaryToDecimal(bits_6[1:5])
    bits_4 = decimalTo4Bits(S1[row][column])
    return ''.join(str(x) for x in bits_4)

def sbox2(bits_6):
    row = BigEndianBinaryToDecimal([bits_6[0], bits_6[5]])
    column = BigEndianBinaryToDecimal(bits_6[1:5])
    bits_4 = decimalTo4Bits(S2[row][column])
    return ''.join(str(x) for x in bits_4)

def sbox3(bits_6):
    row = BigEndianBinaryToDecimal([bits_6[0], bits_6[5]])
    column = BigEndianBinaryToDecimal(bits_6[1:5])
    bits_4 = decimalTo4Bits(S3[row][column])
    return ''.join(str(x) for x in bits_4)

def sbox4(bits_6):
    row = BigEndianBinaryToDecimal([bits_6[0], bits_6[5]])
    column = BigEndianBinaryToDecimal(bits_6[1:5])
    bits_4 = decimalTo4Bits(S4[row][column])
    return ''.join(str(x) for x in bits_4)

def sbox5(bits_6):
    row = BigEndianBinaryToDecimal([bits_6[0], bits_6[5]])
    column = BigEndianBinaryToDecimal(bits_6[1:5])
    bits_4 = decimalTo4Bits(S5[row][column])
    return ''.join(str(x) for x in bits_4)

def sbox6(bits_6):
    row = BigEndianBinaryToDecimal([bits_6[0], bits_6[5]])
    column = BigEndianBinaryToDecimal(bits_6[1:5])
    bits_4 = decimalTo4Bits(S6[row][column])
    return ''.join(str(x) for x in bits_4)

def sbox7(bits_6):
    row = BigEndianBinaryToDecimal([bits_6[0], bits_6[5]])
    column = BigEndianBinaryToDecimal(bits_6[1:5])
    bits_4 = decimalTo4Bits(S7[row][column])
    return ''.join(str(x) for x in bits_4)

def sbox8(bits_6):
    row = BigEndianBinaryToDecimal([bits_6[0], bits_6[5]])
    column = BigEndianBinaryToDecimal(bits_6[1:5])
    bits_4 = decimalTo4Bits(S8[row][column])
    return ''.join(str(x) for x in bits_4)


P =[16,  7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25]

# 32 bit permutation
def permutation(C):
    output = []
    for idx in P:
        output.append(C[idx-1])
    return ''.join(output)


''' Function f(R[i-1],K[i])
    A = last round right side output (R[i-1])
    J = key (K[i])
'''
def f(A, J):
    print "\nf(R[i-1],K[i]) Function"
    print " Rightside: " + str(A)
    # expand 32 input bits
    A_48 = expand(A)
    print " Expansion: " + str(A_48)

    # xor 48 expanded bits with 48 key bits
    B = []
    for idx in range(48):
        B.append(int(A_48[idx])^int(J[idx]))
    print " XOR: " + ''.join(str(x) for x in B)

    # S-box transformation of 48 bits into 32 bits
    C = []
    C.append(sbox1(B[0:6]))
    C.append(sbox2(B[6:12]))
    C.append(sbox3(B[12:18]))
    C.append(sbox4(B[18:24]))
    C.append(sbox5(B[24:30]))
    C.append(sbox6(B[30:36]))
    C.append(sbox7(B[36:42]))
    C.append(sbox8(B[42:48]))
    C = ''.join(C)
    print " S-box output: " + str(C)

    # 32 bit permutation
    output = permutation(C)
    print " Permutation: " + str(output) + "\n"
    return output


def round(M, K):
    leftside = M[:32]
    rightside = M[32:]
    # calculate f function
    output = f(rightside,K)
    # update new leftside from old rightside
    new_leftside = rightside
    # update new rightside as xor from function output and old leftside
    new_rightside = []
    for idx in range(32):
        new_rightside.append(int(leftside[idx])^int(output[idx]))
    print " XOR: " + ''.join(str(x) for x in new_rightside)
    return new_leftside + ''.join(str(x) for x in new_rightside)


KP =   [57, 49, 41, 33, 25, 17,  9,
         1, 58, 50, 42, 34, 26, 18,
        10,  2, 59, 51, 43, 35, 27,
        19, 11,  3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
         7, 62, 54, 46, 38, 30, 22,
        14,  6, 61, 53, 45, 37, 29,
        21, 13,  5, 28, 20, 12,  4]

def keyPermutation(K):
    output = []
    for idx in KP:
        output.append(K[idx-1])
    return ''.join(output)

KP2 =  [14, 17, 11, 24,  1,  5,
         3, 28, 15,  6, 21, 10,
        23, 19, 12,  4, 26,  8,
        16,  7, 27, 20, 13,  2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32]

def keyPermutation2(K):
    output = []
    for idx in KP2:
        output.append(K[idx-1])
    return ''.join(output)


def shiftLeft(bits_28):
    firstbit = bits_28[0]
    shiftedbits = []
    for idx in range(1,28):
        shiftedbits.append(bits_28[idx])
    shiftedbits.append(firstbit)
    return ''.join(shiftedbits)

def shiftLeft2(bits_28):
    first2bits = bits_28[0:2]
    shiftedbits = []
    for idx in range(2,28):
        shiftedbits.append(bits_28[idx])
    shiftedbits.append(first2bits)
    return ''.join(shiftedbits)


def createRoundKeys(K):
    key_56 = keyPermutation(K)
    C = [key_56[:28]]
    D = [key_56[28:]]
    keys = []
    for i in range(1,17):
        if i == 1 or i == 2 or i == 9 or i == 16:   # shift 1 time
            C.append(shiftLeft(C[i-1]))
            D.append(shiftLeft(D[i-1]))
        else:                                       # shift 2 times
            C.append(shiftLeft2(C[i-1]))
            D.append(shiftLeft2(D[i-1]))
        keys.append(keyPermutation2(C[i]+D[i]))
    return keys

IP =   [58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17,  9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7]

def initialPermutation(M):
    output = []
    for idx in IP:
        output.append(M[idx-1])
    return ''.join(output)

FP =   [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41,  9, 49, 17, 57, 25]

def finalPermutation(M):
    output = []
    for idx in FP:
        output.append(M[idx-1])
    return ''.join(output)



if __name__ == "__main__":
    M = '0000000100100011010001010110011110001001101010111100110111101111'
    K = '0001001100110100010101110111100110011011101111001101111111110001'

    subkeys = createRoundKeys(K)

    M = initialPermutation(M)

    for i in range(16):
        print "\nRound " + str(i+1)
        print "Round input:  " + str(M[:32]) + "  " + str(M[32:])
        print "Round key:    " + str(subkeys[i])
        M = round(M,subkeys[i])
        print "Round output: " + str(M[:32]) + "  " + str(M[32:])

    cipherbits = finalPermutation(M[32:]+M[:32])
    print "Final cipherbits: " + str(cipherbits)
