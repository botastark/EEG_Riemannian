import numpy as np
from scipy import signal
# from scipy import stats
from .signal_filtering import butter_bandpass_filter
# from scipy.signal import welch
from scipy.integrate import simps

fs = 250


# ___________________________________Features Extraction___________________________________#

def feature_extraction(data):  # data[trial_n, freq_band_n, channel_n, : ]

    sf = fs
    win = sf
    freqs, psd = signal.periodogram(data, sf, window='hann', scaling='density', detrend='constant')
    psd_all = []
    for i in range(0, 25):
        low, high = i * 2 + 0.5, (i + 1) * 2 + 0.5
        idx_min = np.argmax(freqs > low) - 1
        idx_max = np.argmax(freqs > high) - 1
        idx = np.zeros(dtype=bool, shape=freqs.shape)
        idx[idx_min:idx_max] = 1
        a1 = psd[:, :, idx]
        a2 = freqs[idx]
        trial = simps(a1, a2)
        psd_all.append(trial)

    DE_all = np.zeros((25,))
    for m in range(0, 25):  # frequency band
        new_data = butter_bandpass_filter(data, lowcut=0.5 + m * 2, highcut=0.5 + (m + 1) * 2, fs=250, order=4)
        DE_all[m] = 0.5 * np.log(2 * np.pi * np.exp(1) * np.var(new_data))

    features_1 = psd_all
    features_1 = np.log10(features_1)
    n, = DE_all.shape
    features_2 = DE_all.reshape(n, 1, 1)
    features_11 = np.array(features_1)

    features = np.hstack((features_11, features_2))

    return np.squeeze(features, axis=2)
