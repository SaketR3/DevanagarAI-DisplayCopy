from flask import Flask, render_template, request, url_for
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        # Get the file from post request
        # Here we should handle the image data from the drawing pad
        # implement model's prefiction function here
        # here is a simulated prediction
        prediction = 'This is a simulated prediction: 9 with 99% confidence'

    # Render the HTML template index.html with the prediction 
    current_year = datetime.now().year  # Get the current year
    return render_template('index.html', prediction=prediction, current_year=current_year)

if __name__ == '__main__':
    app.run(debug=True)
