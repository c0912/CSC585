"""
We will read in <Subject>.csv file from 'choices' folder and extract choices.
We write out 2 files to Subject/Behavioral Folder'
	selections: which contains the selections made by participants.
			NA -  0 (No Choice Made)
			1  -  1	(High Risk Option)
			4  - -1	(Low Risk Option)

	choice_type	: which contain which type of choice the subject is making.
			 1 - Song  (Experiential)
			-1 - Games (Monetary)
"""
import os

home = os.path.abspath('..')
path = os.path.join(home,'subjects')

choice_path = os.path.join(home,'choices')

choice_type = [1,-1,1,1,-1,1,-1,-1,1,-1]
def main():

	subjects = os.listdir(path)
	subjects.sort()

	for i in range(0,len(subjects)):
		print ('----------------------------------------------')
		print ('Processing :',subjects[i])

		fold_path = os.path.join(path,subjects[i])

		behv_path = os.path.join(fold_path,'Behavioral')

		# Check if Behavioral foler exists.
		if not os.path.isdir(behv_path):
			os.mkdir(behv_path)
	
		# Get choice File
		cfile = os.path.join(choice_path,subjects[i]+'.csv')
		if not os.path.exists(cfile):
			print ('Choice File NOT Present for ',subjects[i])
			continue
		choices = get_choices(cfile)
		print (choices)
		
		write_to_file(behv_path,choices)

def write_to_file(path,choices):
	global choice_type
	cl = len(choices) -1
	s_file = os.path.join(path,'selections')
	t_file = os.path.join(path,'choice_type')
	fs = open(s_file,'w')
	ft = open(t_file,'w')
	for i in range(0,cl):
		fs.write(str(choices[i])+'\n')
		ft.write(str(choice_type[i])+'\n')

	fs.write(str(choices[cl]))
	ft.write(str(choice_type[cl]))

	fs.close()
	ft.close()

def get_choices(cfile):

	# Number of Choices is 10
	num_ch = 10

	fd = open(cfile,'r')
	data = fd.read()
	lines = data.split('\n')
	fd.close()
	choices = []	
	# 1st line is headers, then followed by 10 lines of choices.
	# 5th column contains choices. 
	for i in range(1,num_ch+1):
		lines[i] = lines[i].split(',')
		if lines[i][4] == 'NA':
			choices.append(0)
		elif lines[i][4] == '1':
			choices.append(1)
		else:
			choices.append(-1)
	return choices
main()
