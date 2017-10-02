import fnmatch
import os
from Upload import *

data_dir = "/home/leeps/redwood-test-harness/data/scenarios/"

os.system("rm -rf data/scenarios/*")

os.system("./features/steps/run.sh")

mydirs = []

for subdir, dirs, files in os.walk(data_dir):
	for diry in dirs:
		mydirs.append(os.path.join(subdir, diry) + "/")


for diry in mydirs:
	folder = "/" + os.path.basename(os.path.normpath(diry)) + "/"
	investLink = uploadToDropbox([diry + 'T1_investors.csv',], folder)
	jumpLink = uploadToDropbox([diry + 'T1_jump.csv'], folder)
	inputLinks = []
	for file in os.listdir(diry):
		if fnmatch.fnmatch(file, '*_input.csv'):
			inputLinks.append(uploadToDropbox([diry+file],folder))
	with open(diry + '.configRead', 'w') as f:
		for link in investLink:
			f.write("invest>" + link + "\n")
		for link in jumpLink:
			f.write("jump>" + link + "\n")
		count = 1;
		for link in inputLinks:
			f.write("input_" + str(count) + ">" + link[0] + "\n")
			count = count + 1
