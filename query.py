import sys
import csv
import pandas as pd 
import numpy as np
from math import floor


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

	# for every tuple in the query
	for i in range(1,len(query)):
		
		# break the tuple apart
		check = query[i].split(':');

		if int(master[check[0]][rowID]) != int(check[1]):
			status = False; # if any are false update status
	return status;

# Return the value of the closest value to k
def kClosestElement(k, data):
	timestamps = data["timestamp"]

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


query_sets = readConfig(sys.argv[1]) # retrieve queries

outData = csvToNumpy(sys.argv[2]); # retrieve csv


for item in query_sets: 
	if not executeQ(item, outData):
		print("Bad");
		exit(1);
print("Good")
exit(0);

