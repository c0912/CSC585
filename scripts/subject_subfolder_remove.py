"""

Script: subject_subfolder_remove.py
Author: Chinmai

This script takes in the name of the sub folder that should be
deleted from within each subject folder.

Script to be place in scripts folder. In the same level as subjects folder.

"""
import shutil
import os

del_fold = "SVM_Features"

home = os.path.abspath('..')
sub_dir = os.path.join(home,'subjects')


def main():
	global home, sub_dir
	global del_fold

	# List all subjects
	subjects = filter(lambda x:filter_hidden_folders(x,sub_dir),os.listdir(sub_dir))
	subjects.sort()

	for sub in subjects:
		fold = os.path.join(sub_dir,sub,del_fold)

		if os.path.exists(fold):
			shutil.rmtree(fold)

		print del_fold,' deleted for ',sub


def filter_hidden(x):
	if x[0] != '.' :
		return True
	else:
		return False

def filter_hidden_folders(x,path):
	"""
	x:	  is the name of the folder 
	path: is the absolute path of the folder

	A filter to remove any files or hidden folders and return a list
	of folders present in path.
	"""
	if x[0] != '.' and os.path.isdir(os.path.join(path,x)):
		return True
	else:
		return False









