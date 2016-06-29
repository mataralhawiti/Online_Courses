import pymongo
import bottle
import sys



@bottle.get("/hw1/<n>")
def get_hw1(n):

	n = int(n)

	# connect to monogd server on standard port
	connection = pymongo.MongoClient("mongodb://localhost")

	# attach db
	db = connection.m101

	# collectioin
	collectioin = db.funnynumbers


	magic = 0

	try :
		iter = collectioin.find({}, limit=1, skip=n, ).sort('value', direction=1)
		# how it looks in mongo shell
		# db.funnynumbers.find().sort({"value":1}).skip(50).limit(1)
		
		for item in iter:
			return str(int(item['value'])) + '\n'
	except Exception as s:
		print ("Error trying to read collection:", type(s), s)


bottle.debug(True)
bottle.run(host='localhost', port=8080)