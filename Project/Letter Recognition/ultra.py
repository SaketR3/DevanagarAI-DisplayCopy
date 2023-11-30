# this is the overkill model. Do not run on your laptop it is too large of a model for your laptop to handle!

import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import confusion_matrix

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Activation
from keras.optimizers import Adam
from keras.callbacks import LearningRateScheduler, ReduceLROnPlateau, EarlyStopping
from keras.preprocessing.image import ImageDataGenerator
from keras.regularizers import l2
from keras.optimizers import legacy

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

# Create and initialize an early stopping function
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
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

model = Sequential()

l2_reg = 0.001  # L2 Regularization factor

# Define a function to create a new model
def create_model():
    model = Sequential()
    l2_reg = 0.001  # L2 Regularization factor
# Adding L2 regularization to Convolutional Layers and increasing Dropout layers
# Increasing depth and filters
    model.add(Conv2D(64, (3,3), padding='same', input_shape=(32, 32, 1), activation='relu', kernel_regularizer=l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(Conv2D(64, (3,3), padding='same', activation='relu', kernel_regularizer=l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.3))  # Increased dropout


    model.add(Conv2D(128, (3,3), padding='same', activation='relu', kernel_regularizer=l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(Conv2D(128, (3,3), padding='same', activation='relu', kernel_regularizer=l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.4))  # Increased dropout


    model.add(Conv2D(256, (3,3), padding='same', activation='relu', kernel_regularizer=l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(Conv2D(256, (3,3), padding='same', activation='relu', kernel_regularizer=l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.5))  # Increased dropout


    # Additional layers for complexity
    model.add(Conv2D(512, (3,3), padding='same', activation='relu', kernel_regularizer=l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(Conv2D(512, (3,3), padding='same', activation='relu', kernel_regularizer=l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.5))  # Increased dropout

    model.add(Flatten())
    model.add(Dense(1024, activation='relu', kernel_regularizer='l2'))
    model.add(Dropout(0.5))
    model.add(Dense(46, activation='softmax'))  # Assuming 46 classes for different characters

    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer=legacy.Adam(learning_rate=0.001), metrics=['accuracy'])
    return model

# # Training with data augmentation
# history = model.fit(
#     datagen.flow(re_x_train, y_train, batch_size=32),
#     validation_data=(re_x_test, y_test),
#     epochs=200,  # Increased epochs
#     verbose=2,
#     callbacks=[lr_scheduler, lr_plateau_callback, early_stopping]
# )

# K-fold Cross-Validation
num_folds = 5
kf = KFold(n_splits=num_folds, shuffle=True, random_state=42)

fold_no = 1
for train_index, val_index in kf.split(re_x_train):
    print('Training on fold ' + str(fold_no) + '/' + str(num_folds) + '...')

    # Splitting data
    train_data, val_data = re_x_train[train_index], re_x_train[val_index]
    train_labels, val_labels = y_train[train_index], y_train[val_index]

    # Create a new model instance for each fold
    fold_model = create_model()

    # Train the model
    fold_history = fold_model.fit(
        datagen.flow(train_data, train_labels, batch_size=32),
        validation_data=(val_data, val_labels),
        epochs=200,
        verbose=2,
        callbacks=[lr_scheduler, lr_plateau_callback, early_stopping]
    )

    fold_history_df = pd.DataFrame(fold_history.history)
    fold_history_df.loc[:, ['loss', 'val_loss', 'accuracy', 'val_accuracy']].plot(title="Fold " + str(fold_no))
    plt.show()

    # Increase fold number
    fold_no += 1

    # Evaluate the model on test set for each fold
    scores = fold_model.evaluate(re_x_test, y_test, verbose=2)
    print("Fold {} - Test loss: {}, Test accuracy: {}".format(fold_no, scores[0], scores[1]))

    # Save model checkpoints
    fold_model.save('model_fold_{}.h5'.format(fold_no))

print(re_x_train.shape)
print(re_x_test.shape)
print(y_train.shape)
print(y_test.shape)

# Evaluate the model
scores = model.evaluate(re_x_test, y_test, verbose=2)
print("Test loss:", scores[0])
print("Test accuracy:", scores[1])

# Save the last fold model (Optional)
fold_model.save('aidan_last_fold.h5')
print("Saving the last fold model as aidan_last_fold.h5")

# Plot the accuracy and loss
history_df = pd.DataFrame(fold_history.history)
history_df.loc[:, ['loss', 'val_loss', 'accuracy', 'val_accuracy']].plot()


# Plot the confusion matrix
X_images = X.values.reshape((-1,32,32))

plt.imshow(X_images[555])
plt.show()

imgTrans = X_images[555].reshape(1,32,32,1)
predictions = model.predict(imgTrans)
binencoder.classes_[np.argmax(predictions)]

y_pred = model.predict(re_x_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d')
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

