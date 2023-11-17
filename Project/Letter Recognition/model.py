import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Activation
from keras.optimizers import Adam
from keras.callbacks import LearningRateScheduler, ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator


import matplotlib.pyplot as plt


# Load the data
train = pd.read_csv("data/data.csv")
X = train.drop("character", axis=1)
y0 = train["character"]
binencoder = LabelBinarizer()
y = binencoder.fit_transform(y0)

# Split the data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=90)
x_train = x_train / 255
x_test = x_test / 255

# Reshape the data
re_x_train = x_train.values.reshape(-1, 32, 32, 1)
re_x_test = x_test.values.reshape(-1, 32, 32, 1)

# Create an ImageDataGenerator object for data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=[0.7, 1.3],
    shear_range=0.1,
    fill_mode='nearest'
)

# Define a learning rate schedule
def scheduler(epoch, lr):
    if epoch < 10:
        return lr
    else:
        return lr * 0.9  # Example: reduce lr by 10% every epoch after 10
    
lr_scheduler = LearningRateScheduler(scheduler)

# Reduce learning rate of plateau
lr_plateau_callback = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=3,
    verbose=1
)

# Enhanced Model Architecture
model = Sequential()

# Increasing depth and filters
model.add(Conv2D(64, (3,3), padding='same', input_shape=(32, 32, 1), activation='relu'))
model.add(BatchNormalization())
model.add(Conv2D(64, (3,3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(128, (3,3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(256, (3,3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))

# Additional layers for complexity
model.add(Conv2D(512, (3,3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(512, activation='relu', kernel_regularizer='l2'))
model.add(Dropout(0.5))
model.add(Dense(46, activation='softmax'))  # Assuming 46 classes for different characters

model.summary()

# Compile the model
optimizer = Adam(lr=0.001)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Training with data augmentation
history = model.fit(
    datagen.flow(re_x_train, y_train, batch_size=32),
    validation_data=(re_x_test, y_test),
    epochs=150,  # Increased epochs
    verbose=2,
    callbacks=[lr_scheduler, lr_plateau_callback]
)


print(re_x_train.shape)
print(re_x_test.shape)
print(y_train.shape)
print(y_test.shape)


# Evaluate the model
model.evaluate(re_x_test, y_test, verbose=2)

# Plot the accuracy and loss
history_df = pd.DataFrame(history.history)
history_df.loc[:, ['loss', 'val_loss', 'accuracy', 'val_accuracy']].plot()

# Plot the confusion matrix
X_images = X.values.reshape((-1,32,32))

plt.imshow(X_images[555])
plt.show()

imgTrans = X_images[555].reshape(1,32,32,1)
predictions = model.predict(imgTrans)
binencoder.classes_[np.argmax(predictions)]

model.save('aidan.h5')
print("Saving the model as aidan.h5")
