#define B 3.8
#define BarrelR 1.290+0.079
#define Zhalflength 3.170+0.079

#include "TMath.h"
using namespace TMath;


Double_t rc_(Double_t pt_, Double_t charge_natunits_);
Double_t theta_eta_(Double_t eta_);
Double_t z_etad_(Double_t eta_);
Double_t r_etad_(Double_t eta_);
Double_t theta_zr_(Double_t z_, Double_t r_);
Double_t ztravelled_etad_(Double_t eta_, Double_t zi_);
Double_t tofn_pdata_(Double_t eta_, Double_t zi_);
Double_t helixfinalpar_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t tofc_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t dtofcn_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t zofimpactn_(Double_t eta_, Double_t zi_);
Double_t zofimpactc_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t rofimpactn_(Double_t eta_, Double_t zi_);
Double_t rofimpactc_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t eta_theta_(Double_t theta_);
Double_t eta_zr_(Double_t zi_, Double_t ri_);
Double_t etan_pdata_(Double_t eta_, Double_t zi_);
Double_t etac_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t deta_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t tofn_ddata_(Double_t eta_, Double_t zi_);
Double_t tofc_ddata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t dtofcn_ddata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t thetan_pdata_(Double_t eta_,Double_t zi_);
Double_t thetac_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);
Double_t dtheta_pdata_(Double_t pt_, Double_t charge_natunits_, Double_t eta_, Double_t zi_);

