#include <iostream>
#include <cstdlib>
#include "TF1.h"
#include "TFile.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TH1F.h"
#include "fun.cxx"

#define B 3.8
#define BarrelR 1.3
#define Zhalflength 3.5

using namespace std;
using namespace TMath;

Double_t tof_pt_etad( Double_t *pt, Double_t *par )
{
    Double_t value=42.0;Double_t etad=par[0];Double_t zcoord=par[1];
    Double_t natcharge=par[2];
//    return dtofcn_ddata_(*pt,natcharge,etad,zcoord);
return r_etad_(etad);
}

void tof_pt_etad()
{
    TCanvas *c1=new TCanvas("c1","asdfaksdfj",600,400);
    TLegend *legend=new TLegend(0.6,0.7,0.89,0.89);
    TF1 *f1 = new TF1( "pt1",tof_pt_etad, 0.01,3.,3);
    f1->SetParameters(0.0,0.0,1.0);f1->SetLineColor(42);
    f1->Draw();f1->GetHistogram()->GetXaxis()->SetTitle("p_t");f1->GetHistogram()->GetYaxis()->SetTitle("#Delta t [s]");
    f1->GetHistogram()->GetXaxis()->SetTitle("p_t");
    f1->GetHistogram()->GetYaxis()->SetTitle("#Delta t [s]");
    TF1 *f2 = new TF1( "pt1",tof_pt_etad, 0.01,3.,3);
    f2->SetParameters(1.0,0.0,1.0);f2->SetLineColor(13);
    f2->Draw("SAME");
    TF1 *f3 = new TF1( "pt3",tof_pt_etad, 0.01,3.,3);
    f3->SetParameters(1.57,0.0,1.0);f3->SetLineColor(33);
    f3->Draw("SAME");
    TF1 *f4 = new TF1( "pt4",tof_pt_etad, 0.01,3.,3);
    f4->SetParameters(2.5,0.0,1.0);f4->SetLineColor(66);
    f4->Draw("SAME");
//    gPad->SetLogy();
    c1->Draw();
    legend->SetHeader("z_0=0.0m");
    legend->AddEntry(f1,"#eta_d=0.00","l");
    legend->AddEntry(f2,"#eta_d=1.0","l");
    legend->AddEntry(f3,"#eta_d=1.57","l");
    legend->AddEntry(f4,"#eta_d=2.5","l");
    legend->Draw();
}

