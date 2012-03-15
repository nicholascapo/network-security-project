#!/usr/bin/env python

from __future__ import print_function
import sbox

ROUND_COUNT = 32

#########################################
def crypt(data, userkey, encryptionFlag):
	# Decryption is different from encryption in that
	# the inverse of the S-boxes must be used
	# in the reverse order, as well as
	# the inverse linear transformation [I dont think this is necessary] and
	# reverse order of the subkeys.

	if encryptionFlag:
		subkeyList = keystream(userKey, encryptionFlag)
		sBoxes = sbox.SBox
	else:
		subkeyList = keystream(userKey, encryptionFlag).reverse()
		sBoxes = sbox.SBoxInverse

	b = '' # intermediate value
	b.number = 0
	for i in xrange(ROUND_COUNT):
		b = do_round(b, subkeyList[i], sBoxes[i % 8])
		b.number += 1

	assert b.number == 31
	return b

#########################################
def keystream(userKey, encryptionFlag):
	PHI = 0x9e3779b9
	k = [None]*132 # initialized to have 132 spaces
	result = [None]*32 # initialized to have 32 spaces

	# We first pad the user supplied key to 256 bits, if necessary,
	# as described in section 2.
	paddedUserKey = pad_key(userKey)

	# We write the key K as eight 32-bit words
	w = paddedUserKey[::32] # 8 32-bit words

	# and expand these to an intermediate key (which we call prekey) 
	# w0 , . . . , w131 by the following affine recurrence:
	# wi := (wi-8 ^ wi-5 ^ wi-3 ^ wi-1 ^ PHI ^ i) <<< 11

	for index, value in enumerate(w):
		w[index] = rotate((w[index-8] ^ w[index-5] ^ w[index-3] ^ w[index-1] ^ PHI ^ index), 11)

	# The round keys are now calculated from the prekeys using the S-boxes,
	# again in bitslice mode. We use the S-boxes to transform the prekeys
	# wi into words ki of round key in the following way:
	# 
	# {k0 , k1 , k2 , k3 } := S3 (w0 , w1 , w2 , w3 )
	# {k4 , k5 , k6 , k7 } := S2 (w4 , w5 , w6 , w7 )
	# {k8 , k9 , k10 , k11 } := S1 (w8 , w9 , w10 , w11 )
	# {k12 , k13 , k14 , k15 } := S0 (w12 , w13 , w14 , w15 )
	# {k16 , k17 , k18 , k19 } := S7 (w16 , w17 , w18 , w19 )
	# ...
	# {k124 , k125 , k126 , k127 } := S4 (w124 , w125 , w126 , w127 )
	# {k128 , k129 , k130 , k131 } := S3 (w128 , w129 , w130 , w131 )

	for i in xrange(0, 131, 4):
		k[i+0], k[i+1], k[i+2], k[i+3] = \
		sbox.prekeyTransform(prekeySBoxIndex(encryptionFlag), w[i+0], w[i+1], w[i+2], w[i+3])

	# We then renumber the 32-bit values kj as 128-bit subkeys Ki 
	# (for i in {0, . . . ,r}) as follows:
	# Ki := {k4i , k4i+1 , k4i+2 , k4i+3 }
	
	for i in xrange(32):
		result[i] = [k[4*i+0], k[4*i+1], k[4*i+2], k[4*i+3]]
	
	return result

#########################################
# function to select correct sbox in the prekey calculation
def prekeySBoxIndex(encryptionFlag):
	start = 3
	if encryptionFlag:			
		stop = -33
		step = -1
	else:
		stop = 33
		step = 1
	for i in xrange(start, stop, step):
		yield i

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
def do_round(data, subkey, sBox):
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
