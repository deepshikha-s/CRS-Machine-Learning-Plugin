#importing all necessary modules and libraries
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

# Previously implemented model is proprietery and not available from previous author
# stubbing the model for now and using a random generator for score calc
# in due course, a ML model will be developed and plugged in here

# pkl_filename = 'saved_models/iforest.pkl'
threshold = -0.313

app = Flask(__name__)

# Load the ML model in memory
# with open(pkl_filename, 'rb') as file:
#     ml_model = pickle.load(file)

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
        if score > 0:
            return str(score), 200
        return str(score), 401

    elif request.method == 'GET':
        # Simply return 200 on GET / for health checking
        return "Service is up", 200
    return "Bad Request", 400


def predict(method, path, args, hour, day):
    # Example of function to predict score using ML
    #features = get_features(method, path, args, hour, day)
    #print(features)

    # scores = ml_model.decision_function(features)
    # for now, stubing score compute
    score = random.randint(-5,5)

    #print(scores[0])
    labels = 1 - 2 * (score < threshold).astype('int')

    # return labels[0]
    print(score)
    return labels

if __name__ == '__main__':
    app.run()
