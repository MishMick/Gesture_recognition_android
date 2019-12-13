from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import time
import ml
import vidproc
from sklearn.preprocessing import StandardScaler
import flask
import json as Json

app = Flask(__name__)
data, target = ml.load_data()
scaler = StandardScaler()
scaler.fit(data)
data = scaler.transform(data)
models = ml.make_models(data, target)

@app.route('/upload', methods=['POST'])
def upload():
    for name in request.files:
        if not os.path.exists(name):
            os.makedirs(name)
        f = request.files[name]
        f.save(name + "/" + secure_filename(f.filename))
    return "mp4 saved"

@app.route('/', methods=['GET'])
def hello():
    return "hello3"

@app.route('/json', methods=['POST'])
def json():
    folder = "json"
    content = request.get_json()
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = folder + "/keypoints.json"
    with open(path,'w') as f:
    	Json.dump(content,f)

    #print("helooooooooooo")
    #print(content)
    #content.save(path)
    '''
    for name in request.files:
        if not os.path.exists(folder):
            os.makedirs(folder)
        f = request.files[name]
        path = folder + "/keypoints.json"
        f.save(path)
    '''
    #return "response" 
    return ml.query_models(models, scaler, folder)

@app.route('/classify', methods=['POST'])
def classify():
    for name in request.files:
        folder = "classify"
        if not os.path.exists(folder):
            os.makedirs(folder)

        f = request.files[name]
        #fn = secure_filename(f.filename) + str(time.time())
        fn1 = name + "_" + str(int(time.time()))
        fn = fn1 + ".mp4"
        f.save(folder + "/" + fn)
        vidproc.extract_df(folder + "/", fn)
        return ml.query_models(models, scaler, folder + "/" + fn1)

if __name__ == '__main__':
    #os.system("npm install")
    app.run(host='0.0.0.0', port=5000)
