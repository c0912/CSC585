"""
Script: prepare_svm_training_data.py
Author: Chinmai

This script extracts feature files from subject folders and
creates training data.
"""

import datetime

# Get Current data and time
now = datetime.datetime.now()

import os
import sys
import shutil
from subprocess import call

# Import all functions from utils.py
from utils import *

home = os.path.abspath('..')
dest = os.path.join(home,'Training','SVM')

def main():

	global home,dest
	global Errors,log

	# Set experiment directory and choice directory
	exp_dir = os.path.join(home,'subjects')

	# Get a list of all Subjects
	subjects = filter(lambda x:filter_hidden_folders(x,exp_dir),os.listdir(exp_dir))
	subjects.sort()

	region  = 'Amygdala'
	feature = 'Average'
	choice  = 'Gambles'

	# Training file path and name
	tr_path = os.path.join(dest,choice,region,feature)
	tr_name = choice[:3]+'_'+region[:3]+'_'+feature[:3]+'.train'
	tr_file = os.path.join(tr_path,tr_name)
	print 'Training filename: ',tr_file

	# Open training file
	tr = open(tr_file,'w')
	temp_data = ''
	for sub in subjects:

		# First let's aim to create training file for 
		# Experiences -> Hippocampus -> Avg
		feat_fold = os.path.join(exp_dir,sub,'SVM_Features',choice,region)

		files = filter(lambda x:filter_hidden(x),os.listdir(feat_fold))
		for fl in files:
			if 'avg' in fl:
				feat_file = fl

		print sub,':',feat_file
		temp_fl = open(os.path.join(feat_fold,feat_file))
		temp_data = temp_data + temp_fl.read()

		temp_fl.close()
	
	tr.write(temp_data)
	tr.close()

main()	
