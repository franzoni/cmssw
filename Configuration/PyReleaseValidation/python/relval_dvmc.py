# import the definition of the steps and input files:
from  Configuration.PyReleaseValidation.relval_steps import *

# here only define the workflows as a combination of the steps defined above:
workflows = Matrix()

###############################
# MC basics: MinBias for PU
###############################

# plain MC minbias (sent both in 612 and 621)
workflows[20011] = ['', ['MinBiasVHS','DIGIdvmc','RECOdvmc','HARVESTdvmc']]
#neutrino gun
workflows[20012] = ['', ['NeutrinoPt2to20gun','DIGIdvmc','RECOdvmc','HARVESTdvmc']]
# minbias MC with G4 customization 
workflows[20013] = ['', ['MinBiasVHS-QGSP-FTFP-BERT','DIGIdvmc','RECOdvmc','HARVESTdvmc']]

###############################
# data
###############################
# 
workflows[20101] = ['', ['RunMinBias2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# input dataset available at CERN => 20102 can be tested
workflows[20102] = ['',['ZElSkim2012Cdvmc','RECOSKIMdvmc','HARVESTDdvmc']]
# 
workflows[20103] = ['',['DoubleMu2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# 
workflows[20104] = ['',['DoubleMuParked2012Cdvmc','RECOSKIMdvmc','HARVESTDdvmc']]
# 
workflows[20105] = ['',['RunMu2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# 
workflows[20106] = ['',['ZMuSkim2012Cdvmc','RECOSKIMdvmc','HARVESTDdvmc']]
# STILL TO BE DONE
#workflows[20107] = ['',['RunMultiJet2012Cdvmc','RECODdvmc','HARVESTDdvmc']]                # FIX: remove the selection on one run!
#workflows[20107.1] = ['',['RunMultiJet2012Cdvmc','RECODmultiJetdvmc','HARVESTDdvmc']]      # FIX: remove run selection + *** fix filter***  !
#workflows[20107.2] = ['',['RunMultiJet2012Cdvmc','RECODmultiJetdvmcNEW','HARVESTDdvmc']]   # FIX: remove run selection + *** fix filter***  !
# STILL TO BE DONE
# 
workflows[20108] = ['',['RunJetHT2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# high PU ZeroBias 
workflows[20109] = ['',['RunZBias2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# low PU ZeroBias 
workflows[20110] = ['',['RunZBias2012Advmc','RECODdvmc','HARVESTDdvmc']]
# 25 ns ZeroBias 
workflows[20111] = ['',['RunZBias2012Ddvmc','RECODdvmc','HARVESTDdvmc']]


###############################
# MC samples for comparisons
###############################
# typical min bias run 2012C
workflows[20201] = ['', ['NeutrinoPt2to20gun','DIGIPU203002dvmc','RECOMIN203002dvmc','HARVESTdvmc','ALCAMIN']]
# high pile up
workflows[20202] = ['', ['NeutrinoPt2to20gun','DIGIPU198588dvmc','RECOMIN198588dvmc','HARVESTdvmc','ALCAMIN']]
# low pile up
workflows[20203] = ['', ['NeutrinoPt2to20gun','DIGIPU209148dvmc','RECOMIN209148dvmc','HARVESTdvmc','ALCAMIN']]
# 
workflows[20204] = ['', ['ZEEdvmc','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
# wf with lhe to be followed up
#workflows[20205] = ['', ['DYJetsToLL','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
# 
workflows[20206] = ['', ['ZMMdvmc','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
# gen level filter pull requested ; issue with cmsDriver.py and handling of filters
#workflows[20207] = ['', ['ZMMGammadvmc','DIGIPU2012Cdvmc','RECO2012Cdvmc','HARVESTdvmc',]]
# 
workflows[20208] = ['', ['WMdvmc','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
# 
workflows[20209] = ['', ['JpsiMMdvmc','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
#
workflows[20210] = ['', ['QCD_Pt_30to50','DIGIPU2012Cdvmc','RECO2012Cdvmc','HARVESTdvmc']]
workflows[20211] = ['', ['QCD_Pt_50to80','DIGIPU2012Cdvmc','RECO2012Cdvmc','HARVESTdvmc']]
workflows[20212] = ['', ['QCD_Pt_80to120','DIGIPU2012Cdvmc','RECO2012Cdvmc','HARVESTdvmc']]
workflows[20213] = ['', ['QCD_Pt_120to170','DIGIPU2012Cdvmc','RECO2012Cdvmc','HARVESTdvmc']]
workflows[20214] = ['', ['QCD_Pt_170to300','DIGIPU2012Cdvmc','RECO2012Cdvmc','HARVESTdvmc']]
workflows[20215] = ['', ['QCD_Pt_300to470','DIGIPU2012Cdvmc','RECO2012Cdvmc','HARVESTdvmc']]

