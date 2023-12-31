import pickle5
from flask import Flask, app, request, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__,  template_folder='template')
#loading model
model = pickle5.load(open("regressmodel.pkl", 'rb'))
scalar = pickle5.load(open("scaling.pkl", 'rb'))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])

def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1, -1))
    result = model.predict(scalar.transform(np.array(list(data.values())).reshape(1, -1)))
    print(result[0])
    return jsonify(result[0])   

@app.route('/predict', methods=['POST'])
def predict():
    data =[float(x) for x in request.form.values()]
    print(scalar.transform(np.array(data).reshape(1, -1)))
    output = model.predict(scalar.transform(np.array(data).reshape(1, -1)))[0]
    return render_template("home.html",prediction_text = "Predicted Diabetes Progress- {}".format(output))

if __name__ == '__main__':
    app.run(debug=True)
