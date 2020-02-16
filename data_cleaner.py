"""
data_cleaner.py
---------------
This script prepares the data for data visualization.
"""
import os
import sys

import argparse
from load_data.load_most_recent_data import load_data

def main(args):
    ### Load Data Key
    df = load_data(args.url)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="")
	parser.add_argument("key_url", help="", action='store')
	argv = parser.parse_args()
	sys.exit(main(args=argv))