#!/usr/bin/python
import os
import sys
import shutil


TOPDIR = os.path.dirname(os.path.realpath(__file__)) + "/"
MANIFEST = TOPDIR + "data/manifests/CDA_Manifest.json"
TYPE = "HFT-CDA"

# Driver Phase 1 :
#	Copy Specified Gherkin text to Gherkin Module
try:
	shutil.copyfile(sys.argv[1], "./features/gherkin.feature")
except ParseError:
	pass
# Driver Phase 2 : 
# 	Run steps.py in the Behave Gherkin-behave module
osStatement = "python behave_driver.py"
os.system(osStatement); 
os.remove(TOPDIR + "features/gherkin.feature")

# Driver Phase 3 :
#	run python script on Scenarios dir
osStatement = "python createConfig.py"
os.system(osStatement);


# Driver Phase 4:
#       trigger selenium
scenarios = next(os.walk('data/scenarios'))[1]
for directory in scenarios:
	while True:
		Join = raw_input('Would you like to run a selenium experiment?(y/n)\n')
		if Join == "y" or Join == "yes" or Join == "Y" or Join == "yes":
			break
		elif Join == "n" or Join == "no" or Join == "N" or Join == "no":
			exit()
		else:
			Join = raw_input('Would you like to run a selenium experiment?(y/n)\n')
	osStatement = "selenium/selenium_driver " + TYPE + " " + MANIFEST + " " + TOPDIR + "data/scenarios/" +  directory + " 15"
	# print(osStatement)
	os.system(osStatement);
	print("after wait")

	# Copy exchange server logs to current directory
	# copyStatemnt = "rsync -avz --remove-source-files -e ssh ubuntu@ec2-54-149-235-92.us-west-2.compute.amazonaws.com:/var/HFT2/CDA_DATA/* " + TOPDIR + "data/scenarios/" + directory
	# # print(copyStatemnt)
	# os.system(copyStatemnt)


# # Driveer Phase 5:
# #       trigger query 

# scenarios = next(os.walk('data/scenarios'))[1]
# for directory in scenarios:
# 	osStatement = "python query.py data/scenarios/" + directory + "/query.config data/scenarios/" + directory + "/output.csv"
# 	# print(osStatement)
# 	os.system(osStatement);
