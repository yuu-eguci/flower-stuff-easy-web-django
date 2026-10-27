"""Creates legacy_model.h5, a tiny stand-in for the real model.

It was run with the original stack (Python 3.8, TensorFlow 2.6.0) so the file
has the same HDF5 format as the model on Google Drive:

    python app/tests/fixtures/make_legacy_model.py

The Dense kernel is zero, so the output depends only on the bias:
Sunflower > Tulip > Daisy for every image.
"""

import os

import numpy
import tensorflow

CLASSES = sorted([
    'Anthurium', 'Bluebell', 'Buttercup', 'ColtsFoot', 'Cowslip', 'Crocus',
    'Daffodil', 'Daisy', 'Dandelion', 'Fritillary', 'Hydrangea', 'Iris',
    'LilyValley', 'Pansy', 'Snowdrop', 'Sunflower', 'Tigerlily', 'Tulip',
    'Windflower',
])
BIAS = {'Sunflower': 5.0, 'Tulip': 3.0, 'Daisy': 1.0}


def main():
    inputs = tensorflow.keras.Input(shape=(299, 299, 3))
    x = tensorflow.keras.layers.Conv2D(2, 3, strides=8)(inputs)
    x = tensorflow.keras.layers.GlobalAveragePooling2D()(x)
    dense = tensorflow.keras.layers.Dense(len(CLASSES), activation='softmax')
    outputs = dense(x)
    model = tensorflow.keras.Model(inputs, outputs)
    bias = numpy.array([BIAS.get(name, 0.0) for name in CLASSES], dtype='float32')
    dense.set_weights([numpy.zeros((2, len(CLASSES)), dtype='float32'), bias])
    model.save(os.path.join(os.path.dirname(__file__), 'legacy_model.h5'))


if __name__ == '__main__':
    main()
