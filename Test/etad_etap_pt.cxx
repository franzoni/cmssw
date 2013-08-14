#include <iostream>
#include <cstdlib>
#include "TF1.h"
#include "TFile.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TH1F.h"

#define B 3.8
#define BarrelR 1.3
#define Zhalflength 3.5

using namespace std;
using namespace TMath;

Double_t etad_etap_pt( Double_t *eta, Double_t *par )
{
    Double_t value=42.0;Double_t tmomentum=par[0];Double_t zcoord=par[1];
    Double_t natcharge=par[2];Double_t invmass=par[3]; Double_t theta=2*ATan(Exp(-(*eta)));
    Double_t relr=tmomentum*(1.0E9)/(C()*natcharge*B);
    Double_t Tfinal=ACos(1-0.5*Power(BarrelR/relr,2));
    Double_t neutral_t=BarrelR/(Sin(theta)*C());
    Double_t neutral_t_e=(Zhalflength-zcoord)/(C()*Cos(theta));
    Double_t eta_n=-Log(Tan(0.5*ATan(BarrelR/(C()*Cos(theta)*neutral_t+zcoord))));
    Double_t Tz1=(Zhalflength-zcoord)*natcharge*1.60217657*B*Tan(theta)/(tmomentum*5.344286);
    Double_t deltaeta=-Log(Tan(0.5*ATan(BarrelR/(relr*Tfinal/Tan(theta)+zcoord))))-eta_n;
    if(neutral_t>neutral_t_e) neutral_t=neutral_t_e;
    if((*eta)>=0.0 && Abs(Tfinal)>Abs(Tz1)) {Tfinal=Tz1;
	eta_n=-Log(Tan(0.5*ATan(BarrelR/(C()*Cos(theta)*neutral_t+zcoord))));
       	deltaeta=-Log(Tan(0.5*ATan(Sqrt(Power(relr*(1-Cos(Tfinal)),2)+Power(relr*Sin(Tfinal),2))/Zhalflength)))-eta_n;
    }
    return deltaeta;
}


void etad_etap_pt()
{
    TCanvas *c1=new TCanvas("c1","asdfaksdfj",600,400);
    TLegend *legend=new TLegend(0.6,0.7,0.89,0.89);
    TF1 *f1 = new TF1( "pt1",etad_etap_pt, 0.01,3.,4);
    f1->SetParameters(0.75,0.00,1.0,9.1E-31);f1->SetLineColor(42);
    f1->Draw();
    f1->GetHistogram()->GetXaxis()->SetTitle("#eta of particle");
    f1->GetHistogram()->GetYaxis()->SetTitle("#Delta#eta of detector");
    f1->SetMinimum(1.0E-7);
    TF1 *f2 = new TF1( "pt2",etad_etap_pt, 0.01,3.,4);
    f2->SetParameters(10.0,0.00,1.0,9.1E-31);f2->SetLineColor(13);
    f2->Draw("SAME");
    TF1 *f3 = new TF1( "pt3",etad_etap_pt, 0.01,3.,4);
    f3->SetParameters(100.0,0.00,1.0,9.1E-31);f3->SetLineColor(33);
    f3->Draw("SAME");
//    gPad->SetLogy();
    c1->Draw();
    legend->SetHeader("z_0=0.00m");
    legend->AddEntry(f1,"p_t=0.8GeV","l");
    legend->AddEntry(f2,"p_t=10.0GeV","l");
    legend->AddEntry(f3,"p_t=100.0GeV","l");
    legend->Draw();
}

