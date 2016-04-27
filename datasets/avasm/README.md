# AVASM - Dataset description

The present dataset was adapted from the annotated speech database, part of the [AVASM dataset](http://perception.inrialpes.fr/~Deleforge/AVASM_Dataset/data-10.html). This adaptation is meant to simultaneously perform classification and localization on voice recordings.

The original annotated speech dataset was:
1. manually labeled in `original_data/labels.csv` (0 for male, 1 for female) [1],
2. downsampled to 16000 Hz via `original_data/resample.py`,
3. combined two-by-two to create more superposed data,
4. feature-engineered to compute the binaural features (interaural level difference or ILD) that will be used to train the convolutional neural network via `convert.py` [2],
5. shuffled and split in train/test sets for cross-validation via `convert.py`.

The obtained features are:
- in `data/` under an HDF5 file format with their respective labels,
- in `plotted_data/` as full images (after having launched `convert.py`).

------
[1] The original dataset is not meant for classification and I couldn't come up with anything better for the classification part.
[2] Features were obtained as explained in Antoine Deleforge's [paper](https://arxiv.org/abs/1408.2700).
