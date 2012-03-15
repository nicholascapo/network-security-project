#!/usr/bin/env python

from __future__ import print_function
import viperCrypt
import argparse
import sys

def main():

	args = parse_args()
	
	output = viperCrypt.crypt(args.input_block, args.key, args.encrypt)
	
	print(output)

#######################################
def parse_args():
	# Signature:
	# viper-test [ -h | --help ] [ -e | -d | --encrypt | --decrypt] [ -k | --key KEY ] input block
	parser = argparse.ArgumentParser(description='Single block testing implementation of the Serpent Cipher')

	# Decrypt
	parser.add_argument('-d', '--decrypt', action='store_false', help='decrypt the input', dest='encrypt')
	
	# Encrypt
	parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt the input', dest='encrypt')
	
	# Key
	parser.add_argument('-k', '--key', action='store', dest='key', help='the key to use', required=True)

	# Input Block
	parser.add_argument('input_block', action='store')

	args = parser.parse_args()
	return args
	
#######################################
if __name__ == '__main__': main()
