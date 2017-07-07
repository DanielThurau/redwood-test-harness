from os import walk
import os
import fnmatch



def makeConfig(mypath):
	file = mypath+'/Config.csv' 
	target = open(file, 'w')
	target.write("period,subject,groups,startingWealth,speedCost,maxSpread,marketEventsURL,priceChangesURL,input_addresses\n")
	target.write("1,default,[[1,2,3,4]],140,0.01,4,")
	for file in os.listdir(mypath):
		if fnmatch.fnmatch(file, '*investors*'):
			target.write(mypath + '/' + file + ',')
	for file in os.listdir(mypath):
		if fnmatch.fnmatch(file, '*jump*'):
			target.write(mypath + '/' + file + ',')
	files= []
	for (dirpath, dirnames, filenames) in walk(mypath):
	    files.extend(filenames)
	files.sort()
	for file in files:
		if fnmatch.fnmatch(file, '*input*'):
			target.write(mypath + '/' + file + ',')





f = []
mypath = os.path.dirname(os.path.realpath(__file__))
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(dirnames)


for i in f:
	makeConfig(mypath + "/" + i)
    
