# Dataset description

The original dataset is part of the [AVASM dataset](http://perception.inrialpes.fr/~Deleforge/AVASM_Dataset/data-10.html).

The annotated speech dataset was:
- labeled in `original_data/labels.csv` ($0$ for male, $1$ for female),
- downsampled to 16000 Hz via `original_data/resample.py`,
- combined two-by-two to create more,
- feature-engineered to compute the binaural features (interaural level difference or ILD) that will be used to train the convolutional neural network via `convert.py`,
- shuffled and split in train/test sets using cross-validation via `convert.py`.

The obtained features are:
- in `data/` under an HDF5 file format with their respective labels,
- in `plotted_data/` as full images.
