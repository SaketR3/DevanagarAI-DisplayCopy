from keras.models import load_model
from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np


# label possible outcomes
devanagari_characters = [
    "क", "ख", "ग", "घ", "ङ",
    "च", "छ", "ज", "झ", "ञ",
    "ट", "ठ", "ड", "ढ", "ण",
    "त", "थ", "द", "ध", "न",
    "प", "फ", "ब", "भ", "म",
    "य", "र", "ल", "व", "श",
    "ष", "स", "ह", "क्ष",
    "त्र", "त्त", "०", "१", "२", "३",
    "४", "५", "६", "७", "८", "९"
]

dict = {
  "क": "ka",
  "ख": "kha",
  "ग": "ga",
  "घ": "gha",
  "ङ": "kna",
  "च": "cha",
  "छ": "chha",
  "ज": "ja",
  "झ": "jha",
  "ञ": "yna",
  "ट": "taamatar",
  "ठ": "thaa",
  "ड": "daa",
  "ढ": "dhaa",
  "ण": "adna",
  "त": "tabala",
  "थ": "tha",
  "द": "da",
  "ध": "dha",
  "न": "na",
  "प": "pa",
  "फ": "pha",
  "ब": "ba",
  "भ": "bha",
  "म": "ma",
  "य": "yaw",
  "र": "ra",
  "ल": "la",
  "व": "waw",
  "श": "motosaw",
  "ष": "petchiryakha",
  "स": "patalosaw",
  "ह": "ha",
  "क्ष": "chhya",
  "त्र": "tra",
  "त्त": "gya",
  "०": "0",
  "१": "1",
  "२": "2",
  "३": "3",
  "४": "4",
  "५": "5",
  "६": "6",
  "७": "7",
  "८": "8",
  "९": "9",
}

# Load the model
model = load_model('aidan.h5')

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

# Displaying the modified predict_letter function
predict_letter

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0
        
        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")
        self.label = tk.Label(self, text="Draw a Devanagari character..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Recognise", command = self.classify_handwriting)   
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
       
        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        
        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        x0 = self.canvas.winfo_rootx() + 4
        y0 = self.canvas.winfo_rooty() + 4
        x1 = x0 + self.canvas.winfo_width() - 8
        y1 = y0 + self.canvas.winfo_height() - 8
        im = ImageGrab.grab((x0, y0, x1, y1))
        
        digit, acc = predict_letter(im)
        self.label.configure(text= "{} - {:.2f}%".format(devanagari_characters[digit] + ", " + dict.get(devanagari_characters[digit]), acc*100))

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
       
app = App()
mainloop()
