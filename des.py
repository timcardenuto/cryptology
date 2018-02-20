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

M = '1011010001110101001001011101010101111011010100110111110010010111'
C = '1001010100101001101001101001100010011101001101001111111010100100'


def f(M):


def expand(rightside):
    expanded_bits = []
    for idx in range(0,len(rightside),4):
        expanded_bits.append(rightside[idx-1])
        expanded_bits.append(rightside[idx:idx+4])
    return ''.join(expanded_bits)


def split(M):
    leftside = M[:32]
    rightside = M[32:]
    expanded_rightside = expand(rightside)
    
