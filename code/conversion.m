dataset = 1;
if dataset==1
    % For BCI C IV 2a
    subjdir = '/Users/botaduisenbay/Documents/MATLAB/NN_project/BCICIV_2a_gdf/';
    subjdir_true_labels = ['/Users/botaduisenbay/Documents/MATLAB/NN_project/' ...
        'BCICIV_2a_gdf/true_labels/'];
    outdir = '/Users/botaduisenbay/Documents/MATLAB/NN_project/BCICIV_2a_mat/';
    for i = 2:2

        files = dir(strcat(subjdir, '*.gdf'));
        files_y = dir(strcat(subjdir_true_labels, '*.mat'));
        
        for f=1:length(files)
            disp(files(f).name)
            [s,h] = sload(strcat(subjdir, files(f).name));
            true_label = load(strcat(subjdir_true_labels, files_y(f).name));

            a_X = s;
            a_trial = h.TRIG; %some list with ids 
            a_y = true_label.classlabel; %h.classlabel or from truevalue
            a_fs = h.SampleRate;
            a_classes = 4; % 4 classes
            a_artifacts = h.ArtifactSelection;
            a_gender = h.Patient.Sex;
            a_age = h.Patient.Age;
            [~ ,FileName, ~] = fileparts(files(f).name);
            save(strcat(outdir, FileName, '.mat'), ...
                'a_X', ...
                'a_trial', ...
                'a_y',...
                'a_fs',...
                'a_classes',...
                'a_artifacts',...
                'a_gender',...
                'a_age');
            %break
        end
    end

else
    subjdir = '/Users/botaduisenbay/Documents/MATLAB/NN_project/BCICIV_2b_gdf/';
    outdir = '/Users/botaduisenbay/Documents/MATLAB/NN_project/BCICIV_2b_mat/';
    for i = 2:2
  %     subjdir = strcat(datadir, sprintf('subject%2.2d/', i));
        files = dir(strcat(subjdir, '*.gdf'));
        for f=1:length(files)
            
            disp(strcat(subjdir, files(f).name))
            [s,h] = sload(strcat(subjdir, files(f).name));
            
            EVENTTYP = h.EVENT.TYP;
            EVENTPOS = h.EVENT.POS;
            EVENTDUR = h.EVENT.DUR;
            SampleRate = h.SampleRate;
            ArtifactSelection = h.ArtifactSelection;
            [~ ,FileName, ~] = fileparts(files(f).name);
            save(strcat(outdir, FileName, '.mat'), 's','h', 'EVENTTYP', 'EVENTPOS', ...
                'EVENTDUR','ArtifactSelection','SampleRate', 'FileName');
        end
    end

end
