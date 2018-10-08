% Write time courses of VOI-VTC coordinates to text file
% in MNI space
% Using NeuroElf 1.0, www.neuroelf.net
% Calculation of VTC indices is from DataSimulatorPlugin example code

function y = plot_avg_int_time(sub)
	
	% Sub is the Subject name.
	n = neuroelf;
	close all

	cd ..;
	path = pwd;

	cd MATLAB;
	
	vtc_postfix = '_exp vs gamble_SCSTBL_3DMCTS_THPGLMF2c_MNI.vtc';

	% Split Sub name to get initials and convert it to char array
	sub_initials = strsplit(sub,'_');
	initials = char(sub_initials(2));

	FileName= strcat(initials,vtc_postfix);
	PathName = strcat(path,'/subjects/',sub,'/');
	vtcname = [PathName FileName];
		   
	vtc = xff(vtcname);
		
	voiname = strcat(path,'/VOI/CG_Subcortical_MNIadapted_filled.voi');
	voiobj = xff(voiname);
	[pathstr_voi,name_voi,ext] = fileparts(voiname);
	[pathstr_vtc,name_vtc,ext] = fileparts(vtcname);

	% Cortical Regions	
	cr = {'Thalamus','Amygdala','Hippocampus'};

	trfmat = [];
	inMNIspace = strcmp(voiobj.ReferenceSpace, 'MNI');

	% Explore the VOI - VOI:BVCoords
	nrOfVOIs = voiobj.NrOfVOIs;
 
	% We will make it nrOfVOIs -1 because thalamus2 is quite big.


	% MNI: 44, -76, -2, BVsys on GUI and in VOI file: 84, 204, 130
	% the MNI matrix transforms from native to MNI, so we need:
	% 1. go back to native space: inv(MNI)
	% 2. go from native to BVsys: inv(BVsys2BVint = [0 0 1 0; 1 0 0 0;
	% 0 1 0 0; 0 0 0 1])
	
	TalMNI2sys = [		 
				-1 0 0 128
				0 -1 0 128
				0 0 -1 128
				0 0 0 1];
	
	BVsys2BVint = [ 	0	  0		1	  0
				1	  0		0	  0
				0	  1		0	  0
				0	  0		0	  1];
   
	% Empty Matrices to combine all VOI to form all region timecourse matrix
    all_regions = [];
	all_regions_scaled = [];

	for i=1:nrOfVOIs
   
		voi_coords = voiobj.BVCoords(i);	  %  alternatively use voi.TalCoords(1) and convert
		voital = voiobj.TalCoords(i);
	
	 	% use BV System coordinates (NeuroElf provides both representations)
	  	sz = size(voi_coords);
	  	voi_timecourse_matrix = zeros(sz(1), vtc.NrOfVolumes + 3);
	
	  	if inMNIspace
			for vx=1:sz(1)
				PosX = voi_coords(vx, 1);
			  	PosY = voi_coords(vx, 2);
			  	PosZ = voi_coords(vx, 3);
  
			  	coords = inv(BVsys2BVint)*TalMNI2sys*[PosX PosY PosZ 1]';
			
			  % convert to position in VTC space (from DataSimulatorPlugin)
		  
			  	posxvtc = round((coords(1) - vtc.XStart) / vtc.Resolution) + 1;
			  	posyvtc = round((coords(2) - vtc.YStart) / vtc.Resolution) + 1;
			  	poszvtc = round((coords(3) - vtc.ZStart) / vtc.Resolution) + 1;

			  	voi_timecourse_matrix(vx,:) = [PosX; PosY; PosZ; vtc.VTCData(:,posxvtc,posyvtc,poszvtc)];
			end
        end
		
		voi_timecourse_scaled = standardized_scaling(voi_timecourse_matrix);        
		
    	all_regions = [all_regions ; voi_timecourse_matrix];    
		all_regions_scaled = [all_regions_scaled ; voi_timecourse_scaled];
		
		% Plot Unscaled Time Course	
		%plot_graphs(voi_timecourse_matrix,char(cr(i)),sub,path,0);
		
		%Plot Scaled Time Course
        region = strcat(char(cr(i)),'_scaled');
		%plot_graphs(voi_timecourse_scaled,region,sub,path,1);

		% Using scaled Timecourse, write out CSV files
		write_to_csv(voi_timecourse_scaled,char(cr(i)),sub,path);
    end

    %plot_graphs(all_regions_scaled,'All',sub,path,0);
	write_to_csv(all_regions_scaled,'All',sub,path);
	%exit	
end

