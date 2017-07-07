import os
import sys

# Driver Phase 1 :
#	Copy Specified Gherkin text to Gherkin Module
file = sys.argv[1];
osStatement = "cp " + file + " ./features/gherkin.feature"
os.system(osStatement);

# Driver Phase 2 : 
# 	Run steps.py in the Behave Gherkin-behave module
osStatement = "./features/steps/run.sh"
os.system(osStatement); 
osStatement = "rm -rf features/gherkin.feature"
os.system(osStatement);

# Driver Phase 3 :
#	run python script on Scenarios dir
osStatement = "python createConfig.py"
os.system(osStatement);
