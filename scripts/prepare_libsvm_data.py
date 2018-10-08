"""
Script: prepare_libsvm_data.py
Author: Chinmai

Reads in Voxel intensities from CSV and populates the Subject/SVM_Features folder.

Creates a separate folder for Games/Songs.

"""

import datetime

# Get Current data and time
now = datetime.datetime.now()

import os
import sys
import shutil

import numpy as np

# Import all functions from utils.py
from utils import *

home = os.path.abspath('..')

Errors = ''

log = 'Running vtc_to_csv.py @ '+now.strftime("%m-%d-%y %H:%M:%S")+'\n'
print log,

line_break='*******************************************************************\n'
print line_break

def main():

	global home

	# Set experiment directory and choice directory
	exp_dir = os.path.join(home,'subjects')

	# Get a list of all Subjects
	subjects = filter(lambda x:filter_hidden_folders(x,exp_dir),os.listdir(exp_dir))
	subjects.sort()

	# Reading Configuration file
	conf_file = os.path.join(home,'config')
	config = open(conf_file,'r')
	if not config:
		Errors += 'Error: Config file not present in '+exp_dir+'\n'
		print 'Error: Unable to Open Config File in ',exp_dir,line_break
		return

	param = config.read()
	param_list = param.split('\n')
	# No of functional volumes is 3rd line
	num_vol = int(param_list[2].split(':')[1])
	
	# No of choices will be the No. of CSV files output. Line 13
	csv_num = int(param_list[12].split(':')[1])	
	print 'No of choices: ',csv_num


	for sub in subjects:

		print '\tProcessing :',sub
		sub_path = os.path.join(exp_dir,sub)

		# Features Folder Path
		feat_path = os.path.join(sub_path,'SVM_Features')

		# If 'Features' folder and the sub folders doesn't exist, create them
		if not os.path.isdir(feat_path):
			create_feature_fold(feat_path)	
			#shutil.rmtree(feat_path)
		
		# Read choices from choice files.
		choice_path = os.path.join(sub_path,'Behavioral')
		choice_type,selections = get_choices(choice_path,sub)
		
		# If Unable to retrieve choice files.
		if choice_type == '' or selections =='':
			print 'Error: Unable to process choice information for ',sub
			continue
		
		# CSV Folder Path
		csv_path = os.path.join(sub_path,'CSV')

		# 4 Regions - All, Amygdala, Hippocampus, Thalamus
		regions = filter(lambda x:filter_hidden_folders(x,csv_path),os.listdir(csv_path))
		regions.sort()

		#######################r Experience(Songs) ######################################
		print '\tExtracting only Experiential choices for ',sub	
		
		for reg in regions:	#Only Amygdala for now.
			#print '\t\tProcessing Region: ',reg
			reg_path = os.path.join(csv_path,reg) 
		
			files = filter(lambda x:filter_hidden(x),os.listdir(reg_path))
			files.sort()

			f_path = os.path.join(feat_path,'Experiences',reg)	
			fa_name = sub+'_exp_'+reg+'_avg.feat'	
			fs_name = sub+'_exp_'+reg+'_std.feat'	
			fa = open(os.path.join(f_path,fa_name),'w')
			fs = open(os.path.join(f_path,fs_name),'w')

			for k in range(0,csv_num):
			
				#print 'File: ',files[k]

				# From the file name extract choice number/index
				file_nm = files[k].split('.')[0]
				choice_index = int(file_nm.split('_')[3]) -1
				
				# If choice_type is 1, then it's an experiential choice
				if int(choice_type[choice_index]) != 1:
					continue

				#print 'Choice type: ', choice_type[choice_index]

				fl_path = os.path.join(reg_path,files[k])

				m = np.loadtxt(fl_path,dtype=float,delimiter=',')
				#print 'Matrix Shape: ',m.shape

				# Average of the rows
				avg_m = np.mean(m,axis=1)

				# Standard deviation of the rows
				sig_m = np.std(m,axis=1)

				r = m.shape
			
				# Get only unique rows of the matrix
				#uniq_m = np.unique(m,axis=0)
				
				if (selections[choice_index] != '0'):  # Check no choice
					fa.write(selections[choice_index]+' ')
					fs.write(selections[choice_index]+' ')
					for l in range(0,r[0]):
						fa.write('%i:%.6f ' % (l+1,avg_m[l,]))
						fs.write('%i:%.6f ' % (l+1,sig_m[l,]))
					fa.write('\n')
					fs.write('\n')

			# Close Files	
			fs.close()	
			fa.close()
			print '\t\t',reg,' processed successfully for ',sub

		#######################r Gambles(Games) ######################################

		print '\tExtracting only Gambling choices for ',sub	
		
		for reg in regions:	#Only Amygdala for now.
			#print '\t\tProcessing Region: ',reg
			reg_path = os.path.join(csv_path,reg) 
		
			files = filter(lambda x:filter_hidden(x),os.listdir(reg_path))
			files.sort()

			f_path = os.path.join(feat_path,'Gambles',reg)	
			fa_name = sub+'_exp_'+reg+'_avg.feat'	
			fs_name = sub+'_exp_'+reg+'_std.feat'	
			fa = open(os.path.join(f_path,fa_name),'w')
			fs = open(os.path.join(f_path,fs_name),'w')

			for k in range(0,csv_num):
			
				# From the file name extract choice number/index
				file_nm = files[k].split('.')[0]
				choice_index = int(file_nm.split('_')[3]) -1
				
				# If choice_type is 1, then it's an gambling choice
				if int(choice_type[choice_index]) != -1:
					continue

				fl_path = os.path.join(reg_path,files[k])
				m = np.loadtxt(fl_path,dtype=float,delimiter=',')

				# Average of the rows
				avg_m = np.mean(m,axis=1)

				# Standard deviation of the rows
				sig_m = np.std(m,axis=1)
				r = m.shape
				
				if (selections[choice_index] != '0'):  # Check no choice made
					fa.write(selections[choice_index]+' ')
					fs.write(selections[choice_index]+' ')
					for l in range(0,r[0]):
						fa.write('%i:%.6f ' % (l+1,avg_m[l,]))
						fs.write('%i:%.6f ' % (l+1,sig_m[l,]))
					fa.write('\n')
					fs.write('\n')

			# Close Files	
			fs.close()	
			fa.close()
			print '\t\t',reg,' processed successfully for ',sub

		#######################r Both(Games & Songs) ######################################

		print '\tExtracting both Experiential & Gambling choices for ',sub	
		
		for reg in regions:	#Only Amygdala for now.
			#print '\t\tProcessing Region: ',reg
			reg_path = os.path.join(csv_path,reg) 
		
			files = filter(lambda x:filter_hidden(x),os.listdir(reg_path))
			files.sort()

			f_path = os.path.join(feat_path,'Both',reg)	
			fa_name = sub+'_exp_'+reg+'_avg.feat'	
			fs_name = sub+'_exp_'+reg+'_std.feat'	
			fa = open(os.path.join(f_path,fa_name),'w')
			fs = open(os.path.join(f_path,fs_name),'w')

			for k in range(0,csv_num):
			
				# From the file name extract choice number/index
				file_nm = files[k].split('.')[0]
				choice_index = int(file_nm.split('_')[3]) -1
				
				fl_path = os.path.join(reg_path,files[k])
				m = np.loadtxt(fl_path,dtype=float,delimiter=',')

				# Average of the rows
				avg_m = np.mean(m,axis=1)

				# Standard deviation of the rows
				sig_m = np.std(m,axis=1)
				r = m.shape
				
				if (selections[choice_index] != '0'):  # Check no choice made
					fa.write(selections[choice_index]+' ')
					fs.write(selections[choice_index]+' ')
					for l in range(0,r[0]):
						fa.write('%i:%.6f ' % (l+1,avg_m[l,]))
						fs.write('%i:%.6f ' % (l+1,sig_m[l,]))
					fa.write('\n')
					fs.write('\n')

			# Close Files	
			fs.close()	
			fa.close()
			print '\t\t',reg,' processed successfully for ',sub

