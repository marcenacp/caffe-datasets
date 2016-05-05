# Two!Ears - Format and prepare files for Caffe

How to format Two!Ears clean sounds into HDF5 for Caffe. Initial raw data should be in `raw_hdf5`. They'll be moved to `raw_hdf5_with_angles` and then to `concatenate_hdf5`/`concatenate_hdf5/bal`/`concatenate_hdf5/split`.

## Get train and test data

```
ssh -X alioth
matlab
% matlab commands:
cd src/nideep/datasets/twoears/
% format train set
fpath_src = '/mnt/raid/data/ni/twoears/kashefy/localization/clean_multiAzimuth/pos45_0/train/dataStoreUni.mat';
dir_dst = '/mnt/scratch/pierre/raw_hdf5/pos45_0/'; % directory must exist
twoears2hdf5(fpath_src, dir_dst);
% same for test set
fpath_src = '/mnt/raid/data/ni/twoears/kashefy/localization/clean_multiAzimuth/pos45_0/test/dataStoreUni.mat';
dir_dst = '/mnt/scratch/pierre/raw_hdf5/pos45_0/'; % directory must exist, can be same location as train set
twoears2hdf5(fpath_src, dir_dst);
exit % close matlab
```

Now that it's done train and test set are saved in HDF5.

## Angle 0

The data for azimuth 0 is to find under: `/home/kashefy/data/twoears/clean2`.

```
cp /home/kashefy/data/twoears/clean2/twoears_data_test.h5 /mnt/scratch/pierre/raw_hdf5/pos00_0/twoears_data_test.h5
cp /home/kashefy/data/twoears/clean2/twoears_data_train.h5 /mnt/scratch/pierre/raw_hdf5/pos00_0/twoears_data_train.h5
```

## Add property to HDF5

The script `add_azimut.py` currently add angle labels, but can be easily adapted to add anything. Copy the directories previously obtained and execute:

```
cd raw_hdf5_with_angles
python add_azimut.py path_to_directory # directory should contain twoears_data_test.h5 and twoears_data_train.h5
```

## Concatenate several HDF5 files

The script `concatenate.py` concatenates train and test sets simultaneously appending all datasets with the same names except the ones which contain "names" in their name (data descriptor). Both train and test sets should be in the same directories.

```
cd concatenate_hdf5
python concatenate.py path_to_directory1 path_to_directory2  # directories should contain twoears_data_test.h5 and twoears_data_train.h5
```

## Balance data

How to balance the data:

```
# activate virtualenv if applicable
ipython # launch ipython intepreter
from nideep.datasets.balance_hdf5 import save_balanced_class_count_hdf5
# train set:
fpath_src = '/mnt/scratch/pierre/concatenate_hdf5/twoears_data_train.h5'
fpath_dst = '/mnt/scratch/pierre/concatenate_hdf5/bal/twoears_data_train.h5' # parent directory must exist
keys = [u'amsFeatures', u'label_scalar', u'ratemap', u'azimuth_bin', u'azimuth_deg', u'azimuth_rad'] # make sure u'classnames' and u'label' are not included
idxs = save_balanced_class_count_hdf5(fpath_src, keys, fpath_dst, key_label='label', other_clname='general')
# test set
fpath_src = '/mnt/scratch/pierre/concatenate_hdf5/twoears_data_test.h5'
fpath_dst = '/mnt/scratch/pierre/concatenate_hdf5/bal/twoears_data_test.h5' # parent directory must exist
idxs = save_balanced_class_count_hdf5(fpath_src, keys, fpath_dst, key_label='label', other_clname='general')
```

## Split data

If HDF5 files are too large for caffe, you can split them into several smaller HDF5 files:

```
ipython # launch ipython intepreter
from nideep.iow.to_hdf5 import split_hdf5
# train set
fpath_src = '/mnt/scratch/pierre/concatenate_hdf5/twoears_data_train.h5'
paths = split_hdf5(fpath_src, '/mnt/scratch/pierre/concatenate_hdf5/split')
# create a txt file in which each line contains the absolute path of each new smaller HDF5
# test set
fpath_src = '/mnt/scratch/pierre/concatenate_hdf5/twoears_data_test.h5'
paths = split_hdf5(fpath_src, '/mnt/scratch/pierre/concatenate_hdf5/split')
# create a txt file in which each line contains the absolute path of each new smaller HDF5
```
