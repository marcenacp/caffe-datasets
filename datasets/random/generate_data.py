import numpy as np
import h5py

img_size = (12, 12)
lbl_size = (9,)

nb_train_examples = 10000
nb_test_examples = int(1./3 * nb_train_examples)

train_db_path = "data/train.h5"
test_db_path = "data/test.h5"

epsilon = 0.7 # coefficient before white noise

def make_gaussian(size, fwhm = 3, center=None):
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    if center is None:
        x0 = y0 = size
    else:
        x0 = center[0]
        y0 = center[1]
    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)

def generate_data(img_size, lbl_size, nb_examples, generate_labels=True):
    d, l = [], []
    for _ in range(nb_examples):
        data = np.zeros(img_size)
        label = np.zeros(lbl_size)
        nb_blocks = 3 # Number of blocks on a side
        block_size = img_size[0]/nb_blocks
        nb_pixels = np.random.randint(nb_blocks**2)
        while nb_pixels <> 0:
            # choose a block dial
            dial_x = np.random.randint(nb_blocks)
            dial_y = np.random.randint(nb_blocks)
            dial = dial_x + nb_blocks*dial_y
            # write on label
            label[dial] = 1
            center_x = np.random.randint(block_size)
            center_y = np.random.randint(block_size)
            y_beg = block_size*dial_y
            y_end = y_beg + block_size
            x_beg = block_size*dial_x
            x_end = x_beg + block_size
            # write on data
            gaussian = make_gaussian(block_size,fwhm=2,center=(center_x, center_y))
            data[y_beg:y_end, x_beg:x_end] = gaussian
            nb_pixels -= 1
        l.append(label)
        noise = epsilon*np.random.normal(0, 1, img_size)
        d.append([data+noise]) # in brackets [] because one channel only
    if generate_labels:
        return np.array(d), np.array(l)
    return np.array([d]), None

def save_data(db_path, key_label, key_data, img_size, lbl_size, nb_examples, generate_labels=True):
    d, l = generate_data(img_size, lbl_size, nb_examples, generate_labels)
    with h5py.File(db_path, 'w') as f:
        f.create_dataset(key_data, (nb_examples, 1, img_size[0], img_size[1]), dtype="float32")
        f[key_data][:] = d
        if generate_labels:
            f.create_dataset(key_label, (nb_examples, lbl_size[0]), dtype="float32")
            f[key_label][:] = l
    pass

save_data(train_db_path, "label", "data", img_size, lbl_size, nb_train_examples)
save_data(test_db_path, "label", "data", img_size, lbl_size, nb_test_examples)
print "Data generation: done"
