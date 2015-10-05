# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --conditions auto:run2_data -s RAW2DIGI --runUnscheduled --process reRECO --data --eventcontent DQM --hltProcess reHLT --scenario pp --datatier DQMIO -n 1 --filein file:step2.root --fileout file:step3.root
import FWCore.ParameterSet.Config as cms

process = cms.Process('reRECO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

# Input source
process.source = cms.Source("PoolSource",
    # fileNames = cms.untracked.vstring('file:step2.root'),
    fileNames = cms.untracked.vstring('/store/data/Run2015B/MuonEG/RAW/v1/000/251/251/00000/2CED917D-CA25-E511-AE88-02163E01416E.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:step3.root'),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

#process.FillInfoESProducer = cms.ESProducer("FillInfoESProducer")
#process.FillInfoESProducer = cms.ESProducer("FillInfoESProducerBis")

#process.siPixelTemplateDBObjectESProducer = cms.ESProducer( "SiPixelTemplateDBObjectESProducer" )
# SiPixelTemplateDBObjectESProducerBis started off as an identical copy of SiPixelTemplateDBObjectESProducer, simply renamed
process.siPixelTemplateDBObjectESProducer = cms.ESProducer( "SiPixelTemplateDBObjectESProducerBis" )

process.load('CondFormats.FillInfoPlay.CfiFile_cfi')
#from CondFormats.FillInfoPlay.CfiFile_cfi import demo
process.mydemo = cms.EDAnalyzer('FillInfoPlay')
process.demo_step = cms.Path(process.mydemo)



# Schedule definition
process.schedule = cms.Schedule(
    process.demo_step,
    process.raw2digi_step,process.DQMoutput_step)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
from FWCore.ParameterSet.Utilities import cleanUnscheduled
process=cleanUnscheduled(process)

