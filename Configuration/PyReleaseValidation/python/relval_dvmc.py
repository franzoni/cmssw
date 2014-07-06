# import the definition of the steps and input files:
from  Configuration.PyReleaseValidation.relval_steps import *

# here only define the workflows as a combination of the steps defined above:
workflows = Matrix()

###############################
# MC basics:  MinBias for PU
###############################

# plain MC minbias
workflows[20011] = ['', ['MinBiasVHS','DIGIdvmc','RECOdvmc','HARVESTdvmc']]
workflows[20011.1] = ['', ['MinBiasVHS']]
#neutrino gun
workflows[20012] = ['', ['SingleNuE10','DIGIdvmc','RECOdvmc','HARVESTdvmc']]
workflows[20012.1] = ['', ['SingleNuE10']]


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
workflows[20105] = ['',['RunMu2012Cdvmc','RECODSplitdvmc','HARVESTDdvmc']]
# 
workflows[20106] = ['',['ZMuSkim2012Cdvmc','RECOSKIMdvmc','HARVESTDdvmc']]
#
workflows[20107] = ['',['RunJetMon2012Cdvmc','FILTERJetMon2012Ddvmc','RECODdvmc','HARVESTDdvmc']]                # FIX: remove the selection on one run!
# 
workflows[20108] = ['',['RunJetHT2012Cdvmc','RECODdvmc','HARVESTDdvmc']]
# high PU ZeroBias 
workflows[20109] = ['',['RunZBias2012Cdvmc','RECODSplitdvmc','HARVESTDdvmc']]
# low PU ZeroBias 
workflows[20110] = ['',['RunZBias2012Advmc','RECOZBias2012Advmc','HARVESTDdvmc']]
# 25 ns ZeroBias 
workflows[20111] = ['',['RunZBias2012Ddvmc','RECODdvmc','HARVESTDdvmc']]


#################################################
# MC samples for comparisons : full and fast sim
#################################################
# typical min bias run 2012C
workflows[20201] = ['', ['SingleNuE10','DIGIPU203002Splitdvmc','RECOMIN203002dvmc','HARVESTdvmc','ALCAMIN']]
# high pile up
workflows[20202] = ['', ['SingleNuE10','DIGIPU198588dvmc','RECOMIN198588dvmc','HARVESTdvmc','ALCAMIN']]
# 25 ns to be done when GT available FIX <<<<<<<===============
workflows[20203] = ['', ['SingleNuE10','DIGIPU209148dvmc','RECOMIN209148dvmc','HARVESTdvmc','ALCAMIN']]
# re-digi single MB for low pu
workflows[20204] = ['', ['MinBiasVHS','DIGIPU193092dvmc','RECOMIN193092dvmc','HARVESTdvmc']]

workflows[20205] = ['', ['ZEEdvmc','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]

# article 5591 still accessible in eos;  match efficiency 0.43; local tests ok.
workflows[20206] = ['', ['DYJetsToLL','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
# 

workflows[20207] = ['', ['ZMMdvmc','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]

# gen level filter pull requested ; issue with cmsDriver.py and handling of filters
workflows[20208] = ['', ['ZMMGammadvmc','DIGIPU2012Cdvmc','RECO2012Cdvmc','HARVESTdvmc',]]

# 
workflows[20209] = ['', ['WMdvmc','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
# 
workflows[20210] = ['', ['JpsiMMdvmc','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]

# The following wf's (jetMet) may need be re-run with DIGIPU2012Cdvmc (btag)
workflows[20211] = ['', ['QCD_Pt_30to50','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
workflows[20212] = ['', ['QCD_Pt_50to80','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
workflows[20213] = ['', ['QCD_Pt_80to120','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
workflows[20214] = ['', ['QCD_Pt_120to170','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
workflows[20215] = ['', ['QCD_Pt_170to300','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]
workflows[20216] = ['', ['QCD_Pt_300to470','DIGIPU203002dvmc','RECO203002dvmc','HARVESTdvmc']]

# typical min bias run 2012C
workflows[20201.5] = ['',['SingleNuE10FS203002dvmc','HARVESTFSdvmc']]
# high pile up
workflows[20202.5] = ['',['SingleNuE10FS198588dvmc','HARVESTFSdvmc']]
# 25 ns to be done when GT available FIX <<<<<<<===============
workflows[20203.5] = ['',['SingleNuE10FS209148dvmc','HARVESTFSdvmc']]
# re-digi single MB for low pu
workflows[20204.5] = ['', ['MinBiasVHFSdvmc','HARVESTFSdvmc']]
# workflows[20204] = ['', ['MinBiasVHS','DIGIPU193092dvmc','RECOMIN193092dvmc','HARVESTdvmc']]
workflows[20205.5] = ['', ['ZEEFSdvmc','HARVESTFSdvmc']]

# article 5591 still accessible in eos;  match efficiency 0.43; local tests ok.
workflows[20206.5] = ['', ['DYJetsToLLFSdvmc','HARVESTFSdvmc']]
# 

workflows[20207.5] = ['', ['ZMMFSdvmc','HARVESTFSdvmc']]

# gen level filter pull requested ; issue with cmsDriver.py and handling of filters
workflows[20208.5] = ['', ['ZMMGammaFSdvmc','HARVESTFSdvmc']]

# 
workflows[20209.5] = ['', ['WMFSdvmc','HARVESTFSdvmc']]
# 
workflows[20210.5] = ['', ['JpsiMMFSdvmc','HARVESTFSdvmc']]

# The following wf's (jetMet) may need be re-run with DIGIPU2012Cdvmc (btag)
workflows[20211.5] = ['', ['QCD_Pt_30to50FSdvmc','HARVESTFSdvmc']]
workflows[20212.5] = ['', ['QCD_Pt_50to80FSdvmc','HARVESTFSdvmc']]
workflows[20213.5] = ['', ['QCD_Pt_80to120FSdvmc','HARVESTFSdvmc']]
workflows[20213.6] = ['', ['QCD_Pt_80to120FSdvmc_db1','HARVESTFSdvmc']]
workflows[20213.7] = ['', ['QCD_Pt_80to120FSdvmc_db2','HARVESTFSdvmc']]
workflows[20214.5] = ['', ['QCD_Pt_120to170FSdvmc','HARVESTFSdvmc']]
workflows[20215.5] = ['', ['QCD_Pt_170to300FSdvmc','HARVESTFSdvmc']]
workflows[20216.5] = ['', ['QCD_Pt_300to470FSdvmc','HARVESTFSdvmc']]
