from flask import Flask, request, redirect, render_template
from bson.json_util import dumps
import requests
import os
import json
from pprint import pprint
from pymongo import MongoClient
from os.path import join, dirname
from dotenv import load_dotenv
client = MongoClient('localhost', 27017)
db = client['main']

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)



#get the last 5 CNBC videos posted:
#API KEY: AIzaSyDLgcYIKMiMVM2HM3liPbzrJyJTnVUq1oY
#   'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCvJJ_dzjViJCoLf5uKUTwoA&maxResults=5&order=date&key=AIzaSyDLgcYIKMiMVM2HM3liPbzrJyJTnVUq1oY' \

application = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(request.data)
    return render_template('404page.html')

@app.route('/videos') #requires results query arg
def videos():
    if 'results' in request.json:
        length = request.json.get('results')
        request_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCvJJ_dzjViJCoLf5uKUTwoA&maxResults=' + str(length) + '&order=date&key=AIzaSyDLgcYIKMiMVM2HM3liPbzrJyJTnVUq1oY'
        req = requests.get(request_url)
        yt_response = req.json
        yt_response['status'] = req.status_code
        return yt_response, req.status_code
    else:
        return {'message': 'Please supply the params'}, 400

@app.route('/latest-articles') #returns the latest articles filtered by the eyebrow
def articles():
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://qa-aws01webql.cnbc.com',
    }

    data = '{"query":"{\\npage(\\n path:\\"/us-top-news-and-analysis/\\") {\\n brand\\n layout {\\n   columns {\\n     span\\n     modules {\\n       data {\\n          ...on heroLedePlusThree {\\n  id\\n            datePublished\\n  assets {\\n    id\\n    description\\n    title\\n    headline\\n    shorterDescription\\n    url\\n    promoImage {\\n      url\\n    }\\n  }\\n}\\n       }\\n      \\n     }\\n   }\\n }\\n}\\n}"}'
    response = requests.post('https://qa-aws01webql.cnbc.com/graphql', headers=headers, data=data)
    data = response.json['data']['page']['layout'][3]['columns'][0]['modules'][0]
    return data, 200
    

@app.route('/create-user', methods = ['POST']) #creates a user and returns the information about the user
def create_user():
    if 'body' in request.json:
        return {'message': 'no body'}, 400
    name = 'invalid' if ('name' not in request.json) else request.json.get('name')
    email = 'invalid' if ('email' not in request.json) else request.json.get('email')
    age = -1 if ('age' not in request.json) else request.json.get('age')
    industry = 'invalid' if ('industry' not in request.json) else request.json.get('industry')
    interests = 'invalid' if ('interests' not in request.json) else request.json.get('interests')
    password = 'invalid' if ('password' not in request.json) else request.json.get('password')
    if name == "invalid" or email == "invalid" or age <= 8 or industry == "invalid" or interests == "invalid" or password == "invalid":
        return {'message': 'invalid parameters'}, 400
    users = db.Users
    user_id = users.insert_one({
        'name': name,
        'email': email,
        'age': age,
        'industry': industry,
        'interests': interests,
        'password': password,
        'history': []
    }).inserted_id
    jss = json.loads(dumps(users.find_one({"_id": user_id})))
    return jss, 200



# @app.route('/update-articles', methods = ['PUT'])
# def update_articles():
    

if __name__ == "__main__":
    app.run()