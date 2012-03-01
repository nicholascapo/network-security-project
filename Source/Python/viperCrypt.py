#!/usr/bin/env python

from __future__ import print_function

sbox_file = '../sboxes.text'
permutations_file = '../permutations.text'
sboxes = {}
permutations = []
inversePermutations = []
ROUND_COUNT = 32

#########################################
def parse_S_Boxes():
	for line in open(sbox_file, 'r'):
		name = line.split(':')[0]
		values = [int(v) for v in line.split(':')[1].split()]
		sboxes[name] = values
		
	# assertions to check that we got the right data
	# not secure, just a sanity check
	assert sboxes['S0'][7]  == 11
	assert sboxes['S1'][3]  ==  7
	assert sboxes['S2'][5]  == 12
	assert sboxes['S3'][15] == 14
	assert sboxes['S4'][2]  ==  8
	assert sboxes['S5'][1]  ==  5
	assert sboxes['S6'][4]  ==  8
	assert sboxes['S7'][13] == 3
	for l in sboxes:
		assert len(sboxes[l]) == 16

#########################################
def parse_Permutations():
	input_file = open(permutations_file, 'r')
	data = input_file.read()
	input_file.close()
	
	data = data.replace('\n', '')
	
	permutations = [int(v) for v in data.split('//')[2].split(',')]
	inversePermutations = [int(v) for v in data.split('//')[4].split(',')]

	# assertions to check that we got the right data
	# not secure, just a sanity check
	assert len(permutations) == 128
	assert permutations[14] == 67
	assert permutations[-21] == 122
	assert len(inversePermutations) == 128
	assert inversePermutations[25] == 100
	assert inversePermutations[-9] == 95
	
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
def permutation(data, permutation_table):
	result = ''
	for b in permutation_table:
		result += data[b]
	return result

#########################################
def keystream():
	pass
	
#########################################
# maybe this should be combined with permutation()
def sBox(data, sBox):
	result = ''
	for b in sBox:
		result += data[b]
	return result

#########################################
def linearTransform(a, b, c, d):
	pass
	

#########################################
def do_round(data, subkey, sbox):
	result = ''
	intermidiate = ''
	# 1. Key Mixing: At each round, a 128-bit subkey Ki is exclusive or’ed
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

	a, b, c, d = sbox(a, b, c, d)
	
	# 3. Linear Transformation: The 32 bits in each of the output words are
	# linearly mixed
	
	intermediate = linearTransform(a, b, c, d)
	
	result = a + b + c + d
	
	return result
	
	
## EOF ##
