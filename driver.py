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

# Driver Phase 4:
#       trigger selenium
osStatement = "selenium/test_sel"
os.system(osStatement);

# Driveer Phase 5:
#       trigger query 
osStatement = "python query.py data/scenarios/Scenario1/query.config"
os.system(osStatement);
