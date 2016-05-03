How to format twoears clean sounds into HDF5 for caffe:

ssh -X alioth
matlab
% matlab commands:
cd src/nideep/datasets/twoears/
% format train set
fpath_src = '/mnt/raid/data/ni/twoears/jmrepos/twoears-identification-training-pipeline/test/DNN data clean sounds/train/dataStoreUni.mat';
dir_dst = '/mnt/antares_raid/home/kashefy/data/twoears/clean_data123' % directory must exist
twoears2hdf5(fpath_src, dir_dst);
% same for test set
fpath_src = '/mnt/raid/data/ni/twoears/jmrepos/twoears-identification-training-pipeline/test/DNN data clean sounds/test/dataStoreUni.mat';
dir_dst = '/mnt/antares_raid/home/kashefy/data/twoears/clean_data123' % directory must exist, can be same location as test set
twoears2hdf5(fpath_src, dir_dst);
exit % close matlab
# Done. Train and test set are saved in HDF5

How to balance the data:
# activate virtualenv if applicable
ipython # launch ipython intepreter
from datasets.balance_hdf5 import save_balanced_class_count_hdf5 
# train set:
fpath_src = '/home/kashefy/data/twoears/clean2/twoears_data_train.h5'
fpath_dst = '/home/kashefy/data/twoears/clean2/bal/twoears_data_train.h5' # parent directory must exist
keys = [u'amsFeatures', u'label_scalar', u'ratemap'] # make sure classnames are not included
idxs = save_balanced_class_count_hdf5(fpath_src, keys, fpath_dst, key_label='label', other_clname='general')
# test set
fpath_src = '/home/kashefy/data/twoears/clean2/twoears_data_test.h5'
fpath_dst = '/home/kashefy/data/twoears/clean2/bal/twoears_data_test.h5' # parent directory must exist
idxs = save_balanced_class_count_hdf5(fpath_src, keys, fpath_dst, key_label='label', other_clname='general')

# if HDF5 files are too large for caffe, you can split them into several smaller HDF5 files
ipython # launch ipython intepreter
from iow.to_hdf5 import split_hdf5
fpath_src = '/home/kashefy/data/twoears/clean2/twoears_data_train.h5'
paths = split_hdf5(fpath_src, '/home/kashefy/data/twoears/clean2/split/')
# create a txt file in which each line contains the absolute path of each new smaller HDF5
