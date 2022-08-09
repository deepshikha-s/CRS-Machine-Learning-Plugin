from flask import Flask
from flask import request
import pickle
import sklearn
import psutil
import os
import random
import json
from helper import *
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
pid = os.getpid()
py = psutil.Process(pid)
memoryUse = py.memory_info().rss
print('RAM INIT: ', memoryUse)
UPLOAD_FOLDER = '/var/www/html/uploads'
'''
DIRECTIVE!!!
Add the path where you have saved your machine learning model and uncomment the next line
'''
# pkl_filename = 'saved_models/iforest.pkl'
threshold = -0.313

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 10485760

# Load the ML model in memory
'''
DIRECTIVE!!!
Uncomment the following 2 lines to load the file to the server.
'''
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
        print(method)
        print(path)
        print(args)
        print(hour, day)
        process_json()
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

@app.route("/uploader", methods=["POST"])
def upload():
    if request.method == 'POST':
      f = request.files['file']
      print('app_root:', app.root_path, 'file to upload: ', f.filename)
      f.save(os.path.join(app.root_path, 'uploads', secure_filename(f.filename)))
      return 'file uploaded successfully'

def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print(content_type)
        return json
    else:
        print(content_type)
        return 'Content-Type not supported!'


def predict(method, path, args, hour, day):
    # Example of function to predict score using ML
    '''
    DIRECTIVE!!!
    Uncomment the following lines to complete the machine learning plugin.
    Comment the line which generates a random score to stub the score in the absence of a machine learing model.
    '''
    #features = get_features(method, path, args, hour, day)
    #print(features)
    # scores = ml_model.decision_function(features)
    # for now, stubing score for completeness.
    score = random.randint(-5,5)
    #print(scores[0])
    labels = 1 - 2 * int(score < threshold)
    # return labels[0]
    print(score)
    return labels

if __name__ == '__main__':
    app.run()
