#!/usr/bin/env python

from __future__ import print_function
import argparse
import sys

def main():

	args = parse_args()
	print(args)

#######################################
def parse_args():
	# Signature:
	# viper [ -h | --help ] [ -e | -d | --encrypt | --decrypt ] [ -t | --threads NUM ] [ -k | --key KEY ]

	parser = argparse.ArgumentParser(description='Single block testing implementation of the Serpent Cipher')

	# Decrypt
	parser.add_argument('-d', '--decrypt', action='store_false', help='decrypt the input', dest='encrypt')
	
	# Encrypt
	parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt the input', dest='encrypt')

	# Threads
	parser.add_argument('-t', '--threads', action='store', help='number of threads to use', dest='thread_count', type=int, default=1)
	
	# Key
	parser.add_argument('-k', '--key', action='store', dest='key', help='the key to use', required=True)

	args = parser.parse_args()
	return args
	
#######################################
if __name__ == '__main__': main()
