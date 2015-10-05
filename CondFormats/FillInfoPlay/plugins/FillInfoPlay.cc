// -*- C++ -*-
//
// Package:    CondFormats/FillInfoPlay
// Class:      FillInfoPlay
// 
/**\class FillInfoPlay FillInfoPlay.cc CondFormats/FillInfoPlay/plugins/FillInfoPlay.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Giovanni Franzoni
//         Created:  Mon, 05 Oct 2015 07:41:29 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/EventSetup.h"

#include "CondFormats/RunInfo/interface/FillInfo.h"
#include "CondFormats/DataRecord/interface/FillInfoRcd.h"

#include "FWCore/Framework/interface/ESHandle.h"

#include "CondFormats/SiPixelObjects/interface/SiPixelTemplateDBObject.h"
#include "CondFormats/DataRecord/interface/SiPixelTemplateDBObjectRcd.h"



//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class FillInfoPlay : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit FillInfoPlay(const edm::ParameterSet&);
      ~FillInfoPlay();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

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
FillInfoPlay::FillInfoPlay(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed
  //usesResource("TFileService");

}


FillInfoPlay::~FillInfoPlay()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
FillInfoPlay::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;


   std::cout << "++++ FillInfoPlay GF " << std::endl;

   // std::cout << "GF FillInfoPlay asking for SiPixelTemplateDBObject to the event setup " << std::endl;
   //edm::ESHandle<SiPixelTemplateDBObject> pixSetup;
   //iSetup.get<SiPixelTemplateDBObjectRcd>().get(pixSetup);
   //std::cout << "GF FillInfoPlay I have SiPixelTemplateDBObject " << std::endl;

   std::cout << "GF FillInfoPlay asking for FillInfoRcd to the event setup " << std::endl;
   edm::ESHandle<FillInfo> pSetup;
   iSetup.get<FillInfoRcd>().get(pSetup);
   std::cout << "GF FillInfoPlay do I have " << (*pSetup) << "?" << std::endl;



#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------
void 
FillInfoPlay::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FillInfoPlay::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FillInfoPlay::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(FillInfoPlay);
