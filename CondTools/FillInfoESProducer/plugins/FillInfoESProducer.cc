// -*- C++ -*-
//
// Package:    CondTools/FillInfoESProducer
// Class:      FillInfoESProducer
// 
/**\class FillInfoESProducer FillInfoESProducer.h CondTools/FillInfoESProducer/plugins/FillInfoESProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Giovanni Franzoni
//         Created:  Mon, 05 Oct 2015 06:39:15 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/ModuleFactory.h"
#include "FWCore/Framework/interface/ESProducer.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ESProducts.h"

#include <iostream>

#include <boost/shared_ptr.hpp>
#include "boost/mpl/vector.hpp"

#include "CondFormats/RunInfo/interface/FillInfo.h"
#include "CondFormats/DataRecord/interface/FillInfoRcd.h"

//
// class declaration
//

class FillInfoESProducer : public edm::ESProducer {
   public:
      FillInfoESProducer(const edm::ParameterSet&);
      ~FillInfoESProducer();
  
  //typedef std::shared_ptr<FillInfo> ReturnType;
      typedef boost::shared_ptr<FillInfo> ReturnType;

      ReturnType produce(const FillInfoRcd&);
   private:
      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
FillInfoESProducer::FillInfoESProducer(const edm::ParameterSet& iConfig)
{

  std::cout << "GF FillInfoESProducer construct" << std::endl;
  
   //the following line is needed to tell the framework what
   // data is being produced
   setWhatProduced(this);

   //now do what ever other initialization is needed
}


FillInfoESProducer::~FillInfoESProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
FillInfoESProducer::ReturnType
FillInfoESProducer::produce(const FillInfoRcd& iRecord)
{

  std::cout << "GF FillInfoESProducer produce" << std::endl;
  
   using namespace edm::es;
   //std::shared_ptr<FillInfo> pFillInfo;
   boost::shared_ptr<FillInfo> pFillInfo;
   pFillInfo -> setInjectionScheme( std::string ("25ns_pippo") );
   return pFillInfo;
   //   return products(pFillInfo);

}

//define this as a plug-in
DEFINE_FWK_EVENTSETUP_MODULE(FillInfoESProducer);
