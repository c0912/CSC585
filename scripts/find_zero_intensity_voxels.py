"""
Script: find_zero_intensity_voxels.py
Author: Chinmai

This script should be run after CSV extraction.

This script goes through the CSV files in All region folder line by line
and indentifies any zero intensity rows for all subjects.

Prints out the line number which also corresponds to voxel in VOI
"""

import os
import sys

from utils import *

home = os.path.abspath('..')


def main():

	global home

	# Set experiment directory and choice directory
	exp_dir = os.path.join(home,'subjects')
	
	# Get a list of all Subjects
	subjects = filter(lambda x:filter_hidden_folders(x,exp_dir),os.listdir(exp_dir))
	subjects.sort()

	for sub in subjects:
		print 'Subject: ',sub
		reg_path = os.path.join(exp_dir,sub,'CSV')

		regions = filter(lambda x:filter_hidden_folders(x,reg_path),os.listdir(reg_path))
		regions.sort()
		for reg in regions:
			csv_path = os.path.join(reg_path,reg)
	
			files = filter(lambda x:filter_hidden(x),os.listdir(csv_path))
			files.sort()
		
			#print '\tFile: ',fl
			fd = open(os.path.join(csv_path,files[0]),'r')
			data = fd.read()
			lines = data.split('\n')
			print '\tNo. of lines :',len(lines)
			count = 0
			for i in range(0,len(lines)-1) :
				if lines[i][0] == '0':
					count = count + 1
			#print '\tZero intensity at ',i	
			print '\t\tTotal zero intensity rows in ',reg,' :',count
main()