def get_choices(c_path,sub):

	if not os.path.isdir(c_path):
		print 'Error: Behavioral folder not present for ',sub
		return
	files = os.listdir(c_path)
	select_file = os.path.join(c_path,'selections')
	type_file	= os.path.join(c_path,'choice_type')
	
	if not os.path.exists(select_file) or not os.path.exists(type_file):
		print 'Error: Choice files missing for ',sub
		return
	
	fs = open(select_file,'r')
	sel_data = fs.read()
	selections = sel_data.split('\n')
	fs.close()
	ft = open(type_file,'r')
	type_data = ft.read()
	choice_type = type_data.split('\n')
	ft.close()

	return choice_type,selections	

def create_feature_fold(feat_path):
	both  = os.path.join(feat_path,'Both')
	exp  = os.path.join(feat_path,'Experiences')
	gam  = os.path.join(feat_path,'Gambles')
	os.mkdir(feat_path)
	os.mkdir(both)
	create_region_fold(both)
	os.mkdir(exp)
	create_region_fold(exp)
	os.mkdir(gam)
	create_region_fold(gam)

def create_region_fold(path):

	al = os.path.join(path,'All')
	amy = os.path.join(path,'Amygdala')
	hip = os.path.join(path,'Hippocampus')
	tha = os.path.join(path,'Thalamus')
	os.mkdir(al)
	os.mkdir(amy)
	os.mkdir(hip)
	os.mkdir(tha)
	return



main()			
				
