import os
import sys
from subprocess import call


file = sys.argv[1];
osStatement = "cp " + file + " gherkin-behave/"
#call(osStatement);
print(osStatement);
