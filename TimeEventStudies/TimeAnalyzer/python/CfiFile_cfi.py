import FWCore.ParameterSet.Config as cms

TimeAnalysis = cms.EDAnalyzer('TimeAnalyzer',
                              acceptedParticleTypes = cms.vint32( 11,-11 ),
                              lowestpt=cms.double( 20.0 ),
			      acceptedParentTypes = cms.vint32(23),
                              )
