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
# Previously implemented model is proprietery and not available from previous author
# stubbing the model for now and using a random generator for score calc
# in due course, a ML model will be developed and plugged in here

# pkl_filename = 'saved_models/iforest.pkl'
threshold = -0.313

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 10485760
@app.route('/', methods=['POST', 'GET'])
def process_content():
    content_type = request.headers.get('Content-Type')
    print("Entered process_content")
    print(content_type)
    print(request.form)
    #files = request.form['files']
    #method = request.form['method']
    #path = request.form['path']
    #hour = int(request.form['hour'])
    #day = int(request.form['day'])
    #print(method)
    #print(path)
    #print(hour, day)
    if (content_type == 'application/json'):
        json = request.json
        print(content_type)
        return json
    if (content_type == 'application/x-www-form-urlencoded'):
        s = query_ml()
        return s
    if (str(content_type)[0:19] == 'multipart/form-data'):
        s = upload()
        return s
    else:
        #print("Content-Type not supported!")
        print(content_type)
        return 'Content-Type not supported!'
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
        files = request.form['files']
        for k, v in args.items():
            args[k] = v.replace("$#$", '"')
        hour = int(request.form['hour'])
        day = int(request.form['day'])
        print(path)
        print(args)
        print(hour, day)
        print(files)
        #if files != {}:
            #s = upload()
            #return s
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
    print("Entered upload")
    if request.method == 'POST':
      f = request.files['file']
      print('app_root:', app.root_path, 'file to upload: ', f.filename)
      f.save(os.path.join(app.root_path, 'uploads', secure_filename(f.filename)))
      return 'file uploaded successfully'

def predict(method, path, args, hour, day):
    # Example of function to predict score using ML
    #features = get_features(method, path, args, hour, day)
    #print(features)

    # scores = ml_model.decision_function(features)
    # for now, stubing score compute
    score = random.randint(-5,5)

    #print(scores[0])
    #labels = 1 - 2 * (score < threshold).astype('int')
    labels = 1 - 2 * int(score < threshold)
    # return labels[0]
    print(score)
    return labels

if __name__ == '__main__':
    app.run()
