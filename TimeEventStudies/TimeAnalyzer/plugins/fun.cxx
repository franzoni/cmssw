#define B 3.8
#define BarrelR 1.290
#define Zhalflength 3.170

#include "TMath.h"
using namespace TMath;

Double_t rc_(Double_t pt_, Double_t charge_natunits_){
  Double_t radius=0.0;
  if((charge_natunits_)!=0.0) radius=(pt_)*(1.0E9)/(TMath::C()*(charge_natunits_)*B);
  return radius;
}

Double_t theta_eta_(Double_t eta_){
  return 2*TMath::ATan(TMath::Exp(-(eta_)));
}

Double_t z_etad_(Double_t eta_){
  Double_t barrel_z=BarrelR/TMath::Tan(theta_eta_(eta_));
  if(barrel_z>Zhalflength)
    return Zhalflength;
  else
    return barrel_z;
}

Double_t r_etad_(Double_t eta_){
  double endcap_r = BarrelR+1.0;
  if(TMath::Abs(eta_)>1.5) endcap_r=Zhalflength*TMath::Tan(theta_eta_(eta_));
  if(endcap_r>BarrelR)
    return BarrelR;
  else
    return endcap_r;
}

Double_t theta_zr_(Double_t z_, Double_t r_){
  Double_t theta_value=Pi()*0.5;
  if((z_)!=0.0) theta_value=TMath::ATan((r_)/(z_));
  return theta_value;
}

Double_t ztravelled_etad_(Double_t eta_, Double_t zi_){
  return z_etad_(eta_)-(zi_);
}

Double_t tofn_pdata_(Double_t eta_, Double_t zi_){
  Double_t barrelhit=BarrelR/(Sin(theta_eta_(eta_))*TMath::C());
  Double_t endcaphit=(Zhalflength-(zi_))/(TMath::C()*TMath::Cos(theta_eta_(eta_)));
  if(endcaphit>barrelhit)
    return barrelhit;
  else
    return endcaphit;
}

Double_t helixfinalpar_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  Double_t barrelpar=ACos(1-0.5*Power(BarrelR/rc_(pt_,charge_natunits_),2));
  Double_t endcappar=(Zhalflength-(zi_))*(charge_natunits_)*1.60217657*B*TMath::Tan(theta_eta_(eta_))/((pt_)*5.344286);
  if(TMath::Abs(barrelpar)>TMath::Abs(endcappar)){
//cout<< "EE: " << endcappar<<endl;
return endcappar;}
  else {
//cout<< "EB: " << barrelpar<<endl;
    return barrelpar;}
}

Double_t tofc_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  return helixfinalpar_(pt_,charge_natunits_,eta_,zi_)*rc_(pt_,charge_natunits_)/(TMath::C()*Sin(theta_eta_(eta_)));
}


Double_t dtofcn_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  return tofc_pdata_(pt_,charge_natunits_,eta_,zi_)-tofn_pdata_(eta_,zi_);
}

Double_t zofimpactn_(Double_t eta_, Double_t zi_){
  Double_t zn=(zi_)+BarrelR/(TMath::Tan(theta_eta_(eta_)));
  if(zn>Zhalflength)
    return Zhalflength;
  else if(zn<-Zhalflength) return -Zhalflength;
  else return zn;
}

Double_t zofimpactc_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  Double_t zc=(zi_)+rc_(pt_,charge_natunits_)*helixfinalpar_(pt_,charge_natunits_,eta_,zi_)/TMath::Tan(theta_eta_(eta_));
  return zc;
}

Double_t rofimpactn_(Double_t eta_, Double_t zi_){
  Double_t rn=(Zhalflength-(zi_))*TMath::Tan(theta_eta_(eta_));
  if(rn>BarrelR) return BarrelR;
  else return rn;
}

Double_t rofimpactc_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
//double radius = rc_(pt_,charge_natunits_);
//double parameter = helixfinalpar_(pt_,charge_natunits_,eta_,zi_);
//cout<<"r: " << radius << endl;
//cout << "par: " << parameter << endl;


  Double_t rc=rc_(pt_,charge_natunits_)*Sqrt(2-2*TMath::Cos(helixfinalpar_(pt_,charge_natunits_,eta_,zi_)));
//	cout << "rc: " << rc << endl;
  if(rc>BarrelR) {/*cout << "pippone" << endl;*/return BarrelR;}
  else return rc;
}

Double_t eta_theta_(Double_t theta_){
  return -Log(TMath::Tan(0.5*theta_));
}

Double_t eta_zr_(Double_t zi_, Double_t ri_){
  return eta_theta_(TMath::ATan((ri_)/(zi_)));
}

Double_t etan_pdata_(Double_t eta_, Double_t zi_){
  return eta_zr_(zofimpactn_(eta_,zi_),rofimpactn_(eta_,zi_));
}

Double_t etac_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  return eta_zr_(zofimpactc_(pt_,charge_natunits_,eta_,zi_),rofimpactc_(pt_,charge_natunits_,eta_,zi_));
}

Double_t deta_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  return etac_pdata_(pt_,charge_natunits_,eta_,zi_)-etan_pdata_(eta_,zi_);
}

Double_t tofn_ddata_(Double_t eta_, Double_t zi_){
  Double_t barrelhit=BarrelR/(TMath::C()*Sin(theta_zr_(ztravelled_etad_(eta_,zi_),BarrelR)));
  Double_t endcaphit=(Zhalflength-(zi_))/(TMath::C()*TMath::Cos(theta_zr_(ztravelled_etad_(eta_,zi_),r_etad_(eta_))));
  if(barrelhit>endcaphit) return endcaphit;
  else return barrelhit;
}

Double_t tofc_ddata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  Double_t thetap=theta_zr_(ztravelled_etad_(eta_,zi_),r_etad_(eta_));
  return helixfinalpar_(pt_,charge_natunits_,eta_theta_(thetap),zi_)*rc_(pt_,charge_natunits_)/(TMath::C()*Sin(thetap));
  
}

Double_t dtofcn_ddata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  return tofc_ddata_(pt_,charge_natunits_,eta_,zi_)-tofn_ddata_(eta_,zi_);
}

Double_t thetan_pdata_(Double_t eta_,Double_t zi_){
  return theta_eta_(etan_pdata_(eta_,zi_));
}

Double_t thetac_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  return theta_eta_(etac_pdata_(pt_,charge_natunits_,eta_,zi_));
}

Double_t dtheta_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_){
  return thetac_pdata_(pt_,charge_natunits_,eta_,zi_)-thetan_pdata_(eta_,zi_);
}

