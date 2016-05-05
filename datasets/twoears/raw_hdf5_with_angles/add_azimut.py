import h5py, sys, math, subprocess
import numpy as np

file_path = sys.argv[1] # path to hdf5

# format file name to get angle
file_path_ = file_path.split("/")
while True:
    try:
        file_path_.remove('')
    except:
        break
file_name = file_path_[-1]
sign = file_name[0:3]
abs_angle = int(file_name[3:5])
if sign == "pos":
    angle_deg = abs_angle
else:
    angle_deg = - abs_angle
angle_rad = math.radians(angle_deg)

for phase in ["test", "train"]:
    h5_path = file_path + "twoears_data_" + phase + ".h5"
    f = h5py.File(h5_path, "r+")

    dimensions = f["amsFeatures"].size
    print "H5PY file {} has {} entries.".format(h5_path, dimensions)

    dset = f.create_dataset("azimuth_deg", (dimensions, 1, 1, 1), dtype="float64")
    dset[:,0,0,0] = np.ones(dimensions) * angle_deg
    print "    > 'azimuth_deg' printed to file"

    dset = f.create_dataset("azimuth_rad", (dimensions, 1, 1, 1), dtype="float64")
    dset[:,0,0,0] = np.ones(dimensions) * angle_rad
    print "    > 'azimuth_rad' printed to file"

    dset = f.create_dataset("azimuth_binnames", (5,), dtype="float64")
    binnames = np.array([-90., -45., 0., 45., 90.])
    dset[...] = binnames
    print "    > 'azimuth_binnames' printed to file"

    dset = f.create_dataset("azimuth_bin", (dimensions, 1, 5, 1), dtype="float64")
    binnum = np.argmax([angle_deg == binnames[i] for i in range(len(binnames))])
    dset[:,0,binnum,0] = np.ones(dimensions)
    print "    > 'azimuth_bin' printed to file"

    f.close()

print "All new entries in degree ({}) and radian ({}) written to train/test files.".format(angle_deg, angle_rad, h5_path)
