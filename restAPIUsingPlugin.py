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
''' Gets all of the data in the Library database collection '''
@app.route('/rpi1', method='GET')
def getAll(mongodb):
    print('getAll - rpi1')
    print("messge(s) = " + dumps(mongodb['rpi1'].count()))
    return dumps(mongodb['rpi1'].find().sort('time',1))

''' Gets all of the data in the database collection '''
@app.route('/rpi2', method='GET')
def getAll(mongodb):
    print('getAll - rpi2')
    print("messge(s) = " + dumps(mongodb['rpi2'].count()))
    return dumps(mongodb['rpi2'].find().sort('time',1))

''' Gets all of the data in the database collection '''
@app.route('/rpi3', method='GET')
def getAll(mongodb):
    print('getAll - rpi3')
    print("messge(s) = " + dumps(mongodb['rpi3'].count()))
    return dumps(mongodb['rpi3'].find().sort('time',1))

''' Gets a specific data in the database collection  using a name parameter'''
#ex. GET http://127.0.0.1:8000/search?name=Jinwoo
@app.route('/rpi1/search', method='GET')
def getName(mongodb):
    print('getName')
    if request.query.name != "":
        return dumps(mongodb['rpi1'].find({"name": {"$regex": request.query.name}}).sort('time',1))
    else:
        return "Please input your parameters!"
@app.route('/rpi2/search', method='GET')
def getName(mongodb):
    print('getName')
    if request.query.name != "":
        return dumps(mongodb['rpi2'].find({"name": {"$regex": request.query.name}}).sort('time',1))
    else:
        return "Please input your parameters!"
@app.route('/rpi3/search', method='GET')
def getName(mongodb):
    print('getName')
    if request.query.name != "":
        return dumps(mongodb['rpi3'].find({"name": {"$regex": request.query.name}}).sort('time',1))
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
@app.route('/rpi1/removeOne', method='GET')
def getName(mongodb):
    print('remove one')
    itemStr = dumps(mongodb['rpi1'].find().limit(1))
    jsonItem = json.loads(itemStr)
    item_id = jsonItem[0]['_id']['$oid']
    mongodb['rpi1'].delete_one({'_id': ObjectId(item_id)})   #remove one
    print("messge(s) = " + dumps(mongodb['rpi1'].count()))
    return dumps(mongodb['rpi1'].find().sort('time',1))

''' removes the oldest entry '''
#ex. GET http://127.0.0.1:8000/removeOne
@app.route('/rpi2/removeOne', method='GET')
def getName(mongodb):
    print('remove one')
    itemStr = dumps(mongodb['rpi2'].find().limit(1))
    jsonItem = json.loads(itemStr)
    item_id = jsonItem[0]['_id']['$oid']
    mongodb['rpi2'].delete_one({'_id': ObjectId(item_id)})   #remove one
    print("messge(s) = " + dumps(mongodb['rpi2'].count()))
    return dumps(mongodb['rpi2'].find().sort('time',1))

''' removes the oldest entry '''
#ex. GET http://127.0.0.1:8000/removeOne
@app.route('/rpi3/removeOne', method='GET')
def getName(mongodb):
    print('remove one')
    itemStr = dumps(mongodb['rpi3'].find().limit(1))
    jsonItem = json.loads(itemStr)
    item_id = jsonItem[0]['_id']['$oid']
    mongodb['rpi3'].delete_one({'_id': ObjectId(item_id)})   #remove one
    print("messge(s) = " + dumps(mongodb['rpi3'].count()))
    return dumps(mongodb['rpi3'].find().sort('time',1))

# POST REQUESTS
''' Posts one entry to the database collection, if full, remove the oldest entry '''
@app.route('/', method='POST')
def addOne(mongodb):
    print('addOne')
    strval = request.body.getvalue().decode("utf-8")
    jsonObj = json.loads(strval)
    new_msg = {'name': jsonObj['name'], 'token':jsonObj['token'], 'time': datetime.now(), "message": jsonObj['message']}
    numStr = dumps(mongodb[jsonObj['token']].count())
    num = int(numStr)
    if num >= 100:
        itemStr = dumps(mongodb[jsonObj['token']].find().limit(1))
        jsonItem = json.loads(itemStr)
        item_id = jsonItem[0]['_id']['$oid']
        mongodb[jsonObj['token']].delete_one({'_id': ObjectId(item_id)})
    mongodb[jsonObj['token']].insert_one(new_msg)
    print("messge(s) = " + dumps(mongodb[jsonObj['token']].count()))
    return dumps(mongodb[jsonObj['token']].find().sort('time',1))


# Listen to localhost:8080 (by default)
app.run(reLoader=True, debug=True, host='172.30.119.137', port='8000') #app.run(port=80, host='123.45.67.89')

