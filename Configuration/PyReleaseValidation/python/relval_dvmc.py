# import the definition of the steps and input files:
from  Configuration.PyReleaseValidation.relval_steps import *

# here only define the workflows as a combination of the steps defined above:
workflows = Matrix()

###############################
# MC basics: MinBias for PU
###############################

# plain MC minbias (sent both in 612 and 621)
workflows[20011] = ['', ['MinBiasVHS','DIGI','RECO','HARVEST']]
#neutrino gun
workflows[20012] = ['', ['NeutrinoPt2to20gun','DIGI','RECO','HARVEST']]
# minbias MC with G4 customization 
workflows[20013] = ['', ['MinBiasVHS-QGSP-FTFP-BERT','DIGI','RECO','HARVEST']]


###############################
# data
###############################
# 
workflows[20101] = ['', ['RunMinBias2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# 
workflows[20102] = ['',['ZElSkim2012Cdvmc','RECOSKIMdvmc','HARVESTDdvmc']]
# 
workflows[20103] = ['',['DoubleMu2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# 
workflows[20104] = ['',['DoubleMuParked2012Cdvmc','RECOSKIMdvmc','HARVESTDdvmc']]
# 
workflows[20105] = ['',['RunMu2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# 
workflows[20106] = ['',['ZMuSkim2012Cdvmc','RECOSKIMdvmc','HARVESTDdvmc']]
# 
workflows[20107] = ['',['RunJetMon2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# high PU ZeroBias 
workflows[20108] = ['',['RunZBias2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# low PU ZeroBias 
workflows[20109] = ['',['RunZBias2012Advmc','RECODdvmc','HARVESTDdvmc']]
# 25 ns ZeroBias 
workflows[20110] = ['',['RunZBias2012Ddvmc','RECODdvmc','HARVESTDdvmc']]


###############################
# MC samples for comparisons
###############################
workflows[20201] = ['', ['NeutrinoPt2to20gun','DIGIPUdvmc','RECOMIN','HARVEST','ALCAMIN']]
workflows[20202] = ['', ['QCD_Pt_80_120','DIGI','RECO','HARVEST']]

#  LocalWords:  HARVESTDdvmc
