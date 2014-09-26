import FWCore.ParameterSet.Config as cms

def customiseBS(process):
    
    #process.VtxSmeared = cms.EDProducer("BetafuncEvtVtxGenerator",
    #                                    Phi = cms.double(0.0),
    #                                    Y0 = cms.double(0.3929),
    #                                    BetaStar = cms.double(70.0),
    #                                    Emittance = cms.double(5.86e-08),
    #                                    SigmaZ = cms.double(6.16),
    #                                    TimeOffset = cms.double(0.0),
    #                                    Alpha = cms.double(0.0),
    #                                    X0 = cms.double(0.244),
    #                                    Z0 = cms.double(0.4145),
    #                                    src = cms.InputTag("generator"),
    #                                    readDB = cms.bool(False)
    #                                    )
    
    process.VtxSmeared = cms.EDProducer("BetafuncEvtVtxGenerator",
                                        Phi = cms.double(0.0),
                                        Y0 = cms.double(0.0),
                                        BetaStar = cms.double(65.0),
                                        Emittance = cms.double(5.411e-08),
                                        SigmaZ = cms.double(5.3),
                                        TimeOffset = cms.double(0.0),
                                        Alpha = cms.double(0.0),
                                        X0 = cms.double(0.0322),
                                        Z0 = cms.double(0.0),
                                        src = cms.InputTag("generator"),
                                        readDB = cms.bool(False)
                                        )

    return process
