import sys
import csv


def csvToArray():
	datafile = open('out.csv', 'r')
	datareader = csv.reader(datafile,delimiter=';')
	data = []
	for row in datareader:
	    data.append(row) 
	return data;

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


def executeQ(querySet, master):
	rowID = -1;
	count = 0;
	for row in master:
		if row[0] == querySet[0]:
			rowID = count;
		count = count + 1;
	print rowID; 







query_sets = readConfig(sys.argv[1]);
outData = csvToArray();
executeQ(query_sets[0], outData);
# print(outData);
# print(query_sets);


