#ifndef CalibTracker_SiPixelESProducers_SiPixelTemplateDBObjectESProducerBis_h
#define CalibTracker_SiPixelESProducers_SiPixelTemplateDBObjectESProducerBis_h
// -*- C++ -*-
//
// Package:    SiPixelTemplateDBObjectESProducerBis
// Class:      SiPixelTemplateDBObjectESProducerBis
// 
/**\class SiPixelTemplateDBObjectESProducerBis SiPixelTemplateDBObjectESProducerBis.cc CalibTracker/SiPixelESProducers/plugin/SiPixelTemplateDBObjectESProducerBis.cc

 Description: ESProducer for magnetic-field-dependent local reco templates

 Implementation: Used inside the RecoLocalTracker/Records/TkPixelRecord to select the correct db for given magnetic field
*/
//
// Original Author:  D.Fehling
//         Created:  Tue Sep 29 14:49:31 CET 2009
//
//

#include "FWCore/Framework/interface/ESProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CondFormats/SiPixelObjects/interface/SiPixelTemplateDBObject.h"
#include "CalibTracker/Records/interface/SiPixelTemplateDBObjectESProducerRcd.h"


#include "CondFormats/RunInfo/interface/FillInfo.h"
#include "CondFormats/DataRecord/interface/FillInfoRcd.h"

class SiPixelTemplateDBObjectESProducerBis : public edm::ESProducer  {

public:

	SiPixelTemplateDBObjectESProducerBis(const edm::ParameterSet& iConfig);
  ~SiPixelTemplateDBObjectESProducerBis();

  typedef boost::shared_ptr<FillInfo> ReturnType;

	ReturnType produce(const FillInfoRcd  &);
 };
#endif
