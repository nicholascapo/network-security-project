#!/usr/bin/env python

from __future__ import print_function

sbox_file = '../sboxes.text'
sboxes = {}

#########################################
def parse_S_Boxes():
	for line in open(sbox_file, 'r'):
		if not line: continue
		name = line.split(':')[0]
		values = [int(v) for v in line.split(':')[1].split()]
		sboxes[name] = values
		
	# assertioans to check that we got the right data
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
	pass

#########################################
def encrypt():
	pass

#########################################
def decrypt():
	pass

#########################################
def initialPermutation():
	pass

#########################################
def finalPermutation():
	pass

#########################################
def keystream():
	pass
	
#########################################
def sBox():
	pass

#########################################
def linearTransform():
	pass

#########################################
def do_round():
	pass

