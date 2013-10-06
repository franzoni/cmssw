# import the definition of the steps and input files:
from  Configuration.PyReleaseValidation.relval_steps import *

# here only define the workflows as a combination of the steps defined above:
workflows = Matrix()

# plain minbias
workflows[20011] = ['', ['MinBiasVHS','DIGI','RECO','HARVEST']]

#neutrino gun
workflows[20012] = ['', ['NeutrinoPt2to20gun','DIGI','RECO','HARVEST']]

# minbias with G4 customization 
workflows[20013] = ['', ['MinBiasVHS-QGSP-FTFP-BERT','DIGI','RECO','HARVEST']]
