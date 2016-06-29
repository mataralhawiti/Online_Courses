# find_one
'''
import pymongo
import sys


# establish a connection to MongoD server
connection = pymongo.MongoClient("mongodb://localhost")
				#pymongo.Connection("mongodb://localhost", safe=True)    >>> Deprecated
# get a handle to DB
db = connection.test


# get a collection
sample = db.sample


def findOne():
	print("Find a person")

	# create dict to hold our query !!!
	query = {'name':"Jessica Booth"}

	try:
		person = sample.find_one(query)

	except:
		print("unexpected error", sys.exe_info()[0])

	print(person)

def find():
	print("Find all persons")

	# create dict to hold our query !!!
	query = {'eyeColor':'brown'}

	try:
		cursor = sample.find(query)

	except:
		print("unexpected error", sys.exe_info()[0])


	sanity = 0

	for doc in cursor:
		print(doc)
		sanity += 1

		if(sanity>10):
			break

	#print(sanity)



def findField():
	print("find a field in a person collection")

	#create dict to holder our query
	query = {'eyeColor':'brown'}

	# another dict for our selector (projection)
	# the field that we want to retrive
	selector = {'name':1, '_id':0} # we specify _id:0 cuz _id is return by default !!


	try:
		itr = sample.find(query, selector)

	except:
		print("unexpected error", sys.exe_info()[0])

	sanity = 0


	for doc in itr:
		print(doc)
		sanity += 1
		if(sanity>10):
			break
			# cursor = students.find({}, {'student_id':1, '_id':0})
			# what's this ?


# using $gt & $lt
def find_gt_lt():
	print("I'm using $gt & $lt operators :)")

	#create dict to hold our query, notice '' around $gt and $lt:
	query = {'eyeColor':'brown', 'age':{'$gt':20, '$lt':30}} 


	# No need for selector here cuz it's embeded in our quey !

	try:
		itr = sample.find(query)

	except:
		print("unexpected error", sys.exe_info()[0])


	sanity = 0
	for doc in itr:
		print(doc)
		sanity += 1
		if(sanity>10):
			break

#findOne()
#find()
#findField()
#find_gt_lt()

'''

#------------------------------------------------------------------------------------------------


# import from Reddit
# curl  http://www.reddit.com/r/technology/.json > reddit.json

'''
json.laod vs json.loads
limit-req error
json types vs python types
loop through dict
'''

'''
import requests
import pymongo
import sys
import json
import urllib3

# connect to MongoD
connection = pymongo.MongoClient("mongodb://localhost")


# get a handler to db (new db)
db = connection.reddit

# get a handler to collection (new collection)
collection = db.stories

# get the target page from Reddit
r = requests.get("http://www.reddit.com/r/technology/.json")


# parse json into Python object
parsed = json.loads(r.text) # type : dict


#print(parsed)
# iter throu every news page
for item in parsed['data']['children']:
	#put into mongodb
	collection.insert(item['data'])
'''

#--------------------------------------------------------------------------------------------

'''
#using $regex 
#--- shell :
#db.stories.find({'title':{$regex:'Obama'}}, {'title':1,'_id':0})


#--- pymongo :
import pymongo
import sys

# estiablesh a connection to mongoD
connection = pymongo.MongoClient("mongodb://localhost")

# get a handler to db
db = connection.reddit

# get a handler for the collection
collection = db.stories

# find doc has Obama in their titles
def use_regex():
	print("we're using regex ")

	query = {'title':{'$regex' : 'Obama'}} # DON NOT FORGET '' around $ operator !!!
	projection = {'title':1, '_id':0} # eleminating unwanted fields !

	try:
		itr = collection.find(query, projection)
		
	except:
		print("unexpected error", sys.exc_info()[0])


	# iter through the retrieved docs :
	for doc in itr:
		print(doc)


use_regex()

'''



#--------------------------------------------------------------------------------------------
'''
# using DOT NOTATION

import pymongo
import sys

# estiablesh a connection to mongoD
connection = pymongo.MongoClient("mongodb://localhost")

# get a handler to db
db = connection.reddit

# get a handler for the collection
collection = db.travel

# find embded fields
def use_dot_notation():
	query = {'media.oembed.thumbnail_url':{'$regex' : '.jpg'}} # DON NOT FORGET '' around $ operator !!!
	projection = {'media.oembed.thumbnail_url':1, '_id':0} # eleminating unwanted fields !

	try:
		itr = collection.find(query, projection)
		
	except:
		print("unexpected error", sys.exc_info()[0])


	# iter through the retrieved docs, only retrive urls :)
	for doc in itr:
		for key in doc:
			for a in doc[key] :
				for b in doc[key][a] :
					print(doc[key][a][b])



use_dot_notation()

'''

#-------------------------------------------------------------------------------------------------