function y = standardized_scaling(matrix)

	% First we reshape the Matrix into a Vector
	% Doesn't matter in what order we roll out the matrix
	
	cols = size(matrix);	
	coords = matrix(:,1:3);	
	mat = reshape(matrix,[],1);
	% Leave the coords and take only values.		
	matrix = matrix(:,4:cols(2));
	% Compute the mean and standard deviation
	% By transposing the Matrix, we calculate per voxel mean & std deviation
	mu = mean(matrix');
	sig = std(matrix');
	smat = matrix' - mu;
	for i = 1:(cols(2)-3)
		smat(:,i) = smat(:,i) / sig(i);
	end	
	
	y = [coords smat'];
	
end

function y = write_to_csv(voi_timecourse_matrix,reg,sub,path)
	% Extract Region Name. Remove .csv extention

    spath = strcat(path,'/subjects/',sub,'/CSV/',reg,'/');

	f1 = strcat(spath,'1.csv');
	song1 = voi_timecourse_matrix(:,220:238);
	csvwrite(f1,song1)

	f2 = strcat(spath,'2.csv');
	game1 = voi_timecourse_matrix(:,242:260);
	csvwrite(f2,game1)

	f3 = strcat(spath,'3.csv');
	song2 = voi_timecourse_matrix(:,262:280);
	csvwrite(f3,song2)

	f4 = strcat(spath,'4.csv');
	song3 = voi_timecourse_matrix(:,286:304);
	csvwrite(f4,song3)

	f5 = strcat(spath,'5.csv');
	game2 = voi_timecourse_matrix(:,308:326);
	csvwrite(f5,game2)

	f6 = strcat(spath,'6.csv');
	song4 = voi_timecourse_matrix(:,334:352);
	csvwrite(f6,song4)

	f7 = strcat(spath,'7.csv');
	game3 = voi_timecourse_matrix(:,354:372);
	csvwrite(f7,game3)

	f8 = strcat(spath,'8.csv');
	game4 = voi_timecourse_matrix(:,374:392);
	csvwrite(f8,game4)

	f9 = strcat(spath,'9.csv');
	song5 = voi_timecourse_matrix(:,394:412);
	csvwrite(f9,song5)

	f10 = strcat(spath,'10.csv');
	game5 = voi_timecourse_matrix(:,414:432);
	csvwrite(f10,game5)

end

function y = plot_graphs(voi_timecourse_matrix,reg,sub,path,scaled)
	
	%song1 = voi_timecourse_matrix(:,222:233);
	%game1 = voi_timecourse_matrix(:,244:255);
	%song2 = voi_timecourse_matrix(:,264:275);
	%song3 = voi_timecourse_matrix(:,288:299);
	%game2 = voi_timecourse_matrix(:,310:321);
	%song4 = voi_timecourse_matrix(:,336:347);
	%game3 = voi_timecourse_matrix(:,356:367);
	%game4 = voi_timecourse_matrix(:,376:387);
	%song5 = voi_timecourse_matrix(:,396:407);
	%game5 = voi_timecourse_matrix(:,416:427);

	song1 = voi_timecourse_matrix(:,220:238);
	game1 = voi_timecourse_matrix(:,242:260);
	song2 = voi_timecourse_matrix(:,262:280);
	song3 = voi_timecourse_matrix(:,286:304);
	game2 = voi_timecourse_matrix(:,308:326);
	song4 = voi_timecourse_matrix(:,334:352);
	game3 = voi_timecourse_matrix(:,354:372);
	game4 = voi_timecourse_matrix(:,374:392);
	song5 = voi_timecourse_matrix(:,394:412);
	game5 = voi_timecourse_matrix(:,414:432);
	
	mean_song1 = mean(song1);
	mean_game1 = mean(game1);
	mean_song2 = mean(song2);
	mean_song3 = mean(song3);
	mean_game2 = mean(game2);
	mean_song4 = mean(song4);
	mean_game3 = mean(game3);
	mean_game4 = mean(game4);
	mean_game5 = mean(game5);
	mean_song5 = mean(song5);

	% Extract Region Name. Remove .csv extention
	if scaled == 0
		s_path = strcat(path,'/subjects/',sub,'/plots/');
	else
		s_path = strcat(path,'/subjects/',sub,'/plots/scaled/');
	end
	%Plot name
	p_name = strcat(reg,'_choices.png');

	f1 = figure(1);
	plot(mean_song1,'r')
	hold on
	plot(mean_song2,'r')
	plot(mean_song3,'r')
	plot(mean_song4,'r')
	plot(mean_song5,'r')
	plot(mean_game1,'b')
	plot(mean_game2,'b')
	plot(mean_game3,'b')
	plot(mean_game4,'b')
	plot(mean_game5,'b')
	hold off
	
	legend('\color{red} song','\color{blue} game')
	xlabel('Time(seconds)')
	tl = strcat(reg,'-',sub);
	title(tl)
	ylabel('Avg of intensity of all voxels')
	xlim([1,18])
	saveas(f1,strcat(s_path,p_name))
	
	songs = [mean_song1; mean_song2; mean_song3; mean_song4; mean_song5];
	games = [mean_game1; mean_game2; mean_game3; mean_game4; mean_game5];

	song_avg = mean(songs);
	game_avg = mean(games);

	%Plot name
	p_name = strcat(reg,'_avg.png');

	f2 = figure(2);
	plot(song_avg,'r');
	hold on
	plot(game_avg,'b');
	legend('songs','games')
	hold off
	xlabel('Time(seconds)')
	title(tl)
	ylabel('Avg of intensity of all voxels')
    xlim([1,18])
	saveas(f2,strcat(s_path,p_name))
	
end




