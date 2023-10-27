from keras.models import load_model
from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np

model = load_model('mnist.h5')

def predict_digit(img):
    # Resize image to 28x28 pixels
    img = img.resize((28, 28))
    # Convert rgb to grayscale
    img = img.convert('L')
    # Invert the grayscale image to match MNIST data representation
    img = Image.fromarray(255 - np.array(img))
    img_array = np.array(img)
    # Reshaping to support our model input and normalizing
    img_array = img_array.reshape(1, 28, 28, 1)
    img_array = img_array / 255.0
    # Predicting the class
    res = model.predict([img_array])[0]
    return np.argmax(res), max(res)

# Displaying the modified predict_digit function
predict_digit

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0
        
        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")
        self.label = tk.Label(self, text="Draw..", font=("Helvetica", 48))
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

        digit, acc = predict_digit(im)
        self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
       
app = App()
mainloop()
