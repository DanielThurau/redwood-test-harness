import sys
import csv
import pandas as pd 
import numpy as np
from math import floor

pd.options.mode.chained_assignment = None 
# *** Deprecated but still here ***
# Return a 2d list of the csv
def csvToArray(infile):
	datafile = open(infile, 'r')
	datareader = csv.reader(datafile,delimiter=',')
	data = []
	# no wanna hard code 
	for row in datareader:
	    data.append(row) 
	return data;


# return a dictionary->list pandas 
# dataframe of the csv
def csvToNumpy(infile):
	return pd.read_csv(infile)


# *** Deprecated but still here ***
# Return a dictionary of labels 
def createInd(line):
	labels = [];
	
	for query in line.split(','):
		labels.append(query.strip())
	return labels;

# Reads config file and creates a 
# set of queries to be executed
def readConfig(file):
	query_sets = [];

	query_file = open(file, 'r');
	
	for line in query_file:
		if line[0] == "#":
			pass;
		else:
			query_sets.append(createInd(line));
	
	return query_sets;


def executeQ(query, master):
	rowID = -1;
	count = 0;
	status = True;
	
	# get the timestamp of the query
	num = query[0].strip().split(':');

	# retrieve the closest element to a given
	# value

	rowID = kClosestElement(int(num[1]), master)
	print(rowID)

	# for every tuple in the query
	for i in range(1,len(query)):
		
		# break the tuple apart
		check = query[i].split(':');
		# print(i)
		# print("Comparative: " + str(int(master[check[0]][rowID])) + " " + str(int(check[1])))
		
		if int(master[check[0]][rowID]) != int(check[1]):
			status = False; # if any are false update status

	return status;

# Return the value of the closest value to k
def kClosestElement(k, data):
	timestamps = data["timestamp"]
	

	# print(timestamps)
	print("want: " + str(k))


	index = 0
	low = 0
	high = len(timestamps) - 1

	# if timestamps[high] < k:
	# 	return high



	while True:
		# print("index: " + str(index))
		# print("low: " + str(timestamps[low]))
		# print("high: " + str(timestamps[high]))
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


query_sets = readConfig(sys.argv[1]) # retrieve queries

outData = csvToNumpy(sys.argv[2]); # retrieve csv

# print(outData)
timestamps = outData["timestamp"]

for i in range(0, len(timestamps)):
		timestamps[i] = timestamps[i].strip("[]").split(":")
		if len(timestamps[i]) > 1:
			timestamps[i] =  int(float((timestamps[i][2] + "." + timestamps[i][3])) * 1000000000)


outData["timestamp"] = timestamps

for item in query_sets: 
	if not executeQ(item, outData):
		print("Bad");
		exit(1);
print("Good")
exit(0);

