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


# extended Eclidean algorithm
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
	gcd, x, y = gcdExtended(a, m)
	if gcd != 1:
		print "Inverse doesn't exist"
		res = ''
	else:
		res = (x%m + m) % m
	return res


if __name__ == "__main__":

    print "Normal way: " + str(pow(652,849)%4847)

    # calculate pow(652,849)%4847 in a more efficient way
    a = 652
    k = 849
    n = 4847
    result = modularExponentiation(a,k,n)
    print "Repeated squaring method: " + str(result)

    a = 3125
    m = 9987
    a = 28
    m = 75
    result = findModularInverse(a, m)
    print result
