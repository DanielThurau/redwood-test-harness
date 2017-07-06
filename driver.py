import os
import sys

# Driver Phase 1 :
#	Copy Specified Gherkin text to Gherkin Module
#	Start Gherkin
file = sys.argv[1];
osStatement = "cp " + file + " gherkin-behave/"
os.system(osStatement);
