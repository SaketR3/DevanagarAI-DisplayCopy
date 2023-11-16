from keras.models import load_model
from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np


# label possible outcomes
devanagari_characters = [
    "character_01_ka", "character_02_kha", "character_03_ga", "character_04_gha", "character_05_kna",
    "character_06_cha", "character_07_chha", "character_08_ja", "character_09_jha", "character_10_yna",
    "character_11_taamatar", "character_12_thaa", "character_13_daa", "character_14_dhaa", "character_15_adna",
    "character_16_tabala", "character_17_tha", "character_18_da", "character_19_dha", "character_20_na",
    "character_21_pa", "character_22_pha", "character_23_ba", "character_24_bha", "character_25_ma",
    "character_26_yaw", "character_27_ra", "character_28_la", "character_29_waw", "character_30_motosaw",
    "character_31_petchiryakha", "character_32_patalosaw", "character_33_ha", "character_34_chhya",
    "character_35_tra", "character_36_gya", "digit_0", "digit_1", "digit_2", "digit_3",
    "digit_4", "digit_5", "digit_6", "digit_7", "digit_8", "digit_9"
]

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
        
        letter, acc = predict_letter(im)
        self.label.configure(text= "{} - {:.2f}%".format(devanagari_characters[letter], acc*100))

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
       
app = App()
mainloop()
