from flask import Flask
from flask import request
import pickle
import sklearn
import psutil
import os
import random
import json
from helper import *
import random

app = Flask("upload")

pid = os.getpid()
py = psutil.Process(pid)
memoryUse = py.memory_info().rss
print('RAM INIT: ', memoryUse)
pwd = os.getcwd()
print(pwd)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Previously implemented model is proprietery and not available from previous author
# stubbing the model for now and using a random generator for score calc
# in due course, a ML model will be developed and plugged in here

#to load the machine learning model
#pkl_filename = 'Desktop/CRS-Machine-Learning-Plugin/ml_model_server/saved_models/test.pkl'
threshold = -0.313

app = Flask(__name__)

# Load the ML model in memory
#with open(pkl_filename, 'rb') as file:
    #ml_model = pickle.load(file)

@app.route('/', methods=['POST', 'GET'])

def query_ml():
    pri("Inside")
    pri(request.form['method'])
    if request.method == 'POST':
        # Retrieve arguments from the request
        method = request.form['method']
        path = request.form['path']
        args = json.loads(request.form['args'])
        for k, v in args.items():
            args[k] = v.replace("$#$", '"')
        hour = int(request.form['hour'])
        day = int(request.form['day'])
        pri(method)
        pri(path)
        pri(args)
        upload()
        # Predict a score (1 for normal, -1 for attack)
        score = predict(method, path, args, hour, day)

        # Return the score to the Lua script
        if score > 0:
            return str(score), 200
        return str(score), 401

    elif request.method == 'GET':
        # Simply return 200 on GET / for health checking
        return "Service is up", 200
    return "Bad Request", 400

@app.route("/upload", methods=["POST"])
def upload():
    pri("File")
    files = request.files.getlist("file[]")
    pri(files)
    for file in files:
        if file.filename !='':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

def predict(method, path, args, hour, day):
    # Example of function to predict score using ML
    #features = get_features(method, path, args, hour, day)
    #print(features)

    #score = ml_model.decision_function()
    # for now, stubing score compute
    score = random.randint(-5, 5)
    #print(scores[0])
    #labels = 1 - 2 * (score < threshold).astype('int')

    # return labels[0]
    print(score)
    return score

def pri(s):
    print(s)

if __name__ == '__main__':
    app.run()
