import pymongo

print(pymongo.version)

connection = pymongo.MongoClient()
db = connection.usa

res = db.cities.aggregate( [ {"$group" : {"_id" : {"state":"$state"}     , "population" : {"$sum":"$pop"} } } ] )

for i in res :
	print(i)
# res = db.cities.aggregate( [ {$group : {_id : {"state":"$state"}     , population : {$sum:"$pop"} } } ] )