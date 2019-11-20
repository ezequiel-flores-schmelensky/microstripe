import json
import datetime
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo, ObjectId


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__,  template_folder='templates')
app.config.from_pyfile('Settings/env.py')
app.json_encoder = JSONEncoder
mongo = PyMongo(app)
CORS(app)


from Views import *


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=7000, debug=True)
