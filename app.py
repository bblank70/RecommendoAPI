
from flask import Flask,jsonify,request 
import pandas as pd
import json
from flask_cors import CORS


# with open("./static/response.json", "r") as file:
#     json_data = file.read()
# data = json.loads(json_data)
# results = data['result']
# r = pd.DataFrame(results)
# content = pd.read_csv("./static/Model_Content.csv")
# colab = pd.read_csv("./static/Model_Colab.csv")

popular = pd.read_csv("./static/Model_popular.csv")
new = pd.read_csv( "./static/Model_New.csv")
CC = pd.read_csv("./static/Model_CCrecs.csv")

stashedusers = list(set(CC.user.tolist()))

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
    if user not in stashedusers:
        print("This user is not in the data!, return popular recs")
        r = popular.sample(8)
        r['user'] = user
    else:
        r = CC[CC.user == user]
        model = list(set(r.Model))[0]
        print("This user is using:", model)
        if r.shape[0] < 8:
            print("This user needs more recommendations!")
            extrarecs = new.sample(8-r.shape[0])
            extrarecs['user'] = user
            print(extrarecs) #fill in extra recs from the new content
            r = pd.concat([r, extrarecs], axis=0)
            print(r)
        else:
            print("This user had too many reccomendations!")
            r =  r.sample(8)
    print(user)
    if(request.method == 'GET'): 
        return ReturnJsonResultOuterKey(r, user)