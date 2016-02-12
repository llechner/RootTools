''' A TreeReader runs over a sample and evaluates extra variables.
Useful for using in a plot makro with complex derived observables.
'''

# Standard imports
import sys
from math import sqrt, cos
import ROOT
from RootTools.tools.Sample import Sample
from RootTools.tools.Variable import Variable, ScalarType, VectorType
from RootTools.tools.TreeReader import TreeReader
from RootTools.tools.logger import get_logger
import RootTools.tools.helpers as helpers
# argParser
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel', 
      action='store',
      nargs='?',
      choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],
      default='INFO',
      help="Log level for logging"
)

args = argParser.parse_args()
logger = get_logger(args.logLevel, logFile = None)

# Samplefrom files
s0 = Sample.fromFiles("s0", files = ["example_data/file_0.root"], treeName = "Events")

variables =  [ Variable.fromString('Jet[pt/F,eta/F,phi/F]' ) ] \
           + [ Variable.fromString(x) for x in [ 'met_pt/F', 'met_phi/F' ] ]

# Defining a variable and giving it a filler
cosMetPhi = Variable.fromString('cosMetPhi/F') 
cosMetPhi.filler = helpers.uses(lambda data: cos( data.met_phi ) , "met_phi/F")
filled_variables = [ cosMetPhi ]

h=ROOT.TH1F('met','met',100,0,0)
r = s0.treeReader( variables = variables, filled_variables = filled_variables, selectionString = "met_pt>100")
r.start()
while r.run():
    h.Fill( r.data.cosMetPhi )
