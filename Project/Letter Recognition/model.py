import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

import matplotlib.pyplot as plt


# Load the data
train = pd.read_csv("data/data.csv")
train.head()

X = train.drop("character", axis=1)
y0 = train["character"]

print(y0.unique())
print(len(y0.unique()))

# Encode the labels
binencoder = LabelBinarizer()
y = binencoder.fit_transform(y0)

y

# Split the data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=90)

x_train = x_train/255
x_test = x_test/255

print(X.shape)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

# Reshape the data
re_x_train = x_train.values.reshape(-1, 32, 32, 1)
re_x_test = x_test.values.reshape(-1, 32, 32, 1)

print(X.shape)
print(re_x_train.shape)
print(re_x_test.shape)
print(y_train.shape)
print(y_test.shape)

# Model architecture
model = Sequential()

model.add(Conv2D(32, (4,4), input_shape = (32, 32, 1), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(64, (3,3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dense(46, activation = 'softmax'))

model.summary()

# Compile the model
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

print(re_x_train.shape)
print(re_x_test.shape)
print(y_train.shape)
print(y_test.shape)

# Fit the model
history = model.fit(
    re_x_train,
    y_train,
    validation_split=0.2,
    epochs=2,
    batch_size=8,
    verbose=2,
)

# Evaluate the model
# model.evaluate(re_x_test, y_test, verbose=2)

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
