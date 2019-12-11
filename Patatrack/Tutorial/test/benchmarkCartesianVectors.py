import FWCore.ParameterSet.Config as cms

process = cms.Process("PRINT")

process.options = cms.untracked.PSet(
  numberOfThreads = cms.untracked.uint32( 1 ),
  numberOfStreams = cms.untracked.uint32( 1 ),
  wantSummary = cms.untracked.bool( True )
)

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring("file:cylindricalVectors.root"),
)

process.convertToCartesianVectors = cms.EDProducer('ConvertToCartesianVectors',
  input = cms.InputTag('generateCylindricalVectors')
)

process.path = cms.Path(process.convertToCartesianVectors)

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32( -1 )
)
