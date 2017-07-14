import sys
import csv


def csvToArray():
	datafile = open('a.csv', 'r')
	datareader = csv.reader(datafile,delimiter=';')
	data = []
	for row in data reader:
	    data.append(row) 


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


def executeQ(set):







query_sets = readConfig(sys.argv[1]);
print(query_sets);


