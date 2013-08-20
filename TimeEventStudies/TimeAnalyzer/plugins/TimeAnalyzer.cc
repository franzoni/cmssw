// -*- C++ -*-
//
// Package:    TimeAnalyzer
// Class:      TimeAnalyzer
// 
/**\class TimeAnalyzer TimeAnalyzer.cc TimeEventStudies/TimeAnalyzer/plugins/TimeAnalyzer.cc

Description: [one line class summary]

Implementation:
[Notes on implementation]
*/
//
// Original Author:  Ivana Kurecic / Gianluca Cerminara / Giovanni Franzoni
//         Created:  Mon, 01 Jul 2013 07:44:21 GMT
// $Id$
//
//


// system include files
#include <memory>
#include <utility>

// ==> user include files
// =-> defaults
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

// =-> for development
#include <TMath.h>

#include "DataFormats/Common/interface/Handle.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/DetId/interface/DetId.h"

#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"

#include "RecoEcal/EgammaCoreTools/interface/EcalClusterTools.h"

#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"

#include "TFile.h"
#include "TH1.h"
#include "TCanvas.h"
#include "TPad.h"
#include "HepMC/SimpleVector.h"
#include "THStack.h"
#include "THistPainter.h"
#include "TH2.h"

#include "fun.h"

//
// class declaration
//

class TimeAnalyzer : public edm::EDAnalyzer {
public:
  explicit TimeAnalyzer(const edm::ParameterSet&);
  ~TimeAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

  //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

  // ----------member data ---------------------------

  // pointers to the histograms for persistency
  //  TH1F* h_nVtx_;
  //  TH1F* h_pType_;
  //  TH1F* h_pTypeSel_;
  //  TH1F* h_nSCEB_;
  //  TH1F* h_nSCEE_;
  TH1F* h_masses_;
  //  TH1F* h_pr_;
  TH1F* h_pperp_;
  TH1F* h_eta_;
  TH1F* h_phi_;
  //  THStack* h_SCstack_;
  TH1F* h_eclusterE_;
  TH1F* h_etaclusterE_;
  TH1F* h_phiclusterE_;
  TH1F* h_eclusterB_;
  TH1F* h_etaclusterB_;
  TH1F* h_phiclusterB_; 
  TH2F* h_eta_phi_;
  THStack* h_etacstack_;
  THStack* h_phicstack_;
  TH2F* h_ceta_phi_;
  TH1F* h_delta_e;
  TH1F* h_delta_b;
  TH1F* h_energies_;
  THStack* h_ecstack_;
  TH1F* h_massofmother_;
  TH1F* h_mothertype_;
  TH1F* h_ptotal_;
  TH1F* h_tdiffdet_;
  TH1F* h_tdiffsim_;
  TH1F* h_tdiffdetsim_;
  TH2F* h_dtofdet_zvtx_;
  TH2F* h_dtofdet_detad_;
  TH2F* h_dtofdet_dtofsim_;
  TH2F* h_dtofdiff_zvtx_;
  TH2F* h_dtofdiff_detad_;
  TH2F* h_dtofsim_zvtx_;
 
