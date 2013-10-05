# import the definition of the steps and input files:
from  Configuration.PyReleaseValidation.relval_steps import *

# here only define the workflows as a combination of the steps defined above:
workflows = Matrix()

# plain minbias
workflows[20011] = ['', ['MinBiasVHS','DIGI','RECO','HARVEST']]

#neutrino gun
#workflows[20011] = ['', ['MinBiasVHS','DIGI','RECO','HARVEST']]
