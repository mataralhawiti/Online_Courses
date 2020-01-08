import pymongo
import sys

# connection
#mongodb://localhost
connection = pymongo.MongoClient()

# db handler
db = connection.pic

# collection handler
imgC = db.images
albC = db.albums


findImg = imgC.find({},{"_id":1})
findAlb = albC.find()

imgArr = []
albArr = []
toBeDeleted = []

albAgg = albC.aggregate([ {"$project": {"_id": 0, "images":1}}, {"$unwind" : "$images"} , {"$group" : {"_id":"$images"}} ])
#db.albums.aggregate([ {"$project": {"_id": 0, "images":1}}, {"$unwind" : "$images"} , {"$group" : {"_id":"$images"}} ])


print(type(albAgg))



for i in findImg :
	imgArr.append(i.get("_id"))

for i in albAgg :
	albArr.append(i.get("_id"))


for img in imgArr :
	if img not in albArr :
		toBeDeleted.append(img)


for img in toBeDeleted :
	imgC.delete_one({"_id":img})

print(len(albArr))
print(len(imgArr))
print(toBeDeleted)
#print(len(toBeDeleted))


