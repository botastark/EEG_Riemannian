import numpy as np
from load_data import load_data_bci_2a, load_data_bci_2b
from library.signal_filtering import signal_filtering
import os
from tqdm import tqdm

# from tqdm.notebook import tqdm_notebook

fs = 250

'''
This pre-processing file is for BCI_IV_2a and BCI_IV_2b datasets

'''


def folder(path):
    isExist = os.path.exists(path)
    if isExist:
        return
    else:
        os.makedirs(path)
        print("The new directory is created at " + path)
        return


def bci_iv_2a():
    PATH = '/Users/botaduisenbay/PycharmProjects/EEG_Riemannian/code/DATA/BCI_IV_2a/'
    # PATH = '/media/patrick/DATA/BCI_Competition/'
    data_train_addr = os.path.join(PATH, 'train/data_{}')  # subject
    data_test_addr = os.path.join(PATH, 'test/data_{}')  # subject

    label_train_addr = os.path.join(PATH, 'train/label_{}')  # subject
    label_test_addr = os.path.join(PATH, 'test/label_{}')  # subject

    data_train_filter_addr = os.path.join(PATH, 'train/EEG/filter_data_{}')  # subject
    data_test_filter_addr = os.path.join(PATH, 'test/EEG/filter_data_{}')  # subject

    folder(os.path.join(PATH, 'train/'))
    folder(os.path.join(PATH, 'test/'))
    s_filter = signal_filtering(dataset='BCI_IV_2a')

    for subject_No in tqdm(range(1, 10), desc='subject_No'):

        # _________________training_data_________________________#
        data, label = load_data_bci_2a(subject_No, True, PATH)

        filter_data = []

        for trial_No in tqdm(range(data.shape[0]), desc='trial_No train'):
            # print("trial "+str(trial_No)+ " out of "+str(data.shape[0]))
            data_trial = data[trial_No]
            filtered_data = s_filter.main(data_trial)
            filter_data.append(filtered_data)
            # break

        filter_data = np.array(filter_data)
        # print(type(filter_data))
        # print(filter_data.shape)
        # print(filter_data[0].shape)
        # return None
        np.save(data_train_filter_addr.format(subject_No), filter_data)

        np.save(data_train_addr.format(subject_No), data)
        np.save(label_train_addr.format(subject_No), label)
        print("Filtered " + str(subject_No) + 'th subject of training')

        # _________________testing_data______ ___________________#
        data, label = load_data_bci_2a(subject_No, False, PATH)
        filter_data = []
        for trial_No in tqdm(range(data.shape[0]), desc='trial_No testing'):
            # for trial_No in range(data.shape[0]):
            data_trial = data[trial_No]
            filtered_data = s_filter.main(data_trial)
            filter_data.append(filtered_data)

        filter_data = np.array(filter_data)
        np.save(data_test_filter_addr.format(subject_No), filter_data)

        np.save(data_test_addr.format(subject_No), data)
        np.save(label_test_addr.format(subject_No), label)
        print("Filtered for " + str(subject_No) + 'th subject of testing')
        # print("saved for testing  ")


def bci_iv_2b():
    D_PATH = "DATA/BCI_IV_2b/"
    # D_PATH = '/media/patrick/DATA/BCI_IV_2b/'
    L_PATH = os.path.join(D_PATH, 'true_label/')
    # fs = 250

    data_train_addr = os.path.join(D_PATH, 'train/data_{}')  # subject
    data_test_addr = os.path.join(D_PATH, 'test/data_{}')  # subject

    label_train_addr = os.path.join(D_PATH, 'train/label_{}')  # subject
    label_test_addr = os.path.join(D_PATH, 'test/label_{}')  # subject

    data_train_filter_addr = os.path.join(D_PATH, 'train/EEG/filter_data_{}')  # subject
    data_test_filter_addr = os.path.join(D_PATH, 'test/EEG/filter_data_{}')  # subject

    folder(os.path.join(D_PATH, 'train/'))
    folder(os.path.join(D_PATH, 'test/'))
    s_filter = signal_filtering(dataset='BCI_IV_2b')

    # for subject_No in (range(1, 10)):
    for subject_No in tqdm(range(1, 10), desc='subject_No'):

        # _________________training_data_________________________#

        data, label = load_data_bci_2b(subject_No, True, D_PATH, L_PATH)
        filter_data = []

        # for trial_No in range(data.shape[0]):
        for trial_No in tqdm(range(data.shape[0]), desc='trial_No train'):
            data_trial = data[trial_No]
            filtered_data = s_filter.main(data_trial)
            filter_data.append(filtered_data)

        filter_data = np.array(filter_data)
        np.save(data_train_filter_addr.format(subject_No), filter_data)

        np.save(data_train_addr.format(subject_No), data)
        np.save(label_train_addr.format(subject_No), label)
        print("Filtered for " + str(subject_No) + 'th subject of training')

        # _________________testing_data_________________________#
        data, label = load_data_bci_2b(subject_No, False, D_PATH, L_PATH)

        filter_data = []
        for trial_No in tqdm(range(data.shape[0]), desc='trial_No testing'):
            # for trial_No in range(data.shape[0]):
            data_trial = data[trial_No]
            filtered_data = s_filter.main(data_trial)
            filter_data.append(filtered_data)

        filter_data = np.array(filter_data)
        np.save(data_test_filter_addr.format(subject_No), filter_data)

        np.save(data_test_addr.format(subject_No), data)  # Use Only at the first run of this script
        np.save(label_test_addr.format(subject_No), label)
        print("Filtered for " + str(subject_No) + 'th subject of testing')

    #
