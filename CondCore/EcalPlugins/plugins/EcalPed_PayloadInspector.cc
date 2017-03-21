#include "CondCore/Utilities/interface/PayloadInspectorModule.h"
#include "CondCore/Utilities/interface/PayloadInspector.h"
#include "CondCore/CondDB/interface/Time.h"

#include "CondFormats/EcalObjects/interface/EcalPedestals.h"

#include <memory>
#include <sstream>

namespace {

  class EcalPedMap : public cond::payloadInspector::Histogram2D<EcalPedestals> {
  public:
    EcalPedMap() : cond::payloadInspector::Histogram2D<EcalPedestals>( "ECAL pedestals", "ieta",170,-85,85,"iphi",360,0,360){
    //EcalPedMap() : cond::payloadInspector::Histogram2D<EcalPedestals>( "ECAL pedestals", "ieta",17,-8,7,"iphi",36,0,36){
      Base::setSingleIov( true );
    }

    bool fill( const std::vector<std::tuple<cond::Time_t,cond::Hash> >& iovs, std::vector<std::tuple<float,float,float> >& plotData ){
      for( auto iov : iovs ) {
	std::shared_ptr<EcalPedestals> payload = Base::fetchPayload( std::get<1>(iov) );
	
	for (int ieta=-85; ieta < 86; ieta++) {
	  for (int iphi=1; iphi < 361; iphi++) {
	//for (int ieta=-8; ieta < 7; ieta++) {
	//  for (int iphi=1; iphi < 36; iphi++) {
	    fillWithValue( ieta ,  iphi, ieta/iphi );
	  }
	}

	//if( payload.get() ){
	//
	//  if (!payload->barrelItems().size()) return false;
	//  for(int cellid = EBDetId::MIN_HASH;
	//      cellid < EBDetId::kSizeForDenseIndexing;
	//      ++cellid) {
	//    uint32_t rawid = EBDetId::unhashIndex(cellid);
	//    
	//    if (payload->find(rawid) == payload->end()) continue;
	//    if (!(*payload)[rawid].mean_x12 && !(*payload)[rawid].rms_x12) continue;
	//    
	//    fillWithValue( (EBDetId(rawid)).ieta() ,  (EBDetId(rawid)).iphi(), (*payload)[rawid].mean_x12 );
	//
	//  }
	//}

      }
      return true;
    }

  };

}

PAYLOAD_INSPECTOR_MODULE( EcalPed ){
  PAYLOAD_INSPECTOR_CLASS( EcalPedMap );
}
