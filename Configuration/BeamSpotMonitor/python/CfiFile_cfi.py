import FWCore.ParameterSet.Config as cms

demo = cms.EDAnalyzer('BeamSpotMonitor'
)


BeamSpotMonitor = cms.Sequence( demo )