  // list of particle tipe(s) which are used for the study and matched to clusters/recHits
  std::vector<int> acceptedParticleTypes_;
  double lowestpt_;
  std::vector<int> acceptedParentTypes_;
  float inv_nofproducts_;
//  double lowestenergyparent_;
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
TimeAnalyzer::TimeAnalyzer(const edm::ParameterSet& iConfig)

{
  //now do what ever initialization is needed
  
  // list of particle tipe(s) which are used for the study and matched to clusters/recHits
  acceptedParticleTypes_ = iConfig.getParameter< std::vector<int> >("acceptedParticleTypes");
  lowestpt_ = iConfig.getParameter<double>("lowestpt");
  acceptedParentTypes_= iConfig.getParameter<std::vector<int>>("acceptedParentTypes");
  inv_nofproducts_=1.0/acceptedParticleTypes_.size();
//  lowestenergyparent_ = iConfig.getParameter<double>("lowestenergyparent");
}


TimeAnalyzer::~TimeAnalyzer()
{
 
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
TimeAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  //   using namespace reco;
  //   using namespace std;

#ifdef THIS_IS_AN_EVENT_EXAMPLE
  Handle<ExampleData> pIn;
  iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  ESHandle<SetupData> pSetup;
  iSetup.get<SetupRecord>().get(pSetup);
#endif

  unsigned int brojrazl=0;
  std::vector< std::vector<double>> particledata(9, std::vector<double> (acceptedParticleTypes_.size()+1,0.));
  float squaremomenta=0.;
  double particlecharge=0.0;
  int vertexmarker=0;

  // reconstructed vertex in the event
  Handle<reco::VertexCollection> vertexHandle;
  iEvent.getByLabel("offlinePrimaryVerticesWithBS", vertexHandle);
  const reco::VertexCollection * vertexCollection = vertexHandle.product();
  // reco vertex multiplicity
  //   h_nVtx_ -> Fill( vertexCollection->size() );
  math::XYZPoint recoVtx(0.,0.,0.);
  if (vertexCollection->size()>0) { recoVtx = vertexCollection->begin()->position();  }

  // get hold of the MC product and loop over truth-level particles 
  // standard numeric ParticleId:
  // http://www.physics.ox.ac.uk/CDF/Mphys/old/notes/pythia_codeListing.html
  Handle< edm::HepMCProduct > hepProd ;
  iEvent.getByLabel("generator",hepProd) ;
  const HepMC::GenEvent * myGenEvent = hepProd->GetEvent();
   
  // loop over MC particles
  for ( HepMC::GenEvent::particle_const_iterator p = myGenEvent->particles_begin(); p != myGenEvent->particles_end(); ++p ) 
    {
//       std::cout<<"before status check"<<std::endl;
      // You only want particles with status 1
      if  ((*p)->status()!=1 ) continue; 
//       std::cout<<"after status check, before id check"<<std::endl;
      //       h_pType_ ->  Fill((*p)->pdg_id()); 
       
      // match only to truth of desired particle types
      if (std::find(acceptedParticleTypes_.begin(), acceptedParticleTypes_.end(), (*p)->pdg_id())==acceptedParticleTypes_.end() )  continue;
//	std::cout<<"after id check, before minimal pt check"<<std::endl;
      if((*p)->pdg_id()>0) particlecharge=1.0;
	else particlecharge=-1.0;
      if(lowestpt_>(*p)->momentum().perp()) continue;
//	std::cout<<"after minimal pt check"<<std::endl;

  vertexmarker=0;
  for(HepMC::GenVertex::particle_iterator anc=(*p)->production_vertex()->particles_begin(HepMC::ancestors);
	anc!=(*p)->production_vertex()->particles_end(HepMC::ancestors); ++anc){
		if(std::find(acceptedParentTypes_.begin(), acceptedParentTypes_.end(), (*anc)->pdg_id())!=acceptedParentTypes_.end()){
			vertexmarker=(*anc)->pdg_id();
		}
  }

  if(vertexmarker==0) continue;
//  std::cout<<vertexmarker<<std::endl;

//      h_pTypeSel_ ->  Fill((*p)->pdg_id()); 

      h_masses_ -> Fill((*p)->momentum().m());
//      h_pr_ -> Fill((*p)->momentum().pseudoRapidity());
      h_pperp_ -> Fill((*p)->momentum().perp());
      h_eta_ -> Fill((*p)->momentum().eta());
      h_phi_ -> Fill((*p)->momentum().phi());
      h_eta_phi_ -> Fill((*p)->momentum().phi(),(*p)->momentum().eta());
      h_energies_ -> Fill((*p)->momentum().e());
      float p_eta=(*p)->momentum().eta();
      float p_phi=(*p)->momentum().phi();
      h_ptotal_ -> Fill(pow((*p)->momentum().px(),2)+pow((*p)->momentum().py(),2)+pow((*p)->momentum().pz(),2));

      // hard-coded names of recHit collections as in standard CMS data (AOD)
      // GF: send to configuration file
      std::string reducedEcalRecHitsEB = "reducedEcalRecHitsEB";
      std::string reducedEcalRecHitsEE = "reducedEcalRecHitsEE";

      // Ecal barrel RecHits : reach rechit holds energy and time information
      // reconstructed from the scintillation signal of one crystal
      edm::Handle<EcalRecHitCollection> pBarrelEcalRecHits ;
      const EcalRecHitCollection* theBarrelEcalRecHits = 0;
      if( iEvent.getByLabel (reducedEcalRecHitsEB,"", pBarrelEcalRecHits) && pBarrelEcalRecHits.isValid ())
	{
	  theBarrelEcalRecHits = pBarrelEcalRecHits.product () ;   
	}
      if (! (pBarrelEcalRecHits.isValid ()) )
	{
	  LogWarning ("TimeAnalyzer") << "reducedEcalRecHitsEB "
				      << " not available" ;
	  return ;
	}
      // Ecal endcap RecHits : reach rechit holds energy and time information
      // reconstructed from the scintillation signal of one crystal
      edm::Handle<EcalRecHitCollection> pEndcapEcalRecHits ;
      const EcalRecHitCollection* theEndcapEcalRecHits = 0;
      if( iEvent.getByLabel (reducedEcalRecHitsEE,"", pEndcapEcalRecHits) && pEndcapEcalRecHits.isValid ())
	{
	  theEndcapEcalRecHits = pEndcapEcalRecHits.product () ;   
	}
      if (! (pEndcapEcalRecHits.isValid ()) )
	{
	  LogWarning ("TimeAnalyzer") << "reducedEcalRecHitsEE "
				      << " not available" ;
	  return ;
	}
      
double eta_det=0.0;

      // superclusters are groups of neighboring Electromagnetic Calorimeter (ECAL) recHits
      // collecting the energy relesed by (at least) one particle impinging into the ECAL
      Handle<std::vector<reco::SuperCluster> > barrelSCHandle;
      iEvent.getByLabel("correctedHybridSuperClusters","",barrelSCHandle);
      const reco::SuperClusterCollection * barrelSCCollection = barrelSCHandle.product();
      //   h_nSCEB_ -> Fill( barrelSCCollection->size() );
      for(reco::SuperClusterCollection::const_iterator blah = barrelSCCollection->begin(); blah != barrelSCCollection->end(); blah++) {
	float deltaphib=blah->phi()-p_phi; if(deltaphib<-Pi()) deltaphib+=2*Pi(); if(deltaphib>Pi()) deltaphib-=2*Pi();
	eta_det=blah->eta();
	float deltaetab=eta_det-p_eta;
	float deltab = sqrt(deltaphib*deltaphib+deltaetab*deltaetab);
	// in the above, phi_SC is  phi_detector, while phi_particle is phi_physics
	// tolerate this confusion by extendeding cut on deltab to 0.3

	if(deltab>0.3) continue;
	  h_delta_b -> Fill(deltab);
	  h_eclusterB_ -> Fill( blah->rawEnergy() );
	  h_etaclusterB_ -> Fill( eta_det );
	  h_phiclusterB_ -> Fill( blah->phi() );
	  h_ceta_phi_ -> Fill( blah->phi(), eta_det );
	
	// the seed basic cluster as a component of the supercluster (SC)
	reco::CaloClusterPtr SCseed = blah->seed() ;
	// time of the seed recHit inside the seed BC (aka "time of the SC seed")
	std::pair<DetId, float> maxRH = EcalClusterTools::getMaximum( *SCseed, theBarrelEcalRecHits );
	DetId seedCrystalId = maxRH.first;
	EcalRecHitCollection::const_iterator seedRH = theBarrelEcalRecHits->find(seedCrystalId);
	float seedTime = (float)seedRH->time();
//	std::cout << "++ EB TimeAnalyzer rechit seedTime and energy : "<< seedTime << "\t" << seedRH->energy() << std::endl;

        for(unsigned int bb=0;bb<acceptedParticleTypes_.size();bb++) {
          if( (*p)->pdg_id()==acceptedParticleTypes_[bb] &&
              particledata[6][bb]<(*p)->momentum().perp() )
            {
              particledata[3][bb]=(*p)->momentum().e();
              particledata[0][bb]=(*p)->momentum().px();
              particledata[1][bb]=(*p)->momentum().py();
              particledata[2][bb]=(*p)->momentum().pz();
              particledata[4][bb]=vertexmarker;
              particledata[5][bb]=seedTime;
	      particledata[6][bb]=(*p)->momentum().perp();
	      particledata[7][bb]=tofc_ddata_(particledata[6][bb],particlecharge,eta_det,recoVtx.Z());
	      particledata[8][bb]=eta_det;
//		std::cout<<particledata[4][0]<<" asdfasf"<<std::endl;
            }
	}// close loop  over acceptedParticleTypes_
      }
//std::cout<<recoVtx.Z()<<std::endl;
      Handle<std::vector<reco::SuperCluster> > endcapSCHandle;
      iEvent.getByLabel("correctedMulti5x5SuperClustersWithPreshower","",endcapSCHandle);
      const reco::SuperClusterCollection * endcapSCCollection = endcapSCHandle.product();
      //   h_nSCEE_ -> Fill( endcapSCCollection->size() );
      for(reco::SuperClusterCollection::const_iterator blah = endcapSCCollection->begin(); blah != endcapSCCollection->end(); blah++) {
	float deltaphie=blah->phi()-p_phi; if(deltaphie<-Pi()) deltaphie+=2*Pi(); if(deltaphie>Pi()) deltaphie-=2*Pi();
	eta_det=blah->eta();
	float deltaetae=eta_det-p_eta;
	float deltae = sqrt(deltaphie*deltaphie+deltaetae*deltaetae);
	// in the above, phi_SC is  phi_detector, while phi_particle is phi_physics
	// tolerate this confusion by extendeding cut on deltab to 0.3

	// if no matching between current SC and current truth particle => return 
	if(deltae>0.3) continue; 

	h_delta_e -> Fill(deltae);
	h_eclusterE_ -> Fill( blah->rawEnergy() );
	h_etaclusterE_ -> Fill( eta_det );
	h_phiclusterE_ -> Fill( blah->phi() );
	h_ceta_phi_ -> Fill( blah->phi(), eta_det );

	// the seed basic cluster as a component of the supercluster (SC)
	reco::CaloClusterPtr SCseed = blah->seed() ;
	// time of the seed recHit inside the seed BC (aka "time of the SC seed")
	std::pair<DetId, float> maxRH = EcalClusterTools::getMaximum( *SCseed, theEndcapEcalRecHits );
	DetId seedCrystalId = maxRH.first;
	EcalRecHitCollection::const_iterator seedRH = theEndcapEcalRecHits->find(seedCrystalId);
	float seedTime = (float)seedRH->time();
//	std::cout << "++ EE TimeAnalyzer seedTime and energy : "<< seedTime << "\t" << seedRH->energy() << std::endl;

	for(unsigned int broj=0;broj<acceptedParticleTypes_.size();broj++) {
	  if( (*p)->pdg_id()==acceptedParticleTypes_[broj] && 
	      particledata[6][broj]<(*p)->momentum().perp() ) 
	    {
	      particledata[3][broj]=(*p)->momentum().e();
	      particledata[0][broj]=(*p)->momentum().px();
	      particledata[1][broj]=(*p)->momentum().py();
	      particledata[2][broj]=(*p)->momentum().pz();
	      particledata[4][broj]=vertexmarker;
	      particledata[5][broj]=seedTime;
	      particledata[6][broj]=(*p)->momentum().perp();
              particledata[7][broj]=tofc_ddata_(particledata[6][broj],particlecharge,eta_det,recoVtx.Z());
	      particledata[8][broj]=eta_det;
	    }
	}// close loop  over acceptedParticleTypes_
      }// close loop on SC's
    }// closure of loop over truth particles

  int goodparent=1;
  int likelyid=particledata[4][0];
  for(unsigned int brojac=0;brojac<acceptedParticleTypes_.size();brojac++) {
    if(particledata[3][brojac]!=0.0) brojrazl++;
    if(likelyid!=particledata[4][brojac]) goodparent=-1;
  }
  
  if(goodparent==1 && likelyid!=0 && brojrazl==acceptedParticleTypes_.size()) { 
    // if goodparent and ..
    for(unsigned int bro=0;bro<acceptedParticleTypes_.size();bro++) {
      for(unsigned int tt=0;tt<3;tt++) 
	{
	  particledata[tt][brojrazl]+=particledata[tt][bro];
	}
      particledata[3][brojrazl]+=particledata[3][bro];
    }

    for(unsigned int ff=0;ff<3;ff++) {
      squaremomenta+=particledata[ff][brojrazl]*particledata[ff][brojrazl];
    }
    double dtofdet=(particledata[5][0]-particledata[5][1])*1.0E-9;
    double dtofsim=(particledata[7][0]-particledata[7][1]);
    double dtofdiff=dtofdet-dtofsim;
    double detad=particledata[8][0]-particledata[8][1];
    float ugh=sqrt(particledata[3][brojrazl]*particledata[3][brojrazl]-squaremomenta);
      h_mothertype_ -> Fill(likelyid);h_massofmother_->Fill(ugh);
      h_tdiffdet_->Fill(dtofdet);
      h_tdiffsim_ ->Fill(dtofsim);
      h_tdiffdetsim_->Fill(dtofdiff);
      h_dtofdet_zvtx_->Fill(recoVtx.Z(),dtofdet);
      h_dtofdet_detad_->Fill(detad,dtofdet);
      h_dtofdet_dtofsim_->Fill(dtofsim,dtofdet);
      h_dtofdiff_zvtx_->Fill(recoVtx.Z(),dtofdiff);
      h_dtofdiff_detad_->Fill(detad,dtofdiff);
  } // close of 'if goodparent and .. '
} // close the analyze() method 

// ------------ method called once each job just before starting event loop  ------------
void 
TimeAnalyzer::beginJob()
{
  edm::Service<TFileService> fs;
  TFileDirectory subDir=fs->mkdir("baseHistoDir");  
  


  // histograms need be booked in the beginJob, which is run only once at  the  beginning of execution
  //  h_nVtx_     = fs->make<TH1F>("h_nVtx","no. of primary vertices; num vertices reco",10,0.,10.);
  //  h_pType_    = fs->make<TH1F>("h_pType","truth particle type; truth particle type",80,-40.,40.);
  //  pTypeSel_ = fs->make<TH1F>("h_pTypeSel","truth particle type (selected); truth particle type",80,-40.,40.);
  //  h_nSCEE_    = fs->make<TH1F>("h_nSCEE","number superclusters in EE; num EE SC  ",100,0.,10.);
  //  h_nSCEB_    = fs->make<TH1F>("h_nSCEB","number superclusters in EB; num EB SC",100,0.,10.);
  h_masses_     = fs->make<TH1F>("h_mase","mass",100,0.50995e-3,0.51005e-3);
  //  h_pr_       = fs->make<TH1F>("h_pr","pseudorapidity",100,-10.,10.);
  h_pperp_ = fs->make<TH1F>("h_pperp","transverse momentum",100,0.,90.);
  h_eta_      = fs->make<TH1F>("h_eta","eta",100,-3.,3.);
  h_phi_      = fs->make<TH1F>("h_phi","phi",100,-3.5,3.5);
  //  h_SCstack_ = fs->make<THStack>("SCstack","superclusters total");
  h_eclusterE_ = fs->make<TH1F>("h_eclusterE","cluster energy, E",100,0.,500.);
  h_etaclusterE_ = fs->make<TH1F>("h_etaclusterE","eta E",100,-3.,3.);
  h_phiclusterE_ = fs->make<TH1F>("h_phiclusterE","phi E",100,-3.5,3.5);
  h_eclusterB_ = fs->make<TH1F>("h_eclusterB","cluster energy, B",100,0.,500.);
  h_etaclusterB_ = fs->make<TH1F>("h_etaclusterB","eta B",100,-3.,3.);
  h_phiclusterB_ = fs->make<TH1F>("h_phiclusterB","phi B",100,-3.5,3.5);
  h_eta_phi_  = fs->make<TH2F>("h_eta_phi","eta vs phi",100,-3.5,3.5,100,-10.,10.);
  h_etacstack_= fs->make<THStack>("h_etacstack","E&B cluster eta stack");
  h_phicstack_= fs->make<THStack>("h_phicstack","E&B cluster phi stack");
  h_ceta_phi_ = fs->make<TH2F>("h_ceta_phi","E&B cluster eta vs phi",100,3.5,3.5,100,-3.,3.);
  h_delta_e    = fs->make<TH1F>("h_delta","deltaE",100,0.,0.2);
  h_delta_b    = fs->make<TH1F>("h_delta","deltaB",100,0.,0.2);
  h_energies_ = fs->make<TH1F>("h_enegies","energies",100,0.,500.);
  h_ecstack_  = fs->make<THStack>("h_ecstack","E&B energy stack");
  h_massofmother_ = fs->make<TH1F>("h_massofmother","e+e- particle energy",100,0.,160.);
  h_mothertype_ = fs->make<TH1F>("h_mothertype_","type of mother",80,-40.,40.);
  h_ptotal_   = fs->make<TH1F>("h_ptotal","total momentum",100,0.0,2000000.0);
  h_tdiffdet_ = fs->make<TH1F>("h_tdiffdet","e-e+ tof difference in detector",100,-1.8E-9,1.8E-9);
  h_tdiffsim_ = fs->make<TH1F>("h_tdiffsim","e-e+ tof difference in simulation",100,-1.8E-9,1.8E-9);
  h_tdiffdetsim_ = fs->make<TH1F>("h_tdiffdetsim","e-e+ tof difference between detector and simulation",100,-1.8E-9,1.8E-9);
  h_dtofdet_zvtx_ = fs->make<TH2F>("h_dtofdet_zvtx",
"difference in tof in detector vs inital z coordinate;z_0;#Delta t_det [s]",100,-15.,15.,100,-0.7E-9,0.7E-9);
  h_dtofdet_detad_ = fs->make<TH2F>("h_dtofdet_detad",
"difference in tof in detector vs #Delta#eta_det;#Delta#eta_det;#Delta t_det [s]",100,-2.,2.,100,-0.7E-9,0.7E-9);
  h_dtofdet_dtofsim_ = fs->make<TH2F>("h_dtofdet_dtofsim",
"difference in tof in detector vs difference in tof in simulation;#Delta#t_sim;#Delta t_det [s]",100,-1.3E-9,1.3E-9,100,-0.7E-9,0.7E-9);
  h_dtofdiff_zvtx_ = fs->make<TH2F>("h_dtofdiff_zvtx",
"difference in tof between detector and simulation vs initial z coordinate;z_0;#Delta t_diff[s]",100,-15.,15.,100,-1.3E-9,1.3E-9);
  h_dtofdiff_detad_ = fs->make<TH2F>("h_dtofdiff_detad",
"difference in tof between detector and simulation vs #eta of detector;#eta_det;#Delta t_diff[s]",100,-2.,2.,100,-1.3E-9,1.3E-9);
  h_dtofsim_zvtx_ = fs->make<TH2F>("h_dtofsim_zvtx",
"difference in tof in simulation vs inital z coordinate;z_0;#Delta t_sim [s]",100,-15.,15.,100,-1.3E-9,1.3E-9);

}

// ------------ method called once each job just after ending the event loop  ------------
void 
TimeAnalyzer::endJob() 
{

  //h_SCstack_ -> Add(h_nSCEE_);
  //h_SCstack_ -> Add(h_nSCEB_);
  h_eta_phi_ -> SetOption("colz");
  h_etacstack_ -> Add(h_etaclusterE_); h_etacstack_ -> Add(h_etaclusterB_);
  h_phicstack_ -> Add(h_phiclusterB_); h_phicstack_ -> Add(h_phiclusterE_);
  h_ceta_phi_ -> SetOption("colz");
  h_ecstack_ -> Add(h_eclusterE_); h_ecstack_ -> Add(h_eclusterB_);
  h_dtofdet_zvtx_->SetOption("colz"); h_dtofdet_detad_->SetOption("colz");
  h_dtofdet_dtofsim_->SetOption("colz");
  h_dtofdiff_zvtx_->SetOption("colz"); h_dtofdiff_detad_->SetOption("colz");

}

// ------------ method called when starting to processes a run  ------------
/*
  void 
  TimeAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method called when ending the processing of a run  ------------
/*
  void 
  TimeAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
  void 
  TimeAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
  void 
  TimeAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TimeAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TimeAnalyzer);
