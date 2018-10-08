% Write time courses of VOI-VTC coordinates to text file
% Using NeuroElf 1.0, www.neuroelf.net

% Author : Chinmai
% Experiment : Experiences Vs Gambles

% This script Extracts VTC Data for ALL the voxels specified in VOI file.

% NOTE: The VOI files are not Cubic. They are as originally defined.
% Location: VOI/CG_Subcortical_MNIadapted_filled.voi

% Contributor: HB, 15-06-17, latest update: Chinmai 08/26/2018 

function y = export_vtc_to_csv(sub)
	
	n = neuroelf;
	close all

	cd ..;
	path = pwd;
	cd MATLAB;
	
	% Which VTC file to use - Gaussian Smooting/ No	
	%vtc_postfix = '_Script_MNI_SD3DVSS6.00mm.vtc';
	% Intials + postfix = VTC filename
	vtc_postfix = '_exp vs gamble_SCSTBL_3DMCTS_THPGLMF2c_MNI.vtc';

	% Split Sub name to get initials and convert it to char array
	sub_initials = strsplit(sub,'_');
    
	initials = char(sub_initials(2));

	FileName= strcat(initials,vtc_postfix);
	PathName = strcat(path,'/subjects/',sub,'/');
    
	vtcname = [PathName FileName];
    %X = ['VTC File: ',vtcname];
    %disp(X)
	vtc = xff(vtcname);
	voiname = strcat(path,'/VOI/CG_Subcortical_MNIadapted_filled.voi');
    %X = ['VOI File: ',voiname,'\n'];
    %disp(X)
	voiobj = xff(voiname);
	
	[pathstr_voi,name_voi,ext] = fileparts(voiname);
	[pathstr_vtc,name_vtc,ext] = fileparts(vtcname);

	% Sub cortical areas for EVG - 
	cr = {'Thalamus','Amygdala','Hippocampus'};
	
	trfmat = [];
	inMNIspace = strcmp(voiobj.ReferenceSpace, 'MNI');

	% Explore the VOI - VOI:BVCoords
	nrOfVOIs = voiobj.NrOfVOIs;
	
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
		
	BVsys2BVint = [ 0     0     1     0
	                1     0     0     0
	                0     1     0     0
	                0     0     0     1];

	% Empty Matrices to combine all VOI to form all region timecourse matrix
    all_regions = [];
	all_regions_scaled = [];
	
	% Begin Clock.
    %tic

	for i=1:nrOfVOIs
        %disp('')
        %X = ['Processing Region: ',char(cr(i))];
        %disp(X)
		%  alternatively use voi.TalCoords(1) and convert
		voi_coords = voiobj.BVCoords(i);
		voital = voiobj.TalCoords(i);
		
		% use BV System coordinates (NeuroElf provides both representations)
		sz = size(voi_coords);
        X = ['No of Coords: '];
        %disp(X)
        %disp(sz)    
		voi_timecourse_matrix = zeros(sz(1), vtc.NrOfVolumes + 3);
				        
		if inMNIspace
		    for vx=1:sz(1)
		        PosX = voi_coords(vx, 1);%[3*vx+0];
		        PosY = voi_coords(vx, 2);%[3*vx+1];
		        PosZ = voi_coords(vx, 3);%[3*vx+2];  
		        coords = inv(BVsys2BVint)*TalMNI2sys*[PosX PosY PosZ 1]';
		        
		        % convert to position in VTC space (from DataSimulatorPlugin)
		        posxvtc = round((coords(1) - vtc.XStart) / vtc.Resolution) + 1;
		        posyvtc = round((coords(2) - vtc.YStart) / vtc.Resolution) + 1;
		        poszvtc = round((coords(3) - vtc.ZStart) / vtc.Resolution) + 1;
		        
		        voi_timecourse_matrix(vx,:) = [PosX; PosY; PosZ; vtc.VTCData(:,posxvtc,posyvtc,poszvtc)];
		    end
		end
		
		%newvoiname = fullfile(pathstr_vtc, [name_voi '_voi' num2str(i) '_' name_vtc '.csv']);
		all_regions = [all_regions ; voi_timecourse_matrix]; 
		voi_timecourse_scaled = standardized_scaling(voi_timecourse_matrix);        
		all_regions_scaled = [all_regions_scaled ; voi_timecourse_scaled];
		%write_to_csv(voi_timecourse_scaled,char(cr(i)),sub,path);
		%toc
	end
	%plot_graphs(all_regions_scaled,'All',sub,path,0);
	write_to_csv(all_regions_scaled,'All',sub,path);
	%toc
	exit
end


function y = standardized_scaling(matrix)
    % We will normalize region wise. Subtract the mean intensity
    % of the entire region and divide it by standard deviation.
    
    % Doing so the mean intensity of the region will be 1 and std 1.
    
	% First we reshape the Matrix into a Vector
	cols = size(matrix);
    % Get the Coordinates out
	coords = matrix(:,1:3);
	% Get only the intensities leaving out the coordinates.
    mat = matrix(:,4:cols(2));
    % Reshape it into a vector and evaluate mean and std
	vec = mat(:);
	
	mu = mean(vec);
	sig = std(vec);

    % Standardized scaling    
	smat = mat - mu;
    smat = smat / sig;
	y = [coords smat];  % Concatenate with coords and return,
        
end

function y = write_to_csv(voi_timecourse_matrix,reg,sub,path)
	% Extract Region Name. Remove .csv extention

    spath = strcat(path,'/subjects/',sub,'/CSV/',reg,'/');
	csvwrite(strcat(spath,sub,'_',reg,'_1.csv'),voi_timecourse_matrix(:,221:240))
    csvwrite(strcat(spath,sub,'_',reg,'_2.csv'),voi_timecourse_matrix(:,241:262))
    csvwrite(strcat(spath,sub,'_',reg,'_3.csv'),voi_timecourse_matrix(:,263:282))
    csvwrite(strcat(spath,sub,'_',reg,'_4.csv'),voi_timecourse_matrix(:,283:306))
    csvwrite(strcat(spath,sub,'_',reg,'_5.csv'),voi_timecourse_matrix(:,307:328))
    csvwrite(strcat(spath,sub,'_',reg,'_6.csv'),voi_timecourse_matrix(:,329:354))
    csvwrite(strcat(spath,sub,'_',reg,'_7.csv'),voi_timecourse_matrix(:,355:374))
    csvwrite(strcat(spath,sub,'_',reg,'_8.csv'),voi_timecourse_matrix(:,375:394))
    csvwrite(strcat(spath,sub,'_',reg,'_9.csv'),voi_timecourse_matrix(:,395:414))
    csvwrite(strcat(spath,sub,'_',reg,'_10.csv'),voi_timecourse_matrix(:,415:434))

end
 
	

	
