from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
import requests

app = Flask(__name__)
es = Elasticsearch()

@app.route("/")
def index():
    return  render_template("index.html")

# Returns paginated feed 
@app.route("/get_list/", methods=["GET"])
def get_list():
    # Get the parameters 
    start = int(request.args.get('start'))
    limit = int(request.args.get('limit'))
    # total size of result required from the es
    size  = (start+1)*limit

    query = '''
            {
            "query": {
                    "query_string": {
                    "default_field": "type",
                    "query": "tweet"
                    }
            },
            "sort": [
                    {
                    "retweet_count": {
                        "order": "desc"
                }
            }
                ],
            "size": %s,
            "_source": {
            "includes": ["url", "full_text"]
  }
    }''' %size

    result = es.search(index="twitter", body= query )
    result_list = result['hits']['hits']
    
    tweets = ""
    temp  = {}
    for i in range(start, start+ limit):
        temp["url"] = result_list[i]["_source"]['url']
        temp["url"] = temp["url"]  
        temp["full_text"] = result_list[i]["_source"]['full_text']
        embded = '''<li><blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">%s<a href="%s">%s</a></p>&mdash; The Screen Patti (@TheScreenPatti) <a href="%s">May 25, 2018</a></blockquote>
                <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script><br></li>'''%(temp["full_text"], temp["url"],temp["url"], temp["url"])
        tweets  = tweets + embded
    
    return tweets

if __name__ == "__main__":
    app.run(debug=True)