#!/usr/bin/python
from datetime import datetime
import bottle
from bottle import Bottle, request, response
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps
from bson import json_util
from bson.objectid import ObjectId
#from http.server import HTTPServer, SimpleHTTPRequestHandler
#import bson
import json
import sys
'''
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin']= '*'
        response.headers['Access-Control-Allow-Methods']= 'GET,POST,PUT,OPTIONS'
        response.headers['Access-Control-Allow-Headers']= 'Origin, Accept, Content-Type,X-Requested-Width, X-CSRF-Token'

        if bottle.request.method !=  'OPTIONS':
            print("inside options")
            return fn(*args, **kwargs)
    return _enable_cors
'''


app = Bottle()
database_name = 'memo_in_api'
db_uri = 'mongodb://theFrontSeaters:netAppsClass2017@ds030719.mlab.com:30719/memo_in_api'
db_plugin = MongoPlugin(uri=db_uri, db=database_name)
app.install(db_plugin)


@app.hook('after_request')
def enable_cors_new():
    response.headers['Access-Control-Allow-Origin']= '*'
    response.headers['Access-Control-Allow-Methods']= 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers']= 'Origin, Accept, Content-Type,X-Requested-Width, X-CSRF-Token'

# GET REQUESTS
#ex. GET http://127.0.0.1:8000/
''' Gets all of the data in the database collection '''
@app.route('/', method='GET')
#@enable_cors
#def example():
#    print return_mongo
#    return 'hello'
def getAll(mongodb):
    print('getAll')
    print("messge(s) = " + dumps(mongodb['Library'].count()))
    return dumps(mongodb['Library'].find())

''' Gets a specific data in the database collection  using a name parameter'''
#ex. GET http://127.0.0.1:8000/search?name=Jinwoo
@app.route('/search', method='GET')
def getName(mongodb):
    print('getName')
    if request.query.name != "":
        return dumps(mongodb['Library'].find({"name": {"$regex": request.query.name}}))
    else:
        return "Please input your parameters!"

''' Gets number of items in the collection '''
#ex. GET http://127.0.0.1:8000/search?name=Jinwoo
@app.route('/count', method='GET')
def getName(mongodb):
    print('getCount')
    numStr = dumps(mongodb['Library'].count())
    print("messge(s) = " + numStr)
    return "messge(s) = " + numStr

''' removes the oldest entry '''
#ex. GET http://127.0.0.1:8000/removeOne
@app.route('/removeOne', method='GET')
def getName(mongodb):
    print('remove one')
    itemStr = dumps(mongodb['Library'].find().limit(1))
    jsonItem = json.loads(itemStr)
    item_id = jsonItem[0]['_id']['$oid']
    mongodb['Library'].delete_one({'_id': ObjectId(item_id)})   #remove one
    print("messge(s) = " + dumps(mongodb['Library'].count()))
    return dumps(mongodb['Library'].find())

# POST REQUESTS
''' Posts one entry to the database collection, if full, remove the oldest entry '''
#ex. POST http://127.0.0.1:8000/

#@app.route('/', method='POST')
@app.post('/')
def addOne(mongodb):
    #response.headers['Content-Type'] = 'application/json'
    print('addOne')
    print(request.json)
    #print(response.json.get('name'))
    new_msg = {'name': request.json.get('name'), 'time': datetime.now(), "message": request.json.get('message')}
    numStr = dumps(mongodb['Library'].count())
    num = int(numStr)
    if num >= 100:
        itemStr = dumps(mongodb['Library'].find().limit(1))
        jsonItem = json.loads(itemStr)
        item_id = jsonItem[0]['_id']['$oid']
        mongodb['Library'].delete_one({'_id': ObjectId(item_id)})
    mongodb['Library'].insert_one(new_msg)
    print("messge(s) = " + dumps(mongodb['Library'].count()))
    return dumps(mongodb['Library'].find())
# Listen to localhost:8080 (by default)


app.run(reLoader=True, debug=True, host='172.31.85.253', port='8000') #app.run(port=80, host='123.45.67.89')

