import sys
import csv
import pandas as pd 
import numpy as np
from math import floor


def csvToArray():
	datafile = open('out.csv', 'r')
	datareader = csv.reader(datafile,delimiter=',')
	data = []
	# no wanna hard code 
	for row in datareader:
	    data.append(row) 
	return data;

def csvToNumpy():
	data = pd.read_csv('out.csv')
	return data

def createInd(line):
	temp = [];
	for query in line.split(','):
		temp.append(query.strip())
	return temp;


def readConfig(file):
	query_sets = [];
	query_file = open(file, 'r');
	for line in query_file:
		if line[0] == "#":
			pass;
		else:
			query_sets.append(createInd(line));
	return query_sets;


def executeQ(querySet, master, labels):
	rowID = -1;
	count = 0;
	goodQuery = True;
	num = querySet[0].strip().split(':');
	for row in master:
		if row[0] == num[1]:
			rowID = count;
		count = count + 1;
	# print rowID
	for i in range(1,len(querySet)):
		check = querySet[i].split(':');
		index = labels[check[0]];
		if master[rowID][index] != check[1]:
			goodQuery = False;
	return goodQuery;

def kClosestElement(k, data):
	timestamps = data["timestamp"]

	# print(timestamps)

	index = 0
	low = 0
	high = len(timestamps) - 1
	while True:
		if high == low:
			return high
		elif high - low == 1:
			higher = abs(timestamps[high] - k)
			lower = abs(timestamps[low] - k)
			if higher > lower:
				return low
			else:
				return high
		index = low + int(floor((high - low) / 2))
		if timestamps[index] == k:
			return index
		elif timestamps[index] > k:
			high = index
		else:
			low = index


query_sets = readConfig(sys.argv[1]);
# outData = csvToArray();
outData = csvToNumpy()
closestIndex = kClosestElement(6410000001, outData)

print("closest k index: " + str(closestIndex) + " value: " + str(outData['timestamp'][closestIndex]))

# Create a label system so i dont have to do this a billion 
# and one fucking times
# indexMap = {}
# count = 0;
# for i in outData[0]:
# 	indexMap[i] = count;
# 	count = count + 1;


# for item in query_sets:
# 	if not executeQ(item, outData, indexMap):
# 		print("Bad");
# 		exit(1);
# print("Good")
# exit(0);

