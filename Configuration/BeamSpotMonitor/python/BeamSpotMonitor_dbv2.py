# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --process BeamSpotMonitor -s USER:Configuration/BeamSpotMonitor/CfiFile_cfi.BeamSpotMonitor --conditions auto:run1_data --data --python BeamSpotMonitor.py --no_exec --filein filelist:step1_dasquery.log --lumiToProcess step1_lumiRanges.log --customise_command=process.TFileService=cms.Service("TFileService",fileName = cms.string("BeamSpotMonitor_dbv2.root"),closeFileFast = cms.untracked.bool(True)) -n 500000 --no_output --useCondDBv2 --python_filename=BeamSpotMonitor_dbv2.py
import FWCore.ParameterSet.Config as cms

process = cms.Process('BeamSpotMonitor')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.BeamSpotMonitor.CfiFile_cfi')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(500000)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring('/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/0603DDF8-903D-E211-A48C-001A92971B8C.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/1092BB91-8F3D-E211-A2DC-0025905964C2.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/12CF48A2-8F3D-E211-AB74-0018F3D096BE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/183153EB-973D-E211-99C9-00261894387E.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/188AFC48-923D-E211-99C1-0025905964A6.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/1E95A244-8F3D-E211-AD39-003048678A80.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/249C6CB2-903D-E211-A6BF-003048678FAE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/26ABB8DC-903D-E211-982A-003048678FAE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/36249757-903D-E211-830C-001A92811718.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/38941A9A-8F3D-E211-9948-001A92971BC8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/3A479E01-903D-E211-8FDD-002590596468.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/4428B960-8F3D-E211-B1BC-0026189438CB.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/4C544B26-903D-E211-B61E-003048678F74.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/58FF4633-8F3D-E211-9280-002590596484.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/5C6E9835-913D-E211-ACCB-001A92971B7C.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/66A7A3FC-8F3D-E211-950E-00261894388A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/6A8267D2-8F3D-E211-96E4-0025905938D4.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/7022D743-903D-E211-AB30-00261894391F.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/70CE3863-903D-E211-88FF-0018F3D096BE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/72E5836E-8F3D-E211-ABF5-003048678FF4.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/744A23B3-8F3D-E211-A947-0025905964C0.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/7A257255-903D-E211-B3D7-0018F3D0968A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/80A73760-923D-E211-A5B0-001A92971BDC.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/80BA4440-923D-E211-8A1F-0025905964A6.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/82911CB5-8F3D-E211-B34C-00259059642A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/8A00549D-8F3D-E211-8930-001A92810AB2.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/8CA861E4-903D-E211-9005-001A92971B8C.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/8CDC0B11-903D-E211-909E-003048678FF8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/8E387E6A-933D-E211-A14D-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/94197E6A-933D-E211-804E-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/9A656A5D-8F3D-E211-AA31-00304867BFBC.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/AA0DF05F-903D-E211-B443-003048678FFA.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/B80A592F-933D-E211-98BB-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/BC2DF6DB-903D-E211-8F72-003048678FAE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/BE0DBA69-8F3D-E211-A227-0026189438B0.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/C2637E6A-933D-E211-A677-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/C4DAA937-903D-E211-BD1E-002618943831.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/C4FE864F-903D-E211-8EA1-002590596498.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/CCB6C39D-903D-E211-AD2B-003048678FFA.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/D2A260EE-923D-E211-BC4B-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/D2F2E331-903D-E211-BD36-003048678F74.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/DA2D7312-923D-E211-90F8-001A92971BDC.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/E0380636-933D-E211-B493-003048FF9AC6.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/E0D74245-8F3D-E211-AFB2-003048678A6A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/E0FD8E55-8F3D-E211-A163-003048678FF8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/EE36B03C-903D-E211-80E5-0018F3D0960C.root'),
    lumisToProcess = cms.untracked.VLuminosityBlockRange("208307:1-208307:268435455")
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('step2 nevts:500000'),
    name = cms.untracked.string('Applications')
)

# Output definition

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run1_data', '')

# Path and EndPath definitions
process.user_step = cms.Path(process.BeamSpotMonitor)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.user_step,process.endjob_step)


# Customisation from command line
process.TFileService=cms.Service("TFileService",fileName = cms.string("BeamSpotMonitor_dbv2.root"),closeFileFast = cms.untracked.bool(True))
