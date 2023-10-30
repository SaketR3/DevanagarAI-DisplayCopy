from tensorflow import keras

train_ds = keras.utils.image_dataset_from_directory(
    directory="Group16-FA23/archive/training_data",
    labels='inferred',
    label_mode='categorical',
    batch_size=32, # batch size, can be changed
    image_size=(32, 32))
validation_ds = keras.utils.image_dataset_from_directory(
    directory="Group16-FA23/archive/test_data/",
    labels='inferred',
    label_mode='categorical',
    batch_size=32, # batch size, can be changed
    image_size=(32, 32))

# model.fit(train_ds, epochs=10, validation_data=validation_ds)