import os
import sys

print("usage: python driver.py gherkin-file")

TOPDIR = os.path.dirname(os.path.realpath(__file__)) + "/"
MANIFEST= TOPDIR + "data/manifests/manifest_test.json"
TYPE = "HFT-CDA"


# Driver Phase 1 :
#	Copy Specified Gherkin text to Gherkin Module
file = sys.argv[1];
print(file)
osStatement = "cp " + file + " ./features/gherkin.feature"
print(osStatement)
os.system(osStatement);

# Driver Phase 2 : 
# 	Run steps.py in the Behave Gherkin-behave module
print("before run")
osStatement = "python test.py"
os.system(osStatement); 
print("after run")
osStatement = "rm -rf features/gherkin.feature"
os.system(osStatement);

# Driver Phase 3 :
#	run python script on Scenarios dir
#osStatement = "python createConfig.py"
#os.system(osStatement);

# Driver Phase 4:
#       trigger selenium
#scenarios = next(os.walk('data/scenarios'))[1]
#for directory in scenarios:

#	osStatement = "selenium/test_sel " + TYPE + " " + MANIFEST + " " + TOPDIR + "data/scenarios/" +  directory + " 10"
#	print(osStatement)
#	os.system(osStatement);

# Driveer Phase 5:
#       trigger query 
#osStatement = "python query.py data/scenarios/Scenario1/query.config"
#os.system(osStatement);
