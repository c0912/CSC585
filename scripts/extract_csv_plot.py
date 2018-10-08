
import os
import sys
import shutil
from subprocess import call

home = os.path.abspath('..')
path = os.path.join(home,'subjects')

# MATLAB Path
m_path = os.path.join(home,'MATLAB')

def main():

	global path,m_path
	# Get a list of all Subjects
	subjects = os.listdir(path)
	subjects.sort()

	for sub in subjects:

		print '----------------------------------------------------------------------'
		print 'Processing : ',sub
		fold = os.path.join(path,sub)
		
		# If entry is not a directory
		if not os.path.isdir(fold):
			continue
	
		files = os.listdir(fold)
		
		# Check if plots folder is present
		if 'plots' not in files:
			print 'Plots Folder NOT Present for ',sub
			create_plots_fold(fold)
	
		if 'CSV' not in files:
			print 'CSV Folder NOT Present for ',sub
			create_CSV_fold(fold)
	
		c_path = os.path.join(fold,'CSV','All_Cube')
		if not os.path.isdir(c_path):
			os.mkdir(c_path)

		# If plotting and CSV extraction is done, continue
		#p_path = os.path.join(fold,'plots')
		#p_files = os.listdir(p_path)
		#if len(p_files) > 2:
		#	print  'Subject already Processed!'
		#	continue	

	
		# Get VTC File.
		vtc_file = get_vtc_file(fold)
		
		if  vtc_file == '':
			print 'VTC file not present for',sub
			continue

		cwd = os.getcwd()
		os.chdir(m_path)
		call(["matlab -nodisplay -r \"extract_int_cube_CO(\'%s\')\"" % (sub)],shell=True);
		os.chdir(cwd)
		
		print sub, ' successfully Processed!'
		break

def create_CSV_fold(fold_path):

	CSV_fold = os.path.join(fold_path,'CSV')
	all_fold = os.path.join(CSV_fold,'All')
	ba9l_fold = os.path.join(CSV_fold,'BA-9L')
	ba9r_fold = os.path.join(CSV_fold,'BA-9R')
	ba10l_fold = os.path.join(CSV_fold,'BA-10L')
	ba10r_fold = os.path.join(CSV_fold,'BA-10R')
	os.mkdir(CSV_fold)
	os.mkdir(all_fold)
	os.mkdir(ba9l_fold)
	os.mkdir(ba9r_fold)
	os.mkdir(ba10l_fold)
	os.mkdir(ba10r_fold)
	return

def create_plots_fold(fold_path):

	plot_fold = os.path.join(fold_path,'plots')
	scaled_fold = os.path.join(plot_fold,'scaled')
	os.mkdir(plot_fold)
	os.mkdir(scaled_fold)
	return

def get_vtc_file(fold_path):
	vtc_file = ''
	vtc_path = os.path.join(fold_path,'Functional')
	files = os.listdir(vtc_path)
	for fl in files:
		if fl.endswith('mm.vtc'):
			vtc_file = fl
	return vtc_file

main()
