import json
from flask import Flask, request, make_response, Response, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.develop_database
api = Api(app)

class MyObject(Resource):

    def post(self):
      new_myobject = request.json
      myobject_collection = app.db.myobjects
      result = myobject_collection.insert_one(request.json)

      myobject = myobject_collection.find_one({"_id": ObjectId(result.inserted_id)})

      return myobject

    def get(self, myobject_id):
      myobject_collection = app.db.myobjects
      myobject = myobject_collection.find_one({"_id": ObjectId(myobject_id)})
      return myobject

api.add_resource(MyObject, '/myobject/','/myobject/<string:myobject_id>')

# provide a custom JSON serializer for flaks_restful
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    # Turn this on in debug mode to get detailled information about request related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)