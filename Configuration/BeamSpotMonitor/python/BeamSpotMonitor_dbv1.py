# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --process BeamSpotMonitor -s USER:Configuration/BeamSpotMonitor/CfiFile_cfi.BeamSpotMonitor --conditions auto:run1_data --data --python BeamSpotMonitor.py --no_exec --filein filelist:step1_dasquery.log --lumiToProcess step1_lumiRanges.log --customise_command=process.TFileService=cms.Service("TFileService",fileName = cms.string("BeamSpotMonitor_dbv1.root"),closeFileFast = cms.untracked.bool(True)) -n 500000 --no_output --python_filename=BeamSpotMonitor_dbv1.py
import FWCore.ParameterSet.Config as cms

process = cms.Process('BeamSpotMonitor')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.BeamSpotMonitor.CfiFile_cfi')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(500000)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring('/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/08AB2AA5-9C33-E211-8EFE-00261894392F.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/08B8D682-9C33-E211-BCBC-003048FFCBB0.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/186109A1-9C33-E211-815B-003048FFD728.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/1C4DF27C-9C33-E211-86FB-002618943807.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/1E42C011-9D33-E211-9747-003048678E92.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/20892ECE-9C33-E211-A370-002618943869.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/228EB02C-9C33-E211-92E0-002618943951.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/26049D9D-9C33-E211-B911-003048FFCB6A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/261E20C4-9C33-E211-8A76-0026189437FE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/2A63BB48-9D33-E211-9825-002618943869.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/2A678846-9C33-E211-85FC-0026189438B1.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/2ADF2397-9C33-E211-A839-00261894394F.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/2C14B3CA-9D33-E211-94F4-002618943809.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/3238663F-9C33-E211-8407-002618943833.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/360E9BFD-9C33-E211-B73F-0026189437EB.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/3A10FB74-9C33-E211-96FE-003048FFD756.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/3ADE22FC-9C33-E211-8E03-002590593872.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/3AE33A02-9D33-E211-A7FA-002618943867.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/3C047866-9C33-E211-B1E8-00261894397E.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/4477208E-9C33-E211-B0AA-002354EF3BCE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/464EE3B5-9C33-E211-9E4D-0018F3D0968A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/486C5790-9C33-E211-8E62-002618943843.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/5423D516-9E33-E211-93A0-002618943809.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/5AA79B7C-9C33-E211-AB6A-0026189437FD.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/5E4F7B68-9D33-E211-9737-00261894397F.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/5E6DF9E5-9C33-E211-82B4-002618943969.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/5EAF3BE9-9C33-E211-8D23-002618943969.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/62288AD7-9C33-E211-B3AF-003048FFCBFC.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/709DF0CE-9D33-E211-9BC1-0026189437F8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/78D43C33-9F33-E211-B345-0025905938A4.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/7A6B29A6-9C33-E211-A3AA-00261894388F.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/84842C07-9D33-E211-9916-00261894386E.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/8879BFF8-9C33-E211-AB26-0026189437FE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/8A0F7C72-9C33-E211-A1F7-002618943874.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/8C7E5B81-9C33-E211-A870-00261894389D.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/94D324D6-9E33-E211-84BE-0026189437F8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/968CC134-9D33-E211-B0D3-00261894386D.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/969EA66F-9D33-E211-A909-00261894397F.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/9848AA1F-9D33-E211-93FC-00261894386D.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/9EB47BB4-9C33-E211-8F40-003048678B5E.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/A037D8AE-9D33-E211-A314-0026189437F8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/A4AA8A90-9C33-E211-B377-002618943810.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/B084EB4E-9C33-E211-941D-00261894380B.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/B8063011-9D33-E211-AD67-002618943857.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/B82BBE59-9C33-E211-9D75-002618943972.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/BAAEFC63-9C33-E211-B194-0026189438FC.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/C07D64A4-9C33-E211-88ED-002618943858.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/C22B894D-9C33-E211-A48F-0026189438B5.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/C26394BE-9C33-E211-A5D6-00261894383F.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/CC101B54-9C33-E211-9FA1-00261894397D.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/CEEF8986-9C33-E211-9B05-003048678B8E.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/D4100804-9D33-E211-A441-002618943867.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/D4DA60E6-9C33-E211-B120-002618943935.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/D67CB7D7-9C33-E211-8977-003048FFCB8C.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/D85A75FC-9D33-E211-B2CC-0026189437EB.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/E4D054F1-9C33-E211-874D-00261894386E.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/E82731AA-9D33-E211-A7FE-00261894386D.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/E88F5E9F-9F33-E211-81E5-0025905938A4.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/EA7D0895-9C33-E211-9481-003048FFCB96.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/EE0302CB-9C33-E211-9DD8-001A92971AA8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/F002A185-9C33-E211-8316-002618943857.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/F6C712B2-9C33-E211-AE45-002618943858.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/FADB41EC-9D33-E211-88A7-0026189437EB.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/207/454/00000/FC95EF5B-9C33-E211-889B-0026189438D4.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/0603DDF8-903D-E211-A48C-001A92971B8C.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/1092BB91-8F3D-E211-A2DC-0025905964C2.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/12CF48A2-8F3D-E211-AB74-0018F3D096BE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/183153EB-973D-E211-99C9-00261894387E.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/188AFC48-923D-E211-99C1-0025905964A6.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/1E95A244-8F3D-E211-AD39-003048678A80.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/249C6CB2-903D-E211-A6BF-003048678FAE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/26ABB8DC-903D-E211-982A-003048678FAE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/36249757-903D-E211-830C-001A92811718.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/38941A9A-8F3D-E211-9948-001A92971BC8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/3A479E01-903D-E211-8FDD-002590596468.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/4428B960-8F3D-E211-B1BC-0026189438CB.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/4C544B26-903D-E211-B61E-003048678F74.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/58FF4633-8F3D-E211-9280-002590596484.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/5C6E9835-913D-E211-ACCB-001A92971B7C.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/66A7A3FC-8F3D-E211-950E-00261894388A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/6A8267D2-8F3D-E211-96E4-0025905938D4.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/7022D743-903D-E211-AB30-00261894391F.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/70CE3863-903D-E211-88FF-0018F3D096BE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/72E5836E-8F3D-E211-ABF5-003048678FF4.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/744A23B3-8F3D-E211-A947-0025905964C0.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/7A257255-903D-E211-B3D7-0018F3D0968A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/80A73760-923D-E211-A5B0-001A92971BDC.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/80BA4440-923D-E211-8A1F-0025905964A6.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/82911CB5-8F3D-E211-B34C-00259059642A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/8A00549D-8F3D-E211-8930-001A92810AB2.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/8CA861E4-903D-E211-9005-001A92971B8C.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/8CDC0B11-903D-E211-909E-003048678FF8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/8E387E6A-933D-E211-A14D-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/94197E6A-933D-E211-804E-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/9A656A5D-8F3D-E211-AA31-00304867BFBC.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/AA0DF05F-903D-E211-B443-003048678FFA.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/B80A592F-933D-E211-98BB-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/BC2DF6DB-903D-E211-8F72-003048678FAE.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/BE0DBA69-8F3D-E211-A227-0026189438B0.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/C2637E6A-933D-E211-A677-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/C4DAA937-903D-E211-BD1E-002618943831.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/C4FE864F-903D-E211-8EA1-002590596498.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/CCB6C39D-903D-E211-AD2B-003048678FFA.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/D2A260EE-923D-E211-BC4B-003048679244.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/D2F2E331-903D-E211-BD36-003048678F74.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/DA2D7312-923D-E211-90F8-001A92971BDC.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/E0380636-933D-E211-B493-003048FF9AC6.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/E0D74245-8F3D-E211-AFB2-003048678A6A.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/E0FD8E55-8F3D-E211-A163-003048678FF8.root', 
        '/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-PromptSkim-v1/000/208/307/00000/EE36B03C-903D-E211-80E5-0018F3D0960C.root'),
    lumisToProcess = cms.untracked.VLuminosityBlockRange("207454:1-207454:268435455", "208307:1-208307:268435455")
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('step2 nevts:500000'),
    name = cms.untracked.string('Applications')
)

# Output definition

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run1_data', '')

# Path and EndPath definitions
process.user_step = cms.Path(process.BeamSpotMonitor)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.user_step,process.endjob_step)


# Customisation from command line
process.TFileService=cms.Service("TFileService",fileName = cms.string("BeamSpotMonitor_dbv1.root"),closeFileFast = cms.untracked.bool(True))