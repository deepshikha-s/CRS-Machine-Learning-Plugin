from flask import Flask
from flask import request
import pickle
import sklearn
import psutil
import os
#from helper_predict import *

pid = os.getpid()
py = psutil.Process(pid)
memoryUse = py.memory_info().rss
print('RAM INIT: ', memoryUse)

#pkl_filename = 'saved_models/iforest.pkl'
threshold = -0.313

app = Flask(__name__)

# Load the ML model in memory
#with open(pkl_filename, 'rb') as file:
#    ml_model = pickle.load(file)

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
            return "Normal", 200
        return "Anormal", 401
    elif request.method == 'GET':
        # Simply return 200 on GET / for health checking
        return "Service is up", 200
    return "Bad Request", 400



#code inside function works
def predict(method, path, args, hour, day):
    # Example of function to predict score using ML
    #features = get_features(method, path, args, hour, day)
    #print(features)
    #scores = ml_model.decision_function(features)
    #print(scores[0])
    #labels = 1 - 2 * (scores < threshold).astype('int')
    if hour > 12:
        scores = 23
    else:
        scores = -23
    return scores

if __name__ == '__main__':
    app.run()
