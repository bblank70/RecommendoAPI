
from flask import Flask,jsonify,request 
import pandas as pd
import json
from flask_cors import CORS


with open("./static/response.json", "r") as file:
    json_data = file.read()
data = json.loads(json_data)
results = data['result']
r = pd.DataFrame(results)
r = pd.read_csv("ContentRecommendations.csv")


print(r.head())


def ReturnJsonResultOuterKey(df, user):
    df = df[df['user'] == user]
    outer_key = "result"
    data = df.to_json(orient='records',double_precision=15)
    data = json.loads(data)
    data_with_outer_key = {outer_key: data}
    json_with_outer_key = json.dumps(data_with_outer_key, indent=4)
    return json_with_outer_key


app =   Flask(__name__) 
CORS(app)

@app.route('/')
def home():
	return "current endpoints are / and returnjson <h1>Welcome</h1>" 


@app.route('/returnjson', methods = ['GET']) 
def ReturnJSON(): 
    user = request.args.get('user')
    if(request.method == 'GET'): 
        return ReturnJsonResultOuterKey(r, user)