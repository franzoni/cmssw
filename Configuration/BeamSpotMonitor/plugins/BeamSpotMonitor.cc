// -*- C++ -*-
//
// Package:    Configuration/BeamSpotMonitor
// Class:      BeamSpotMonitor
// 
/**\class BeamSpotMonitor BeamSpotMonitor.cc Configuration/BeamSpotMonitor/plugins/BeamSpotMonitor.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Giovanni Franzoni
//         Created:  Wed, 27 Aug 2014 13:47:27 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "CondFormats/DataRecord/interface/BeamSpotObjectsRcd.h"
#include "CondFormats/BeamSpotObjects/interface/BeamSpotObjects.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TH2F.h"

//
// class declaration
//

class BeamSpotMonitor : public edm::EDAnalyzer {
   public:
      explicit BeamSpotMonitor(const edm::ParameterSet&);
      ~BeamSpotMonitor();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------

  TH2F * h_sigmaBeamZ;
  TH2F * h_sigmaBeamY;
  TH2F * h_sigmaBeamX;

  TH2F * h_BeamZ;
  TH2F * h_BeamY;
  TH2F * h_BeamX;

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
BeamSpotMonitor::BeamSpotMonitor(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed

  edm::Service<TFileService> fs;
  int numLS = 2004;
  
  h_sigmaBeamZ = fs->make<TH2F>("sigmaBeamZ", "sigmaBeamZ", numLS, 0., numLS-1,500, 4.6, 5.1 );
  h_sigmaBeamY = fs->make<TH2F>("sigmaBeamY", "sigmaBeamY", numLS, 0., numLS-1,500, 0.0016, 0.0021 );
  h_sigmaBeamX = fs->make<TH2F>("sigmaBeamX", "sigmaBeamX", numLS, 0., numLS-1,500, 0.0016, 0.0021 );

  h_BeamZ = fs->make<TH2F>("BeamZ", "BeamZ", numLS, 0., numLS-1,500, -1     , 0      );
  h_BeamY = fs->make<TH2F>("BeamY", "BeamY", numLS, 0., numLS-1,500, 0.0633 , 0.0639 );
  h_BeamX = fs->make<TH2F>("BeamX", "BeamX", numLS, 0., numLS-1,500, 0.071  , 7.23   );

}


BeamSpotMonitor::~BeamSpotMonitor()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
BeamSpotMonitor::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;



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
BeamSpotMonitor::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
BeamSpotMonitor::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
BeamSpotMonitor::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
BeamSpotMonitor::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
BeamSpotMonitor::beginLuminosityBlock(edm::LuminosityBlock const& iLumi, edm::EventSetup const& iSetup)
{
  std::cout << "\n ++ beginLuminosityBlock LS: " << iLumi.id().luminosityBlock() << " run: " << std::endl;
  
  //Read BeamSpot from DB
  edm::ESHandle<BeamSpotObjects> bsDBHandle;
  try{
    iSetup.get<BeamSpotObjectsRcd>().get(bsDBHandle);
  }
  catch( cms::Exception& exception ){                                 
    std::cout<< "AlcaBeamMonitor "
      << exception.what(); 
    return;           
  }


  if(bsDBHandle.isValid()) { // check the product
    const BeamSpotObjects *spotDB = bsDBHandle.product();
    std::cout << " beam spot params: "
	      << "\t x: " << spotDB->GetX() << "\t widthx: " <<  spotDB->GetBeamWidthX()
	      << "\t y: " << spotDB->GetY() << "\t widthy: " <<  spotDB->GetBeamWidthY()
	      << "\t z: " << spotDB->GetZ() << "\t sigz: "   << spotDB->GetSigmaZ()
	      << std::endl;

    h_sigmaBeamX->Fill(iLumi.id().luminosityBlock(), spotDB->GetBeamWidthX());
    h_sigmaBeamY->Fill(iLumi.id().luminosityBlock(), spotDB->GetBeamWidthY());
    h_sigmaBeamZ->Fill(iLumi.id().luminosityBlock(), spotDB->GetSigmaZ());

    h_BeamX->Fill(iLumi.id().luminosityBlock(), spotDB->GetX());
    h_BeamY->Fill(iLumi.id().luminosityBlock(), spotDB->GetY());
    h_BeamZ->Fill(iLumi.id().luminosityBlock(), spotDB->GetZ());

  }
  else {
    std::cout << "** bsDBHandle is not valid" << std::endl;
  }

}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
BeamSpotMonitor::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}


// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
BeamSpotMonitor::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(BeamSpotMonitor);
