import pymongo
import os


co = pymongo.MongoClient("mongodb://localhost")
db = co.school
cl = db.students

def inseOne() :
	andr = {"name":"Ahmed", "job":"dev", "hob":["soccor", "swim", "tenss"]}

	try :
		cl.insert_one(andr)
	except Exception as e :
		print("unexpected error", type(e), e)


def findOne() :
	q = cl.find_one({"name":"Ahmed"}, {"name":1, "_id":0})
	print(q)

# cursor !!
def find() :
	cursor = cl.find({"name":"Ahmed"}, {"name":1})
	return cursor


# cursor !!
def find1() :
	cursor = cl.find({})
	return cursor



#inseOne()
#findOne()

# for doc in find() :
# 	print(doc)


for doc in find1() :
	print(doc)
