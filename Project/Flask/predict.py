from keras.models import load_model
import numpy as np

model = load_model('mnist.h5')

def predict_letter(img):
    # Resize image to 32x32 pixels
    img = img.resize((32, 32))
    # Convert rgb to grayscale
    img = img.convert('L')
    # Invert the grayscale image to match data representation
    img = Image.fromarray(255 - np.array(img))
    img_array = np.array(img)
    # Reshaping to support our model input and normalizing
    img_array = img_array.reshape(1, 32, 32, 1)
    img_array = img_array / 255.0
    # Predicting the class
    res = model.predict([img_array])[0]
    return np.argmax(res), max(res)