#created_utc
# using sort, skip, limit
'''
import pymongo
import sys

# estiablesh a connection to mongoD
connection = pymongo.MongoClient("mongodb://localhost")

# get a handler to db
db = connection.reddit

# get a handler for the collection
collection = db.travel

# find embded fields
def sort_limit_skip():
	query = {}

	try:
		cursor = collection.find(query).sort('created_utc', pymongo.ASCENDING).skip(5).limit(3)
		
		#cursor = collection.find(query).sort([('created_utc', pymongo.ASCENDING), ('score', pymongo.DESCENDING)]).skip(5).limit(3)
		# took Tuple !!!!
	except:
		print("unexpected error", sys.exc_info()[0])


	# iter through the retrieved docs, only retrive urls :)
	for doc in cursor:
		print(doc)



sort_limit_skip()
'''


#-------------------------------------------------------------------------------------------------
'''
#created_utc
# using sort, skip, limit
import pymongo
import sys

# estiablesh a connection to mongoD
connection = pymongo.MongoClient("mongodb://localhost")

# get a handler to db
db = connection.test

# get a handler for the collection
collection = db.person

# find embded fields
def insert_m():
	print("insert pymongo")

	richard = {'name':'Richard', 'company':'10g', 'interests':['swimming', 'football', 'running']}
	saleh = {'_id':15, 'name':'Matar', 'company':'Google', 'interests':['singing']}


	try:
		collection.insert(richard)
		collection.insert(saleh)
	except:
		print("unexpected error", sys.exc_info()[0])


	# iter through the retrieved docs, only retrive urls :)
	print(richard)
	print(saleh)



insert_m()

'''

'''
#-------------------------------------------------------------------------------------------------

# update
import pymongo
import sys

# estiablesh a connection to mongoD
connection = pymongo.MongoClient("mongodb://localhost")

# get a handler to db
db = connection.test

# get a handler for the collection
collection = db.person

# find embded fields
def update_save():
	print("update using save")
	try:
		# get doc
		per = collection.find_one({'_id':15})
		print(per)
		#add something
		per['nationality'] = 'USA'

		#update with conivent method
		collection.save(per)

		#get doc, after
		per = collection.find_one({'_id':15})
		print(per)
	except:
		print("unexpected error", sys.exc_info()[0])

# using wholesale replacement of doc
def update_tradi():
	print("update using save")
	try:
		# get doc
		per = collection.find_one({'_id':15})
		print(per)
		#add something
		per['nationality'] = 'USA'

		#update with update method
		# note 
		collection.update({'_id':15}, per)

		#get doc, after
		per = collection.find_one({'_id':15})
		print(per)
	except:
		print("unexpected error", sys.exc_info()[0])

# using wholesale replacement of doc
def update_set():
	print("update using save")
	try:
		# get doc
		per = collection.find_one({'_id':15})
		print(per)

		#add something
		per['nationality'] = 'USA'

		#update with $set operator 
		collection.update({'_id':15},{$set:{'nationality':'ENG'}})

		#get doc, after
		per = collection.find_one({'_id':15})
		print(per)
	except:
		print("unexpected error", sys.exc_info()[0])

# remove the new filed, Nationality - undo update
def remove_nationality():
	print("remove update")
	try:
		#update with $set operator 
		collection.update({},{$unset:{'nationality':1}}, multi=True)

		#get doc, after
		per = collection.find_one({'_id':15})
		print(per)
	except:
		print("unexpected error", sys.exc_info()[0])



# remove the new filed, Nationality - undo update
def using_upsert():
	print("remove update")
	try:
		#update with $set operator 
		collection.update({'_id':15},{$set:{'nationality':'ENG'}}, upsert=True)

		
			things.update({'thing':'apple'}, {$set:{'color':'red'}}, upsert=True)
			things.update({'thing':'pear'}, {'color':'red'}, upsert=True) # notice : no $set operator !!

			apple = collection.find_one({'thing':'apple'})
			pear = collection.find_one({'thing':'pear'})
			print(apple)
			print(pear)
		
		#get doc, after
		per = collection.find_one({'_id':15})
		print(per)

	except:
		print("unexpected error", sys.exc_info()[0])


update_save()
update_tradi()
update_set()
using_upsert()
remove_nationality()

'''

#-------------------------------------------------------------------------------------------------

# find_and_modify()
# sequence of numbers 

#import pymongo

#def get_next_sequence_number(name):

	#get a handler to the server
#	connection = pymongo.MongoClient("mongodb://localhost")

	# get handler to db
#	db = connection.test

	# get handler to collection
#	counters = db.counter


	# let's create seq numbers :
	# note : counter is Dict @@@@@
#	counter = counters.find_and_modify(	query={'type':name},
#										update={'$inc':{'value':1}},
#										upsert=True,
#										new=True)

	# retrive return value in dict(python), doc/obj(mongoDB)
#	counter_value = counter['value']

#	return counter_value
# call
#print(get_next_sequence_number('uid'))
#print(get_next_sequence_number('uid'))


######################################3

# copy a collection :
# db.grades.copyTo('grad')  -- notice ''






##########################
import pymongo

def get():

	#get a handler to the server
	connection = pymongo.MongoClient("mongodb://localhost")

	# get handler to db
	db = connection.blog

	# get handler to collection
	userss = db.users
	username = 'aaa'
	password = 'fe1c84aa8c9adc8f57e6bfdd95790a9b59bf8ee3a1dec34aea751acb2de87f26,GcxRO'

	user = userss.find_one({'_id':'username'})


	for u in user:
		print(u)

