#!/usr/bin/env python3
from pymongo import MongoClient
import csv

client = MongoClient('mongodb://localhost:27017/')
r_collection = client.Restaurantdb.restaurant

# remove previous restaurants
r_collection.remove()

with open('data/db.csv') as file:
	csv_reader = csv.reader(file, delimiter = ',')
	
	for row in csv_reader:
		dictionary = {}
		dictionary['name'] = row[0]
		dictionary['cuisine'] = row[1]
		dictionary['city'] = row[2]
		dictionary['location'] = row[3]
		dictionary['price'] = row[4]

		r_collection.insert_one(dictionary)

print("%d restaurants inserted" % r_collection.count())