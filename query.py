import sys

query_sets = [];


def createInd(line):
	temp = [];
	for query in line.split(','):
		temp.append(query.strip())
	return temp;




query_file = open(sys.argv[1], 'r');
for line in query_file:
	if line[0] == "#":
		pass;
	else:
		query_sets.append(createInd(line));
		

print query_sets;
