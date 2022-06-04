import numpy as np
from utils import load_dataset_feature_addr, load_dataset_signal_addr
from tqdm import tqdm
from library.feature_extraction import feature_extraction

dataset_name = 'BCI_IV_2a'


# DO preprocessing
# preprocessing.bci_iv_2a()
# preprocessing.bci_iv_2b()
# dataset = 'BCI_IV_2a'

# Do feature extraction


# PATH = '/Users/botaduisenbay/PycharmProjects/EEG_Riemannian/code/DATA/BCI_IV_2b/'
# eeg_path = os.path.join(PATH, 'train/EEG/')
# EEG_files = sorted(
#     [os.path.join(eeg_path, f) for f in os.listdir(eeg_path) if os.path.isfile(os.path.join(eeg_path, f))])
# print(EEG_files)


def windowing(signal, fs=250):
    # print(signal.shape)
    window_size = fs
    ch, size = signal.shape
    N_windows = size // window_size
    L = 2 * N_windows - 1
    out = np.zeros((L, ch, window_size))
    for i in range(L):
        start_id = int(i * window_size // 2)
        end_id = int(i * window_size / 2 + window_size)
        # print("start is "+str(start_id)+" end id "+str(end_id))
        out[i] = signal[:, start_id: end_id]
    # print(out.shape)
    return out


# def extract_fast(filtered_data):
#     trial_n, freq_band_n, channel_n, t = filtered_data.shape
#     data = np.reshape(filtered_data, (trial_n * freq_band_n * channel_n, t))
#     windowed = windowing(data)
#     L, N, t = windowed.shape
#     data_FE = np.reshape(windowed, (L * N, t))
#     features = []
#     fs = 250
#     window_size = fs
#     for i in tqdm(range(0, L*N), desc=' data N'):
#         d = data_FE[i]
#         window = d.reshape(1, 1, window_size)
#         feature = np.transpose(feature_extraction(window))
#         features.append(np.reshape(feature, (feature.shape[0] * feature.shape[1])))
#
#     features_arr = np.array(features)
#     features_arr = np.reshape(features_arr, (L, trial_n, freq_band_n, channel_n, 50))
#     features_arr = np.reshape(features_arr, (L, trial_n, freq_band_n, channel_n * 50))
#     all_features = np.transpose(features_arr, (1, 2, 0, 3))
#
#     print(all_features.shape)
#     return all_features


def extract(filtered_data):
    trial_n, freq_band_n, channel_n, t = filtered_data.shape
    features_all = np.zeros((trial_n, freq_band_n, 7, 2 * 25 * channel_n))
    for tr in tqdm(range(0, trial_n), desc=' trial N'):
        features_per_trial = np.zeros((freq_band_n, 7, 2 * 25 * channel_n))
        for freq in range(0, freq_band_n):
            a = filtered_data[tr, freq, :, :]
            windows = windowing(a, 250)
            for w, window in enumerate(windows):
                features = np.zeros((2, 25, channel_n))
                for ch in range(0, channel_n):
                    ch_wise_window = window[ch]
                    t, = ch_wise_window.shape
                    ch_wise_window = ch_wise_window.reshape(1, 1, t)
                    features[:, :, ch] = np.transpose(feature_extraction(ch_wise_window))
                feature = np.reshape(features, (features.shape[0] * features.shape[1] * features.shape[2]))
                features_per_trial[freq, w, :] = feature
        # print("features_per_trial shape " + str(features_per_trial.shape))
        features_all[tr] = features_per_trial
    # print("features_all shape " + str(features_all.shape))
    return features_all
    # np.save(out_data_train_addr.format(subject_No), features_all)


def extract_feature_bci(subject_No):
    addr_dict = load_dataset_signal_addr(dataset_name)
    data_train_addr, data_test_addr, label_train_addr, label_test_addr = list(addr_dict.values())

    out_addr_dict = load_dataset_feature_addr(dataset_name)
    out_data_train_addr, out_data_test_addr, out_label_train_addr, out_label_test_addr = list(out_addr_dict.values())

    # Train data
    filtered_data = np.load(data_train_addr.format(subject_No), allow_pickle=True)
    features_all = extract(filtered_data)
    np.save(out_data_train_addr.format(subject_No), features_all)

    # Test data
    filtered_data = np.load(data_test_addr.format(subject_No), allow_pickle=True)
    features_all = extract(filtered_data)
    np.save(out_data_test_addr.format(subject_No), features_all)


for subject_No in tqdm(range(1, 10), desc='subject_No'):
    extract_feature_bci(subject_No)

    # break
