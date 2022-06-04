import numpy as np
import scipy.io as sio

'''
Load_data_from MatFile
'''


def load_data_bci_2a(subject, training, PATH):
    """	Loads the dataset 2a of the BCI Competition IV
    Keyword arguments:
    subject -- number of subject in [1, .. ,9]
    training -- if True, load training data
                if False, load testing data

    Return:	data_return 	numpy matrix 	size = NO_valid_trial x 22 x 1750
            class_return 	numpy matrix 	size = NO_valid_trial
    """
    NO_channels = 22
    NO_tests = 6 * 48
    Window_Length = 7 * 250

    class_return = np.zeros(NO_tests)  # [0. 0. 0. ... 0.]  --> 6*48 zeroes
    data_return = np.zeros((NO_tests, NO_channels, Window_Length))  # 6*48 x 22 x 7*250

    NO_valid_trial = 0
    if training:  # Load the .mat file contents into a, it is a dict
        a = sio.loadmat(PATH + 'A0' + str(
            subject) + 'T.mat')
    else:
        a = sio.loadmat(PATH + 'A0' + str(
            subject) + 'E.mat')
    # print(len(a))
    # print(a.keys())
    # a_data = a['data']  # a_data is a value corresponding to the key 'data' from the dict
    # for ii in range(0, len(a)):

    a_X = a['a_X']
    a_trial = a['a_trial']
    a_y = a['a_y']
    a_fs = a['a_fs']
    a_classes = a['a_classes']
    a_artifacts = a['a_artifacts']
    a_gender = a['a_gender']
    a_age = a['a_age']

    for trial in range(0, a_trial.size):
        # print("Trial number is " + str(trial))
        # print("Trig for trial number is " + str(a_trial[trial]))
        # print("ind for a_x are " + str(int(a_trial[trial])) + ' and ' + str(int(a_trial[trial]) + Window_Length))

        if a_artifacts[trial] != 3:
            data_return[NO_valid_trial, :, :] = np.transpose(
                a_X[int(a_trial[trial]):(int(a_trial[trial]) + Window_Length), :22])
            class_return[NO_valid_trial] = int(a_y[trial])
            NO_valid_trial += 1
    # print(NO_valid_trial)

    return data_return[0:NO_valid_trial, :, :], class_return[0:NO_valid_trial]


def load_session_2b(content, classlabel):
    NO_channels = 3
    Window_Length = 8 * 250

    data = content['s'][:, 0:3]  # EEG ONLY
    artifact = content['h']['ArtifactSelection'][0, 0]
    event_type = content['h']['EVENT'][0, 0]  # load signal struct since h.EVENT is not a dict anymore
    TYP = event_type['TYP'].item()
    POS = event_type['POS'].item()
    POS = POS.astype('int')  # convert all type to int 64
    TYP = TYP.astype('int')
    classlabel = classlabel['classlabel']
    classlabel = classlabel.astype('int')

    trial_arr = np.where(TYP == 768)[0]
    valid_trial = np.where(artifact == 0)[0]
    valid_trial_arr = trial_arr[valid_trial]
    # print(trial_arr.shape)
    valid_trial_arr = trial_arr
    data_return = np.zeros((valid_trial_arr.size, NO_channels, Window_Length))
    class_return = np.zeros((valid_trial_arr.size, 1))

    for trial in range(0, trial_arr.size):
        data_pos = POS[trial].item()
        label_pos = trial
        data_return[trial] = data[data_pos:data_pos + Window_Length, :].T
        class_return[trial] = classlabel[label_pos]

    return data_return, class_return


def load_data_bci_2b(subject, training, D_PATH, L_PATH):
    """	Loads the dataset 2b of the BCI Competition IV
        Keyword arguments:
        subject -- number of subject in [1, .. ,9]
        training -- if True, load training data
              if False, load testing data

        Return:	data_return 	numpy matrix 	size = NO_valid_trial x 3 x 2000
            class_return 	numpy matrix 	size = NO_valid_trial
    """

    NO_channels = 3
    Window_Length = 8 * 250

    session_arr = [1, 2, 3, 4, 5]
    data = np.zeros((1, 3, Window_Length))
    label = np.zeros((1,))
    if training:
        for session in range(0, 3):
            content = sio.loadmat(D_PATH + 'B0' + str(subject) + '0' + str(session_arr[session]) + 'T.mat')
            classlabel = sio.loadmat(L_PATH + 'B0' + str(subject) + '0' + str(session_arr[session]) + 'T.mat')
            data_temp, label_temp = load_session_2b(content, classlabel)

            data = np.vstack((data, data_temp))
            label = np.vstack((label, label_temp))
        data = data[1:]
        label = label[1:]
    else:
        for session in range(3, 5):
            content = sio.loadmat(D_PATH + 'B0' + str(subject) + '0' + str(session_arr[session]) + 'E.mat')
            classlabel = sio.loadmat(L_PATH + 'B0' + str(subject) + '0' + str(session_arr[session]) + 'E.mat')
            data_temp, label_temp = load_session_2b(content, classlabel)
            data = np.vstack((data, data_temp))
            label = np.vstack((label, label_temp))
        data = data[1:]
        label = label[1:]
    return data, label

#
