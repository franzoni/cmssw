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

Double_t tof_pt_etap( Double_t *pt, Double_t *par )
{
    Double_t etap=par[0];Double_t zcoord=par[1];
    Double_t natcharge=par[2];              
    return dtofcn_pdata_(*pt,natcharge,etap,zcoord);
}

void tof_pt_etap()
{
    TCanvas *c1=new TCanvas("c1","asdfaksdfj",600,400);
    TLegend *legend=new TLegend(0.6,0.7,0.89,0.89);
    TF1 *f1 = new TF1( "p1",tof_pt_etap, 0.75,50.,3);
    f1->SetParameters(0.0,0.,1.0);f1->SetLineColor(42);
    f1->Draw();f1->GetHistogram()->GetXaxis()->SetTitle("p_t [GeV]");f1->GetHistogram()->GetYaxis()->SetTitle("#Delta t [s]");
    f1->SetMinimum(1.0E-15);f1->SetMaximum(1.0E-7);
    TF1 *f2 = new TF1( "p2",tof_pt_etap, 0.75,50.,3);
    f2->SetParameters(1.0,0.,1.0);f2->SetLineColor(13);
    f2->Draw("SAME");
    TF1 *f3 = new TF1( "p3",tof_pt_etap, 0.75,50.,3);
    f3->SetParameters(1.57,0.,1.0);f3->SetLineColor(33);
    f3->Draw("SAME");
//    gPad->SetLogx();
    c1->Draw();
    legend->SetHeader("z=0.00m");
    legend->AddEntry(f1,"#eta_p=0.00","l");
    legend->AddEntry(f2,"#eta_p=1.00","l");
    legend->AddEntry(f3,"#eta_p=1.57","l");
    legend->Draw();
}
