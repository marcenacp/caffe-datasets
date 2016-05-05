"""
Concatenate a list of HDF5 files given as arguments. Datasets with "name" in their names shall not be concatenated.
"""

import h5py, sys
import numpy as np

file_paths = sys.argv[1:] # paths to hdf5 files

def get_name(file_path, phase):
    return file_path + "twoears_data_" + phase + ".h5"

for phase in ["train", "test"]:
    # Get names / types / shapes of datasets
    with h5py.File(get_name(file_paths[0], phase), "r") as f:
        dsets = f.keys()
        dtypes = [f[dset].dtype for dset in dsets]
        shapes = [f[dset].shape for dset in dsets]

    # Get sum of sizes for each dataset
    sizes = np.zeros((len(file_paths), len(dsets)), dtype=object)
    for i, file_path in enumerate(file_paths):
        with h5py.File(get_name(file_path, phase), "r") as f:
            for j, dset in enumerate(dsets):
                sizes[i,j] = f[dset].shape[0]
    sum_sizes = np.sum(sizes, axis=0)

    # Separate datasets to concatenate (not classnames, etc!)
    dsets_toconcat = []
    for dset in dsets:
        if not "names" in dset:
            dsets_toconcat.append(dset)

    # Concatenate datasets in dsets_toconcat
    f = h5py.File(get_name("", phase), "w")
    for j, carac in enumerate(zip(dsets, shapes, sum_sizes, dtypes)):
        first_line, last_line = 0, 0
        dset, shape, size, dtype = carac
        if dset in dsets_toconcat:
            # Create datasets
            new_shape = np.array(shape)
            new_shape[0] = size
            f.create_dataset(dset, new_shape, dtype=dtype)
            print "Datasets:", dset
            print "    Original shape:", shape
            print "    New shape:", new_shape
            print "    Type:", dtype

            # Fill in datasets
            for i, file_path in enumerate(file_paths):
                last_line += sizes[i,j]
                with h5py.File(get_name(file_path, phase), "r") as f_tocopy:
                    f[dset][first_line:last_line] = f_tocopy[dset][:]
                first_line = last_line
    f.close()

    print "Concatenation terminated for {} file.".format(phase)
