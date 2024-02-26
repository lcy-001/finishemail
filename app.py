from flask import Flask, request, jsonify
from utils import dataProcess
from flask_cors import CORS
from utils.logger import Logger
import pickle, json, sys
import pandas as pd
app = Flask(__name__)
CORS(app, supports_credentials=True)
with open("static/model/rfc.pickle", 'rb')as f:
    rfc = pickle.load(f)
    f.close()
per_data = pd.read_csv("static/data/features.csv")


@app.route('/', methods=["GET", "POST"])
def hello_world():  # put application's code here
    if request.method == "POST":
        data = json.loads(request.form.get('data'))
        process = dataProcess.Process(data, per_data)
        data = process.run()
        result = rfc.predict(data)[0]
        pro = rfc.predict_proba(data)[0]
        dict1 = {}
        dict1["email"] = pro[1]
        dict1["fishEmail"] = pro[0]
        if result == 1:
            print(result)
            dict1["res"] = "normal"
            return jsonify(dict1)
        else:
            print(result)
            dict1["res"] = "fishEmail"
            return jsonify(dict1)

    else:

        return "hello world"








if __name__ == '__main__':
    app.run()
    print(123)

