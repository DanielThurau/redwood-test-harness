import sys
import csv


def csvToArray():
	datafile = open('out.csv', 'r')
	datareader = csv.reader(datafile,delimiter=',')
	data = []
	# no wanna hard code 
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


def executeQ(querySet, master, labels):
	rowID = -1;
	count = 0;
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
			print ("YOU FUCKED UP");
		else:
			print("IT WORKS")		



query_sets = readConfig(sys.argv[1]);
outData = csvToArray();

# Create a label system so i dont have to do this a billion 
# and one fucking times
indexMap = {}
count = 0;
for i in outData[0]:
	indexMap[i] = count;
	count = count + 1;



executeQ(query_sets[1], outData, indexMap);


