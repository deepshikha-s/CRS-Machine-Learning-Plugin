from flask import Flask
from flask import request
import pickle
import sklearn
import psutil
import os
import random
import json
from helper import *

pid = os.getpid()
py = psutil.Process(pid)
memoryUse = py.memory_info().rss
print('RAM INIT: ', memoryUse)

##DEE Previously implemented model is proprietery and not available from previous author
##DEE stubbing the model for now and using a random generator for score calc
##DEE in due course, a ML model will be developed and plugged in here

##DEE pkl_filename = 'saved_models/iforest.pkl'
##DEE threshold = -0.313

app = Flask(__name__)

# Load the ML model in memory
##DEE with open(pkl_filename, 'rb') as file:
##DEE    ml_model = pickle.load(file)

@app.route('/', methods=['POST', 'GET'])

def query_ml():
    if request.method == 'POST':
        # Retrieve arguments from the request
        method = request.form['method']
        path = request.form['path']
        args = json.loads(request.form['args'])
        for k, v in args.items():
            args[k] = v.replace("$#$", '"')
        hour = int(request.form['hour'])
        day = int(request.form['day'])

        # Predict a score (1 for normal, -1 for attack)
        score = predict(method, path, args, hour, day)

        # Return the score to the Lua script
        if score > 3:
            return "Normal", 200
        return "Anormal", 401

    elif request.method == 'GET':
        # Simply return 200 on GET / for health checking
        return "Service is up", 200
    return "Bad Request", 400


def predict(method, path, args, hour, day):
    # Example of function to predict score using ML
    #features = get_features(method, path, args, hour, day)
    #print(features)

    ##DEE scores = ml_model.decision_function(features)
    ##DEE for now, stubing score compute
    score = random.randint(0,6)

    #print(scores[0])
    ##DEE labels = 1 - 2 * (scores < threshold).astype('int')

    ##DEE return labels[0]
    print(score)
    return score

if __name__ == '__main__':
    print("Entering main")
    app.run()
