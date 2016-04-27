import numpy as np
import pandas as pd
import h5py
from scipy.io import wavfile
from scipy.signal import spectrogram, get_window, decimate
from scipy.misc import imsave
from scipy import hanning
from sklearn import cross_validation

# change the following paths if needed
path_to_wav = "original_data/annotated_speech/Recorded_16000/"
path_to_labels = "original_data/labels.csv"
path_to_hdf5 = "data/avasm%s.h5"
path_to_spectrograms = "plotted_data/"
data_key = "amsFeatures"
label_key = "label"

labels = np.array(pd.read_csv(path_to_labels, header=None))
original_size, _ = labels.shape

# minimum length from all files
lengths = []
for key in range(original_size):
    name = str(key + 1)
    fs, sound = wavfile.read(path_to_wav + name + ".wav")
    lengths.append(sound.shape[0])

min_length, max_length = np.min(lengths), np.max(lengths)
min_length -= min_length % 1024
max_length -= max_length % 1024
size = np.sum(lengths / min_length)

# open hdf5 db
f = h5py.File(path_to_hdf5 % "", "w")
f.create_dataset(data_key, (size, 1, 513, 105), dtype="float32")
f.create_dataset(label_key, (size, 2), dtype="float32")

db_key = 0
for key in range(original_size):
    for v in range(lengths[key]/min_length):
        name = str(key + 1)
        fs, sound = wavfile.read(path_to_wav + name + ".wav")

        # sound's chanels from 1 to 4: left, right, front, rear
        sound = sound[v*min_length:(v+1)*min_length, :].astype('float')

        # make spectrogram out of raw sounds
        _, _, sL = spectrogram(sound[:,0], fs=fs, window=get_window('hann', 1024), nperseg=1024, noverlap=896, mode='complex')
        _, _, sR = spectrogram(sound[:,1], fs=fs, window=get_window('hann', 1024), nperseg=1024, noverlap=896, mode='complex')

        # interaural level difference
        ild = 20. * np.log(np.absolute(sR / sL))

        # normalize
        ild /= np.max(np.abs(ild))
        #substract mean along x and divide by std along x

        # add to hdf5
        f[data_key][db_key] = np.array([ild.astype("float32")]) # add 1 dimension for the image channel
        f[label_key][db_key] = np.array([labels[key,1] == i for i in range(2)]).astype("float32")
        db_key += 1

        # add to spectrograms
        imsave(path_to_spectrograms + name  + "_" + str(v) + ".jpg", ild)

f.close()

# split in train and test sets from main hdf5
f = h5py.File(path_to_hdf5 % "", "r")
X = f[data_key][:]
y = f[label_key][:]
test_size = 0.3

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=test_size)
size_train, size_test = X_train.shape[0], X_test.shape[0]

# train test
f_train = h5py.File(path_to_hdf5 % "_train", "w")
f_train.create_dataset(data_key, (size_train, 1, 513, 105), dtype="float32")
f_train.create_dataset(label_key, (size_train, 2), dtype="float32")
f_train[data_key][:] = X_train
f_train[label_key][:] = y_train

# test set
f_test = h5py.File(path_to_hdf5 % "_test", "w")
f_test.create_dataset(data_key, (size_test, 1, 513, 105), dtype="float32")
f_test.create_dataset(label_key, (size_test, 2), dtype="float32")
f_test[data_key][:] = X_test
f_test[label_key][:] = y_test

f.close()
f_train.close()
f_test.close()
