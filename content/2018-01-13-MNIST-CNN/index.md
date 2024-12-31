+++
title = "Handwritten Digit Recognition with Keras"
description = "A Convolutional Neural Network using Keras and TensorFlow that ranks well in the Kaggle MNIST handwritten digit challenge"
date = "2018-01-13"
authors = ["Everett Robinson"]
aliases = ["/2018/01/13/MNIST-CNN.html"]

[taxonomies]
tags = ["Data Science", "Python", "Computer Vision", "MNIST"]

[extra]
layout = "post"
output = "html_document"
+++


The neural network trained below was created for the [MNIST digit recognition challenge on Kaggle](https://www.kaggle.com/c/digit-recognizer). It produced a public test set accuracy of 0.99700, earning me the 94th spot out of approximately 2100 entries. This is in the top 5% of scores and well above a line in the rankings at an accuracy of 0.99514 which states "Something Fishy Going On If You're Above This". I hope you'll agree that my model isn't doing anything fishy, it just squeezes the data generation techniques available in Keras for everything they are worth.


# Importing and Splitting the Data into Training and Validation Sets

Before diving into the modelling steps, it is necessary to create a new training set and a validation set. This will allow for a fair assessment of how well the model is doing on the more general problem of digit recognition without the effects of overfitting on the training data. It also provides an opportunity to tune various parameters of the neural network such as the batch size, number of epochs for training, data generation strategy, and model architecture. Importing the provided data and then splitting it into the new training and validation sets is done using pandas and scikit-learn.


```python
from sklearn.model_selection import train_test_split
import pandas as pd
```


```python
'''
Split the provided training data to create a new training
data set and a new validation data set. These will be used
or hyper-parameter tuning.
'''

# For reproducibility
seed = 27

raw_data = pd.read_csv("../input/train.csv")

train, validate = train_test_split(raw_data, test_size=0.1, random_state = seed, stratify = raw_data['label'])
```


```python
# Split into input (X) and output (Y) variables
x_train = train.values[:,1:]
y_train = train.values[:,0]

x_validate = validate.values[:,1:]
y_validate = validate.values[:,0]

```

# Training the Convolutional Neural Network

The model below leverages Keras' built in ImageDataGenerator method with shifts in both dimensions, rotations, shear mapping, and zooming in and out. These randomly distributed transformations are useful to extend the 37,800 training samples we were provided with into a much more diverse training set. By showing the model variations of the original training images, we are also hoping that the neural network will become more robust and less overfit to patterns specific to the data we have. To this end, the model also makes extensive use of dropout, another technique designed to prevent overfitting. The hope is that all of these techniques will allow the neural network to successfully generalize to other digits it hasn't see before.


```python
'''Trains a convnet on the MNIST dataset.

Gets to 99.70% test accuracy after 32 epochs
'''

from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import ReduceLROnPlateau
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator

batch_size = 512
num_classes = 10
epochs = 32

# input image dimensions
img_rows, img_cols = 28, 28

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_validate = x_validate.reshape(x_validate.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_validate = x_validate.reshape(x_validate.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_validate = x_validate.astype('float32')
x_train /= 255
x_validate /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_validate.shape[0], 'validation samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_validate = keras.utils.to_categorical(y_validate, num_classes)

# Use the built in data generation features of Keras
datagen = ImageDataGenerator(
    width_shift_range = 0.075,
    height_shift_range = 0.075,
    rotation_range = 12,
    shear_range = 0.075,
    zoom_range = 0.05,
    fill_mode = 'constant',
    cval = 0
)

datagen.fit(x_train)

# Build the model
model = Sequential()
model.add(Conv2D(32, kernel_size = (5, 5),
                 activation = 'relu',
                 input_shape = input_shape))
model.add(Conv2D(32, kernel_size = (3, 3),
                 activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(1024, activation = 'relu'))
model.add(Dropout(0.5))

model.add(Dense(num_classes, activation = 'softmax'))

model.compile(loss = keras.losses.categorical_crossentropy,
              optimizer = keras.optimizers.Adadelta(),
              metrics = ['accuracy'])

reduce_lr = ReduceLROnPlateau(monitor = 'val_loss', factor = 0.5,
                              patience = 2, min_lr = 0.0001)

model.fit_generator(datagen.flow(x_train,
                                  y_train,
                                  batch_size = batch_size),
                    epochs = epochs,
                    steps_per_epoch = x_train.shape[0]/32,
                    verbose = 1,
                    validation_data = (x_validate, y_validate),
                    callbacks = [reduce_lr])

score = model.evaluate(x_validate, y_validate, verbose = 0)
print('Validation loss:', score[0])
print('Validation accuracy:', score[1])
```

```python
# Generate predictions using the test set data
import numpy as np

test = pd.read_csv("../input/test.csv").values[:,:]

if K.image_data_format() == 'channels_first':
    test = test.reshape(test.shape[0], 1, img_rows, img_cols)
else:
    test = test.reshape(test.shape[0], img_rows, img_cols, 1)

test = test.astype('float32')
test /= 255

pred = np.argmax(model.predict(test), axis = 1)
submission = pd.DataFrame(data = pred, columns = ['Label'])
submission['ImageId'] = submission.index + 1
submission = submission[['ImageId', 'Label']]

#submission.to_csv("submissions/Jan-13-2018.csv", index = False)
#model.save("models/Jan-13-2018.hdf5")
```
