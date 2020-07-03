from flask_restful import Resource
from flask_restful import reqparse

import os

import json
import base64

from youtube_comments_crawler import youtube_crawler
from input_data_processor import input_processor
from morphs import making_word_cloud
from charts import making_charts
from pie_chart import making_pie_chart

from flask_cors import CORS, cross_origin
from time import sleep


def fileToBase64(filepath):
    fp = open(filepath, "rb")
    data = fp.read()
    fp.close()
    return base64.b64encode(data).decode('utf-8')

class Plus(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('url', required=True, type=str, help='url cannot be blank')
            args = parser.parse_args()

            url_input = args['url']

            if os.path.exists("./output/pie_chart.png"):
                os.remove("./output/pie_chart.png")
            if os.path.exists("./output/keywords.png"):
                os.remove("./output/keywords.png")
            if os.path.exists("./output/wordcloud.png"):
                os.remove("./output/wordcloud.png")
            if os.path.exists("./output/line.png"):
                os.remove("./output/line.png")

            youtube_crawler(url_input)
            sleep(1)
            input_processor()
            sleep(1)
            making_word_cloud()
            sleep(1)
            making_pie_chart()            
            sleep(1)
            making_charts()            

            wc = fileToBase64("./output/wordcloud.png")
            pie = fileToBase64("./output/pie_chart.png")
            histo = fileToBase64("./output/keywords.png")
            line = fileToBase64("./output/line.png")

            jstr = json.dumps({"wc": wc, "pie": pie, "histo": histo, "line": line})

            return jstr
        except Exception as e:
            return {'error': str(e)}

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
api.add_resource(Plus, '/plus')
CORS(app)

if __name__ == '__main__':
        app.run(host='server_ip', port=8000, debug=True)
