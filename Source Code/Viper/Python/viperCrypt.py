#!/usr/bin/env python

from __future__ import print_function
import sbox

ROUND_COUNT = 32

#########################################
def encrypt():
	b = '' # intermediate value
	b.number = 0
	for i in xrange(ROUND_COUNT - 1):
		b = do_round(b)
		b.number += 1
	
	# need last round change instead of doing linear transformation

	assert b.number == 31
	return b

#########################################
def decrypt():
	pass

#########################################
def keystream(userKey):
	PHI = 0x9e3779b9
	paddedUserKey = pad_key(userKey)
	tempsubkeys = paddedUserKey[::32] # 8 32-bit words
	w = []

	for i, v in enumerate(tempsubkeys):
		w[i] = rotate((w[i] - 8  ^ wi - 5 ^ wi - 3 ^ w[i] - 1 ^ PHI ^ i), 11)
	
	#{k0 , k1 , k2 , k3 } := S3 (w0 , w1 , w2 , w3 )

	
	subkeys = [k for k in w[::4]]
	

#########################################
def pad_key(key):
	pass
	# short keys with less than 256 bits are mapped to full-length keys of 256 bits
	# by appending one "1" bit to the MSB end, followed by as many "0" bits as
	# required to make up 256 bits
	
#########################################
def linearTransform(X0, X1, X2, X3):
	X0 = rotate(X0, 13)
	X2 = rotate(X2, 3)
	X1 = X1 ^ X0 ^ X2
	X3 = X3 ^ X2 ^ (X0 << 3)
	X1 = rotate(X1, 1)
	X3 = rotate(X3, 7)
	X0 = X0 ^ X1 ^ X3
	X2 = X2 ^ X3 ^ (X1 << 7)
	X0 = rotate(X0, 5)
	X2 = rotate(X2, 22)
	return X0, X1, X2, X3
	

#########################################
def rotate(data, amount):
	 return ((data << amount) | (data >> (32 - amount)))

#########################################
def do_round(data, subkey, sbox):
	result = ''
	intermidiate = ''
	# 1. Key Mixing: At each round, a 128-bit subkey Ki is exclusive or'ed
	# with the current intermediate data Bi
	
	assert len(data) == len(subkey)
	intermediate = data ^ subkey

	# 2. S-Boxes: The 128-bit combination of input and key is considered as
	# four 32-bit words. The S-box, which is implemented as a sequence of
	# logical operations (as it would be in hardware) is applied to these
	# four words, and the result is four output words. The CPU is thus
	# employed to execute the 32 copies of the S-box simultaneously,
	# resulting with Si(Bi XOR Ki)

	a, b, c, d = intermediate[::4]
	assert len(a) == 4
	assert len(b) == 4
	assert len(c) == 4
	assert len(d) == 4

	a, b, c, d = sBox(a, b, c, d)
	
	# 3. Linear Transformation: The 32 bits in each of the output words are
	# linearly mixed
	
	intermediate = linearTransform(a, b, c, d)
	
	result = a + b + c + d
	
	return result
	
## EOF ##
