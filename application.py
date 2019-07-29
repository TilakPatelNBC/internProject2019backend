from flask import Flask
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)



#get the last 5 CNBC videos posted:
#API KEY: AIzaSyDLgcYIKMiMVM2HM3liPbzrJyJTnVUq1oY
#   'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCvJJ_dzjViJCoLf5uKUTwoA&maxResults=5&order=date&key=AIzaSyDLgcYIKMiMVM2HM3liPbzrJyJTnVUq1oY' \

application = Flask(__name__)

@app.route('/videos')
def videos():
    request_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCvJJ_dzjViJCoLf5uKUTwoA&maxResults=50&order=date&key=AIzaSyDLgcYIKMiMVM2HM3liPbzrJyJTnVUq1oY'
    yt_response = requests.get(request_url).json()
    return yt_response

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

    data = '{"query":"{\\npage(path: \\"/us-top-news-and-analysis\\") {\\n    brand\\n    layout {\\n      columns {\\n        modules {\\n          data {\\n            ... on featuredBreaker {\\n              url\\n              type\\n              title: eyebrow\\n              sectionLabel\\n              shorterHeadline\\n              assets(count: 8, promoted: true) {\\n                id\\n                url\\n                datePublished\\n                title\\n                brand\\n                author {\\n                  name\\n                }\\n              }\\n            }\\n          }\\n        }\\n      }\\n    }\\n  }\\n}\\n"}'

    response = requests.post('https://qa-aws01webql.cnbc.com/graphql', headers=headers, data=data)
    return response.json()['data']['page']['layout'][9]['columns'][0]['modules'][0]['data']

