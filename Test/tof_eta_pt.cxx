#include <iostream>
#include <cstdlib>
#include "TF1.h"
#include "TFile.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TH1F.h"
#include "TROOT.h"
#include "fun.cxx"
#include "TSystem.h"

using namespace std;
using namespace TMath;





Double_t tof_eta_pt( Double_t *eta, Double_t *par )
{
    Double_t tmomentum=par[0];Double_t zcoord=par[1];
    Double_t natcharge=par[2];
    return dtofcn_pdata_(tmomentum,natcharge,*eta,zcoord);
}

void tof_eta_pt()
{
  gROOT->LoadMacro("fun.cxx+");

    TCanvas *c1=new TCanvas("c1","asdfaksdfj",600,400);
    TLegend *legend=new TLegend(0.6,0.7,0.89,0.89);
    TF1 *f1 = new TF1( "p1",tof_eta_pt, 0.01,3.,3);
    f1->SetParameters(0.75,0.0,1.0);f1->SetLineColor(42);
    f1->Draw();f1->GetHistogram()->GetXaxis()->SetTitle("#eta of particle");f1->GetHistogram()->GetYaxis()->SetTitle("#Delta t [s]");
    f1->SetMinimum(1.0E-14);f1->SetMaximum(10.0);
    TF1 *f2 = new TF1( "p2",tof_eta_pt, 0.01,3.,3);
    f2->SetParameters(10.0,0.0,1.0);f2->SetLineColor(13);
    f2->Draw("SAME");
    TF1 *f3 = new TF1( "p3",tof_eta_pt, 0.01,3.,3);
    f3->SetParameters(100.0,0.0,1.0);f3->SetLineColor(33);
    f3->Draw("SAME");
    gPad->SetLogy();
    c1->Draw();
    legend->SetHeader("z_0=0.00m");
    legend->AddEntry(f1,"p_t=0.75GeV","l");
    legend->AddEntry(f2,"p_t=10.0GeV","l");
    legend->AddEntry(f3,"p_t=100.0GeV","l");
    legend->Draw();
}
