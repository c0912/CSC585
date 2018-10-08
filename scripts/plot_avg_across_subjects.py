"""
Plot Average Intensity plots for each Region Across Subjects
"""

import os
import numpy as np
import matplotlib.pyplot as plt

home = os.path.abspath('..')
sub_path = os.path.join(home,'subjects')

cols = 12

def main():

	global home,sub_path

	subjects = os.listdir(sub_path)
	subjects.sort()

	if len(subjects) == 0:
		print ('No Subjects Present')
		exit(1)
	
	m_song = np.zeros((1,cols))
	m_game = np.zeros((1,cols))
	for sub in subjects:         
		print ('---------------------------------------------------------------')
		print ('Processing: ',sub)
		CSV_path = os.path.join(sub_path,sub,'CSV')

		if not os.path.isdir(CSV_path):
			print ('CSV Files not present for ',sub)
			continue
	
		regions = os.listdir(CSV_path)

		for reg in regions:
			reg_path = os.path.join(CSV_path,reg)
			files = os.listdir(reg_path)	
			print ('Region:',reg,len(files))
			files.sort()

			mean_x = np.zeros((1,cols))
			for fl in files:
				#print (fl)
				f_path = os.path.join(reg_path,fl)
				x = np.loadtxt(f_path,delimiter=',')
				x = x.mean(0).reshape(1,cols)
				mean_x = np.concatenate([mean_x,x])				
			
			#print (mean_x)
			mean_x = mean_x[1:,:]
			mean_songs = mean_x[(0,2,3,5,8),:]
			mean_games = mean_x[(1,4,6,7,9),:]
			mean_songs = mean_songs.mean(0).reshape(1,cols)
			mean_games = mean_games.mean(0).reshape(1,cols)
			break
		
		m_song = np.concatenate([m_song,mean_songs])
		m_game = np.concatenate([m_game,mean_games])

	# Removing 1st row of zeros
	m_song = m_song[1:,:]
	m_game = m_game[1:,:]
	
	# Getting the Average
	m_song = m_song.mean(0)
	m_game = m_game.mean(0)		
	plt.plot(m_song,'r',label='Songs')
	plt.plot(m_game,'b',label='Games')
	plt.legend()
	plt.xlabel('Time in seconds')
	plt.ylabel('Avg Voxel Intensities')
	plt.title('Avg Intensity: Songs VS Games - Amygdala')
	plt.show()


main()
		
