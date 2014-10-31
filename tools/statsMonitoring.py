#! /usr/bin/env python

# A bunch of clob variables

# Old Global Monitor
#gm_address="https://reqmon-dev02.cern.ch/reqmgr/monitorSvc/"
gm_address="https://vocms204.cern.ch/reqmgr/monitorSvc/"
couch_address="https://cmsweb.cern.ch/couchdb/reqmgr_workload_cache/"
req2dataset="https://cmsweb.cern.ch/reqmgr/reqMgr/outputDatasetsByRequestName/"
request_detail_address="https://cmsweb.cern.ch/reqmgr/view/showWorkload?requestName="
#das_host = 'https://cmsweb.cern.ch'
das_host = 'https://das.cern.ch/das'
runStats_address = 'https://cmsweb.cern.ch/couchdb/workloadsummary/_design/WorkloadSummary/_show/histogramByWorkflow/'
dbs3_url = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader/'


#-------------------------------------------------------------------------------
import shutil
import sys

req_version = (2,6)
cur_version = sys.version_info

if cur_version < req_version:
  print "At least Python 2.6 is required!"
  sys.exit(1)

#-------------------------------------------------------------------------------

import os
import httplib
import urllib2
import urllib
import time
import datetime
import commands
import re
from pprint import pprint,pformat
import multiprocessing
import itertools
import random
import json

from phedex import phedex,runningSites,custodials,atT2,atT3

# Collect all the requests which are in one of these stati which allow for 
priority_changable_stati=['new','assignment-approved']
#skippable_stati=[]
skippable_stati=["rejected", "aborted","failed","rejected-archived","aborted-archived","failed-archived"]
#complete_stati=["announced","closed-out","completed","rejected", "aborted","failed"]
complete_stati=["announced","rejected", "aborted","failed","normal-archived","aborted-archived","failed-archived"]

# Types of requests
request_types=['MonteCarlo',
               'MonteCarloFromGEN',
               'ReDigi',
               'ReReco',
               'Resubmission']

wma2reason = {'success':'success', # wma2reason by vincenzo spinoso!
    'failure':'failure',
    'Pending':'pending',
    'Running':'running',
    'cooloff':'cooloff',
    'pending':'queued',
    'inWMBS':'inWMBS',
    'total_jobs':'total_jobs',
    'inQueue' : 'inQueue'}

#-------------------------------------------------------------------------------  
# Needed for authentication

class X509CertAuth(httplib.HTTPSConnection):
    '''Class to authenticate via Grid Certificate'''
    def __init__(self, host, *args, **kwargs):
      key_file = None
      cert_file = None
  
      x509_path = os.getenv("X509_USER_PROXY", None)
      if x509_path and os.path.exists(x509_path):
        key_file = cert_file = x509_path
  
      if not key_file:
        x509_path = os.getenv("X509_USER_KEY", None)
        if x509_path and os.path.exists(x509_path):
          key_file = x509_path
  
      if not cert_file:
        x509_path = os.getenv("X509_USER_CERT", None)
        if x509_path and os.path.exists(x509_path):
          cert_file = x509_path
  
      if not key_file:
        x509_path = os.getenv("HOME") + "/.globus/userkey.pem"
        if os.path.exists(x509_path):
          key_file = x509_path
  
      if not cert_file:
        x509_path = os.getenv("HOME") + "/.globus/usercert.pem"
        if os.path.exists(x509_path):
          cert_file = x509_path
  
      if not key_file or not os.path.exists(key_file):
        print >>stderr, "No certificate private key file found"
        exit(1)
  
      if not cert_file or not os.path.exists(cert_file):
        print >>stderr, "No certificate public key file found"
        exit(1)
  
      httplib.HTTPSConnection.__init__(self,  host,key_file = key_file,cert_file = cert_file,**kwargs)

#-------------------------------------------------------------------------------

class X509CertOpen(urllib2.AbstractHTTPHandler):
    def default_open(self, req):
      return self.do_open(X509CertAuth, req)

#-------------------------------------------------------------------------------
def eval_wma_string(string):
    string=string.replace("null",'None')
    string=string.replace("true","True")
    string=string.replace("false","False")
    return eval(string)

#-------------------------------------------------------------------------------

def generic_get(url, do_eval=True):
    opener=urllib2.build_opener(X509CertOpen())  
    datareq = urllib2.Request(url)
    datareq.add_header('authenticated_wget', "The ultimate wgetter")  
#   print "Getting material from %s..." %url,
    requests_list_str=opener.open(datareq).read()  

    ret_val=requests_list_str
    #print requests_list_str
    if do_eval:
        ret_val=eval_wma_string(requests_list_str)
    return ret_val
#-------------------------------------------------------------------------------

def generic_post(url, data_input):

    data = json.dumps(data_input)
    opener = urllib2.build_opener(X509CertOpen())
    datareq = urllib2.Request(url, data, {"Content-type" : "application/json"})
    requests_list_str = opener.open(datareq).read()
    ret_val = requests_list_str

    return ret_val
#-------------------------------------------------------------------------------

def get_requests_list(pattern="", not_in_wmstats=False):

    if not_in_wmstats:
      return get_requests_list_old(pattern)
    
    opener=urllib2.build_opener(X509CertOpen())  
    url="https://cmsweb.cern.ch/wmstats/_design/WMStats/_view/requestByStatusAndType?stale=update_after"
    datareq = urllib2.Request(url)
    datareq.add_header('authenticated_wget', "The ultimate wgetter")  
    print "Getting the list of requests from %s..." %url,
    requests_list_str=opener.open(datareq).read()  
    print " Got it in %s Bytes"%len(requests_list_str)
    data = json.loads( requests_list_str )
    ## build backward compatibility
    req_list= map( lambda item : {"request_name" : item[0], "status" : item[1], "type" :item[2]}, map(lambda r : r['key'] , data['rows']))
  
    return req_list

def get_requests_list_old(pattern=""):
    opener=urllib2.build_opener(X509CertOpen())  
    url="%srequestmonitor"%gm_address
    if pattern!="":
      url="%srequests?name=%s" %(gm_address,pattern)
    datareq = urllib2.Request(url)
    datareq.add_header('authenticated_wget', "The ultimate wgetter")  
    print "Getting the list of requests from %s..." %url,
    requests_list_str=opener.open(datareq).read()  
    print " Got it in %s Bytes"%len(requests_list_str)
  
    return eval_wma_string(requests_list_str)

#------------------------------------------------------------------------------- 

def get_req_extras(req):
  opener=urllib2.build_opener(X509CertOpen())  
  req_name=req["request_name"]
  url="%s%s"%(couch_address,req_name)  
  datareq = urllib2.Request(url)  
  datareq.add_header('authenticated_wget', "The ultimate wgetter")  
  #print "Asking for extras %s" %url
  req_xtras_str=opener.open(datareq).read()  
  return eval_wma_string(req_xtras_str)

#------------------------------------------------------------------------------- 

def get_dataset_name(reqname):
  #print "getting dataset name for %s" % reqname
  opener=urllib2.build_opener(X509CertOpen())  
  url="%s%s"%(req2dataset,reqname)  
  datareq = urllib2.Request(url)  
  datareq.add_header('authenticated_wget', "The ultimate wgetter")  
  #print "Asking for dataset %s" %url
  datasets_str=opener.open(datareq).read()  
  #print "-->%s<--"%datasets_str
  dataset_list=eval_wma_string(datasets_str)
  dataset=''
  apossibleChoice=''

  def compareDS(s1, s2):
    t1=s1.split('/')[1:]
    t2=s2.split('/')[1:]
    if len(t1[1]) > len(t2[1]):
      #print t1,t2,True
      return 1
    else:
      #decision=t1[2] < t2[2]
      def tierP(t):
        tierPriority=[
                      'RECO',
                      'SIM-RECO',
                      'DIGI-RECO',
                      'AODSIM',
                      'AOD',
                      'SIM-RAW-RECO',
                      'GEN-SIM',
                      'RAW-RECO',
                      'USER',
                      'ALCARECO',
                      'DQM' ,
                      'DQMIO',
                      'MINIAOD',
                      'MINIAODSIM'
                      ]
        
        for (p,tier) in enumerate(tierPriority):
          if tier == t:
            #print t,p
            return p
        #print t
        return t
      p1=tierP(t1[2])
      p2=tierP(t2[2])
      decision=(p1> p2)
      #print t1,t2,decision
      return decision*2 -1
                                                                                                                                                  
  dataset_list.sort(cmp=compareDS)
  if len(dataset_list)==0:
    dataset='None Yet'
  else:
    dataset=dataset_list[0]
  if 'None-None' in dataset or 'None-' in dataset:
    dataset='None Yet'
  return dataset,dataset_list

  """
  def compareTier(t1, t2):
    tierPriority={'/AOD':1, #/AOD & /AODSIM
                  '-RECO' :2, #/RECO and /GEN*-RECO
                  '/DQM' : 3,
                  '/RAW-RECO' : 4,
                  '/USER' : 5,
                  '/ALCARECO' : 6}

  for dset in sorted(dataset_list): # this way the GEN-SIM-RECO will be after AOD and be picked up
    if 'DQM' in dset:
      apossibleChoice=dset
      continue
    if 'USER' in dset:
      apossibleChoice=dset
      continue
    if 'RAW-RECO' in dset or 'USER' in dset:
      apossibleChoice=dset
      continue
    if 'ALCARECO' in dset:
      apossibleChoice=dset
      continue
    
    dataset=dset
    if 'None-None' in dataset or 'None-' in dataset:
      dataset='None Yet'
  #and fallback to something that looks possible
  if not dataset and apossibleChoice:
    dataset=apossibleChoice
  return dataset
  """
  
#-------------------------------------------------------------------------------
# Thanks to Jean-Roch

def configsFromWorkload( workload ):
  if not 'request' in workload:
    return []
  if not 'schema' in workload['request']:
    return []
  schema = workload['request']['schema']
  res=[]
  if schema['RequestType'] == 'TaskChain':
    i=1
    while True:
      t='Task%s'%i
      if t not in schema:
        break
      if not 'ConfigCacheID' in schema[t]:
        break
      res.append(schema[t]['ConfigCacheID'])
      i+=1
    else:
      pass

  return res

def get_expected_events_by_output( request_name ):
  try:
    return get_expected_events_by_output_( request_name )
  except:
    print "something went wrong in estimating the expected by output. no breaking the update though"
    import traceback
    print traceback.format_exc()
    return {}

def get_expected_events_by_output_( request_name ):
  
  def get_item( i, d ):
    if type(d)!=dict: 
      return None
    if not d:
      return None
    if i in d: 
      return d[i]
    else:
      for (k,v) in d.items():
        r=get_item(i, v)
        if r: return r

  def unique( l ):
    rl = []
    for i in l:
      if not i in rl:
        rl.append(i)
    return rl
  
  def get_strings( d ):
    ## retrieve all leaves that are strings
    if type(d)!=dict or not d:
      return None
    ret=[]
    for (k,v) in d.items():
      if type(v) == str:
        ret.append(v)
      else:
        r=get_strings(v)
        if r:
          ret.extend(r)
    return ret

  dict_from_workload_local = getDictFromWorkload( request_name, attributes=['schema','dataTier',['subscriptions','dataset']])
  if not dict_from_workload_local:
    return {}

  schema = dict_from_workload_local['request']['schema']
    
  if schema['RequestType'] != 'TaskChain':
    return {}

  task_i=1
  task_map = {}
  while task_i:
    k='Task%d'%(task_i)
    task_i+=1
    if k in schema:
      task =schema[k]
      task_map[ task['TaskName']] = k
    else:
      break
    
  expectedEvents='ExpectedNumEvents'
  expectedOuputs='ExpectedOutputs'
  while not all(map( lambda d : expectedEvents in d.keys() and expectedOuputs in d.keys(), [ schema[t] for t in task_map.values()])):
    for (taskname,taski) in task_map.items():
      task = schema[taski]
      if not expectedEvents in task:
        if 'RequestNumEvents' in task:
          #print "from expected",taskname
          task[expectedEvents] = task['RequestNumEvents']
          if 'FilterEfficiency' in task:
            task[expectedEvents] *= task['FilterEfficiency']
        elif 'InputDataset' in task:
          rne=None
          ids = [task['InputDataset']]
          bwl = []
          rwl = []
          f= 1.
          if 'BlockWhitelist' in task:
            bwl = task['BlockWhitelist']
          if 'RunWhitelist' in task:
            rwl = task['RunWhitelist']
          if 'FilterEfficiency' in task:
            f = task['FilterEfficiency']
          task[expectedEvents] = get_expected_events_withinput(rne,ids,bwl,rwl,f)
        else:
          previous=task_map[ task['InputTask'] ]
          if expectedEvents in schema[ previous ]:
            #print "from previous",taskname, previous
            task[expectedEvents] = schema[ task_map[ task['InputTask'] ] ][expectedEvents]
            if 'FilterEfficiency' in task:
              task[expectedEvents] *= task['FilterEfficiency']
      if not expectedOuputs in task:
        what=get_item( taskname, dict_from_workload_local['tasks'] )
        #pprint.pprint( what)
        task[expectedOuputs] = get_strings( what['subscriptions'] )
        task['plenty'] = unique(filter(lambda s : '/' in s, get_strings( what['tree'] )))

  ##pprint( schema )
  
  expected_per_dataset={}
  for (taskname,taski) in task_map.items():           
    task = schema[taski]          
    for d in task[expectedOuputs]:
      expected_per_dataset[d] = task[expectedEvents]
      
  return expected_per_dataset

def get_expected_events(request_name):
    workload_info=generic_get(request_detail_address+request_name, False)
    #import os
    def getfield(line):
        line=line.replace("<br/>","").replace('\n','').replace(' ','')
        return line.split("=")[-1]

    filter_eff=1.
    rne=None
    ids=[]
    bwl=[]
    rwl=[]
    for line in workload_info.split('\n'):
        if 'request.schema.RequestNumEvents' in line or 'request.schema.RequestSizeEvents' in line:
            rne=eval(getfield(line)) # int or None
        if 'request.schema.InputDatasets' in line:
            ids=eval(getfield(line)) # list
        if 'request.schema.BlockWhitelist' in line:
            bwl=eval(getfield(line)) # list
        if 'request.schema.FilterEfficiency' in line:
            filter_eff=float(eval(getfield(line))) # float
        if 'request.schema.RunWhitelist' in line:
            rwl=eval(getfield(line))

    return get_expected_events_withinput(float(rne.replace("'","")),ids,bwl,rwl,filter_eff)
  
def get_expected_events_withdict(dict_from_workload):
  if 'RequestNumEvents' in dict_from_workload['request']['schema']:
    rne=dict_from_workload['request']['schema']['RequestNumEvents']
  elif 'RequestSizeEvents' in dict_from_workload['request']['schema']:
    rne=dict_from_workload['request']['schema']['RequestSizeEvents']
  elif 'Task1' in dict_from_workload['request']['schema'] and 'RequestNumEvents' in dict_from_workload['request']['schema']['Task1']:
    rne=dict_from_workload['request']['schema']['Task1']['RequestNumEvents']
  else:
    rne=None
    
  if 'FilterEfficiency' in dict_from_workload['request']['schema']:
    f=float(dict_from_workload['request']['schema']['FilterEfficiency'])
  elif 'Task1' in dict_from_workload['request']['schema'] and 'FilterEfficiency' in dict_from_workload['request']['schema']['Task1']:
    f=float(dict_from_workload['request']['schema']['Task1']['FilterEfficiency'])
  else:
    f=1.
    
  if 'InputDatasets' in dict_from_workload['request']['schema']:
    try:
      ids=dict_from_workload['request']['schema']['InputDatasets'].split(',')
    except:
      ids=dict_from_workload['request']['schema']['InputDatasets']
  elif 'Task1' in dict_from_workload['request']['schema'] and  'InputDataset' in dict_from_workload['request']['schema']['Task1']:
    try:
      ids=dict_from_workload['request']['schema']['Task1']['InputDataset'].split(',')
    except:
      ids=dict_from_workload['request']['schema']['Task1']['InputDataset']
  else:
    ids=[]

    

  if 'BlockWhitelist' in dict_from_workload['request']['schema']:
    try:
      bwl=dict_from_workload['request']['schema']['BlockWhitelist'].split(',')
    except:
      bwl=dict_from_workload['request']['schema']['BlockWhitelist']
  elif 'Task1' in dict_from_workload['request']['schema'] and  'BlockWhitelist' in dict_from_workload['request']['schema']['Task1']:
    try:
      bwl=dict_from_workload['request']['schema']['Task1']['BlockWhitelist'].split(',')
    except:
      bwl=dict_from_workload['request']['schema']['Task1']['BlockWhitelist']
  else:
    bwl=[]

  if 'RunWhitelist' in dict_from_workload['request']['schema']:
    try:
      rwl=dict_from_workload['request']['schema']['RunWhitelist'].split(',')
    except:
      rwl=dict_from_workload['request']['schema']['RunWhitelist']
  elif 'Task1' in dict_from_workload['request']['schema'] and 'RunWhitelist' in dict_from_workload['request']['schema']['Task1']:
    try:
      rwl=dict_from_workload['request']['schema']['Task1']['RunWhitelist'].split(',')
    except:
      rwl=dict_from_workload['request']['schema']['Task1']['RunWhitelist']
  else:
    rwl=[]
    
  return get_expected_events_withinput(rne,
                                       ids,
                                       bwl,
                                       rwl,
                                       f)

  
def get_expected_events_withinput(
  rne,
  ids,
  bwl,
  rwl,
  filter_eff):
    #print "Calucalating expected events", rne, ids, bwl, rwl, filter_eff
    #wrap up
    if rne=='None' or rne==None or rne==0:

        #from DBSAPI.dbsApi import DbsApi
        #dbsapi = DbsApi()
        s=0.
        for d in ids:
          if len(rwl):
            #rwlfordbs=' or '.join(map(lambda s : "run=%s"%s, rwl))
            #s+=eval(os.popen('dbs search --production --noheader  --query  "find sum(file.numevents) where dataset = %s and (%s)"'%(d,rwlfordbs)).read())
            #make sure this is going to be viable
            try:
                print "$sss %s"%(d)
                #blocks = dbsapi.listBlocks(str(d)) #old
                #comm = './das_client.py --query="block dataset=%s" --format=json --das-headers --limit=0'%(dataset)
                #data = commands.getoutput(comm)
                #blocks = json.loads(data)["data"]
                ret = generic_get(dbs3_url+"blocks?dataset=%s" %(d)) #returns blocks names
                blocks= ret
            except:
                print d,"does not exist, and therefore we cannot get expected events from it"
                blocks = None

            if blocks:
              for run in rwl:
                #q='dbs search --production --noheader  --query  "find sum(file.numevents) where dataset = %s and (run=%s)" '%(d,run)
                #q = './das_client.py --query="file dataset=%s run=%s | sum(file.nevents)" --format=json --das-headers --limit=0' %(d,run)
                #result = commands.getoutput(q)
                ret = generic_get(dbs3_url+"filesummaries?dataset=%s&run_num=%s" %(d, run)) #returns blocks names
                data = ret
                try:
                  #s+=eval(os.popen(q).read())
                  #s += int(data["data"]["result"]["value"])
                  s += int(data[0]["num_event"])
                except:
                  print d,"does not have event for",run
                  #import traceback
                  #print traceback.format_exc()
          else:
            #blocks = dbsapi.listBlocks(str(d)) #old
            #comm = './das_client.py --query="block dataset=%s" --format=json --das-headers --limit=0'%(d)
            #data = commands.getoutput(comm)
            ret = generic_get(dbs3_url+"blocks?dataset=%s" %(d)) #returns blocks names ????
            blocks = ret
            if len(bwl):
                ##we have a block white list in input
                for b in bwl:
                    if not '#' in b: continue
                    for bdbs in filter(lambda bl: bl["block_name"]==b, blocks):
                        block_data = generic_get(dbs3_url+"blocksummaries?block_name=%s" %(bdbs["block_name"].replace("#","%23"))) #encode # to HTML URL
                        s += block_data[0]["num_event"] #because [1] is about replica of block???
            else:
                for bdbs in blocks:
                    block_data = generic_get(dbs3_url+"blocksummaries?block_name=%s" %(bdbs["block_name"].replace("#","%23"))) #encode # to HTML URL
                    s += block_data[0]["num_event"]
        return s*filter_eff
      
        #work from input dbs and block white list
        if len(bwl):
            s=0.
            #print "from block white list"
            for b in bwl:
                if not '#' in b: #a block whitelist needs that
                  continue
                try:
                    #print "###: dbs search --production --noheader  --query  find block.numevents where block = %s"%(b)
                    #s+=eval(os.popen('dbs search --production --noheader  --query  "find block.numevents where block = %s"'%(b)).readline())
                    #q = './das_client.py --query="block block=%s | grep block.nevents" --format=json --das-headers --limit=0'%(b)
                    #result = commands.getoutput(q)
                    ret = generic_get(dbs3_url+"blocksummaries?block_name=%s" %(b.replace("#","%23"))) #encode # to HTML URL
                    data = ret
                    s += data[0]["num_event"]
                except:
                    print b,'does not have events'
            return s*filter_eff
        else:
            s=0.
            #print "from ds list"
            for d in ids:
                try:
                    #s+=eval(os.popen('dbs search --production --noheader  --query  "find sum(block.numevents) where dataset = %s"'%(d)).readline())
                    #q = './das_client.py --query="block dataset=%s | sum(block.nevents)" --format=json --das-headers --limit=0'%(d)
                    #result = commands.getoutput(q)
                    ret = generic_get(dbs3_url+"blocksummaries?dataset=%s" %(d))
                    data = ret
                    s += data[0]["num_event"]
                except:
                    print d,"does not have events"
            return s*filter_eff
    else:
        #use requested number
        #print "from requested number"
        return rne

#------------------------------------------------------------------------------- 

def prepIDs2ReqNames(prepIDs):
  req_list = get_requests_list()
  req_names_dict={}
  for prepID in prepIDs:
    this_id_names=[]
    matching_reqs = filter(lambda req: prepID in req["request_name"] ,req_list )
    matching_reqs_names = map(lambda req: req["request_name"],matching_reqs )
    for matching_req_name in matching_reqs_names:
      this_id_names.append(matching_req_name)
    req_names_dict[prepID]=this_id_names
  return req_names_dict

#------------------------------------------------------------------------------- 
# extract a campaign from a request
# typical name etorassa_EXO-Fall11_R4-01119_T1_UK_RAL_MSS_v1_120207_173750_3364
# after the first _ count 2 - and stop at _
def get_prep_id(request):
    req_name=request["request_name"]

    name = req_name
    while name.count('_')>=1:
        name = name.split('_',1)[-1]
        if name.count('-') ==2:
            (pwg,campaign,begin_withserial) = name.split('-')
            if len(pwg) == 3:
                if begin_withserial[0:5].isdigit():
                    serial = begin_withserial[0:5]
                    prep_id = '-'.join([ pwg, campaign, serial])
                    return prep_id
    return 'No-Prepid-Found'
"""
    spl = req_name.split("_")
    for (i_word,word) in enumerate( spl ):
        next_word=None
        if i_word!= len(spl)-1:
            next_word= spl[i_word+1]
            
        if len(word.split("-")[0]) !=3:
            continue
        ## abc-z
        if word.count("-") ==2:
            ## abc-y-z
            if not word.split("-")[-1].isdigit():
                continue
            ## abc-z-<n>
            if len(word.split("-")[-1]) != 5:
                continue
            ## abc-z-01234
            return word
        elif word.count("-") ==1 and next_word: 
            ## abc-y_<next>
            if next_word.count('-')!=1:
                continue
            ## abc-y_z-u
            if not next_word.split("-")[-1].isdigit():
                continue
            ## abc-y_z-<n>
            if len(next_word.split("-")[-1]) !=5:
                continue
            ## abc-y_z-01234
            return word+"_"+next_word
        else:
            continue

            
    return 'No-Prepid-Found'
"""
"""
    name = req_name
    if name.count('_')>=1:
        name = name.split('_',1)[-1]
        if name.count('-') ==2:
            (pwg,campaign,begin_withserial) = name.split('-')
            if len(pwg) == 3:
                if begin_withserial[0:5].isdigit():
                    serial = begin_withserial[0:5]
                    prep_id = '-'.join([ pwg, campaign, serial])
                    return prep_id

    return 'No-Prepid-Found'
"""
"""
  # is an ACDC request
  if "ACDC" in req_name:
    return "ACDC-ACDC-00000"
    
  chars_to_find=["-","-","_"]
  char_found=0
  prep_id=""
  for char in req_name[req_name.find("_"):]:
    prep_id+=char
    if char!=chars_to_find[char_found]:
      continue
    if char_found==2:
      prep_id=prep_id.strip("_")
      break
    char_found+=1
  return  prep_id
"""

#------------------------------------------------------------------------------- 


def timelist_to_str(timelist):
  (h,m,s)=map(int,timelist)[3:]
  return "%02d%02d%02d"%(h,m,s)
  
def datelist_to_str(datelist):
  year=str(datelist[0])[2:]
  month=str(datelist[1])
  if len(month)==1:
    month="0%s"%month
  day=str(datelist[2])
  if len(day)==1:
    day="0%s"%day
  datestr="%s%s%s"%(year,month,day)
  return datestr
  
def get_submission_date(reqname):
  #print "%s%s" %(request_detail_address,reqname)
  wflowdetails=generic_get("%s%s" %(request_detail_address,reqname),False )
  lines = wflowdetails.split("<br/>")
  try:
    dateline=filter(lambda line: "request.schema.RequestDate" in line,lines)[0]
    datelist_str = dateline.split("=")[1]
    datelist=map(str, eval(datelist_str))
    return datelist_to_str(datelist)
  except:
    return "000101"


#------------------------------------------------------------------------------- 

def get_running_days(raw_date): 
  try:
    now=datetime.datetime.now()  
    yy=int(raw_date[0:2])
    mm=int(raw_date[2:4])
    dd=int(raw_date[4:6])
    then=datetime.datetime(int("20%s"%yy),mm,dd,0,0,0)  
    return int((now-then).days)
  except:
    return -1
  
#------------------------------------------------------------------------------- 

def get_campaign_from_prepid(prepid):
  try:
    return prepid.split("-")[1]
  except:
    return "ByHand"

#-------------------------------------------------------------------------------   

def get_status_nevts_from_dbs(dataset):

  print "You Loose 10CHF antanas"
  
  undefined=(None,0,0)
  debug=False
  if dataset=='None Yet':
    return undefined
  if dataset=='?':
    return undefined
  
  if debug : print "Querying DBS"

  total_evts=0
  total_open=0

  if debug:    print "load"
  #from DBSAPI.dbsApi import DbsApi
  #dbsapi = DbsApi()
  if debug:    print "instance"
  if debug:    print "blocks"
  try:
    #blocks = dbsapi.listBlocks(str(dataset))
    #comm = './das_client.py --query="block dataset=%s" --format=json --das-headers --limit=0'%(dataset)
    #data = commands.getoutput(comm)
    ret = generic_get(dbs3_url+"blocks?dataset=%s&detail=true" %(dataset))
    blocks = ret
  except:
    print "Failed to get blocks for --",dataset,"--"
    import traceback
    print traceback.format_exc()
    blocks = []
    return undefined

  for b in blocks:
    if debug:    print b
    #if b['OpenForWriting'] == '0':
    #  total_evts+=int(b['NumberOfEvents'])
    #elif b['OpenForWriting'] == '1':
    #  total_open+=int(b['NumberOfEvents'])
    #b["block"] = filter(lambda bd : not 'replica' in bd, b["block"])
    #b["block"] = filter(lambda bd : 'nevents' in bd, b["block"])
    if b["open_for_writing"] == 0: #lame DAS format: block info in a single object in list ????
        ret = generic_get(dbs3_url+"blocksummaries?block_name=%s" %(b["block_name"].replace("#","%23")))
        data = ret
        total_evts+=data[0]["num_event"]
    elif b["open_for_writing"] == 1:
        ret = generic_get(dbs3_url+"blocksummaries?block_name=%s" %(b["block_name"].replace("#","%23")))
        data = ret
        total_open+=data[0]["num_event"]
  if debug:    print "done"
  
  """
  dbs_command='dbs search --production --noheader --query="find block,block.numevents where dataset like %s and block.status=0"'%dataset
  output = commands.getoutput(dbs_command)
  
  ##NO it is not true
  #if output=='':
  #  return undefined
  total_evts=0
  try:
    if debug: print "trying to sum",output
    for line in output.split("\n"):
      if not line: continue
      (block,n)=line.split()
      total_evts+=int(n)
      #total_evts=sum(map(int,output.split("\n")))
  except:
    print "failed to sum ",dataset
    return undefined

  dbs_command='dbs search --production --noheader --query="find block,block.numevents where dataset like %s and block.status=1"'%dataset
  output = commands.getoutput(dbs_command)

  total_open=0

  #print output
  try:
    if output!='':
      if debug: print "trying to sum open"
      for line in output.split("\n"):
        if not line : continue
        (block,n)=line.split()
        total_open+=int(n)
        #total_open=sum(map(int,output.split("\n")))
  except:
    print "failed to sum open ",dataset
    return undefined

  #print "executed %s and found %s events" %(dbs_command ,total_evts)
  """
  
  #getstatus='dbs search --production --noheader --query "find dataset.status where dataset = %s"'%dataset
  #getstatus = './das_client.py --query="status dataset=%s" --format=json --das-headers --limit=0'%(dataset)
  try:
    ret = generic_post(dbs3_url+"datasetlist", {"dataset":[dataset], "detail":True})
    result = json.loads(ret) #post method return data as string so we must load it
    if len(result) != 0 :
        status = str(result[0]["dataset_access_type"])
    else:
        status=None
  except:
    print "\n ERROR getting dataset status. return:%s"%(ret)
    raise Exception("  datasetlist POST data:\n%s \n\n results:\n%s"%({"dataset":[dataset], "detail":True}, ret))
    #print "Das glitch on status retrieval for",dataset
    #print "  query:\n%s"%(getstatus)
    #print result
    #return undefined

  if not status:
    status=None

  #print (status,total_evts,total_open)
  return (status,total_evts,total_open)
  
#-------------------------------------------------------------------------------  
# Fetch the priority after changing it
# this is done parsing the workload page
# https://cmsweb.cern.ch/reqmgr/view/showWorkload?requestName=casarsa_BPH-Summer12-00008_21_v3__120309_170117
def get_present_priority(req):
  workload_info_url=request_detail_address+req["request_name"]
  workload_info=generic_get(workload_info_url,do_eval=False)
  # Interpret the workload file, nicer would be as python object
  req_priority=-1
  for line in workload_info.split("\n"):      
    if "request.priority" in line:
      #print "********* %s" %line
      line=line.replace("<br/>","")      
      prio_as_string=line.split("=")[-1]
      prio_as_string=prio_as_string.replace("'","")
      #remove '
      req_priority = int(prio_as_string)
  return req_priority
      

#-------------------------------------------------------------------------------  

#------------------------------------------------------------------------------- 
def get_running_jobs(req):
  #stats_dict={}
  #for key in wma2reason:
    #reason_key=wma2reason[key]
    #quantity=0
    #if req.has_key(key):
      #quantity=req[key]
    #stats_dict[reason_key]=int(quantity)
  key="Running"
  nrunning = 0
  if req.has_key(key):
    nrunning = req[key]
  
  return nrunning

#------------------------------------------------------------------------------- 

def get_pending_jobs(req):  
  key = "Pending"
  bsubmitted=0
  if req.has_key(key):
    bsubmitted = req[key]
  return bsubmitted

#------------------------------------------------------------------------------- 

def get_all_jobs(req):
  key="running"
  all_jobs=0
  if req.has_key(key):
    all_jobs = req[key]
  return all_jobs

#------------------------------------------------------------------------------- 
def calc_eta(level,running_days):
  flevel=float(level)
  irunning_days=int(running_days)
  if flevel>=99.99:
    return 0
  elif flevel<=0.:
    return -1
  #print level
  #print running_days
  total_days=100.*irunning_days/flevel
  eta = total_days-running_days
  return round(eta+0.5)

#------------------------------------------------------------------------------- 

def getDictFromWorkload(req_name, attributes=['request','constraints']):

  dict_from_workload={}
  from TransformRequestIntoDict import TransformRequestIntoDict
  dict_from_workload=TransformRequestIntoDict( req_name, attributes, True )
  dontloopforever=0
  while dict_from_workload==None:
    print "The request",req_name,"does not have a workLoad ... which is a glitch"
    dict_from_workload=TransformRequestIntoDict( req_name, attributes, True )
    dontloopforever+=1
    if dontloopforever>10:
      print "\t\tI am lost trying to get the dict workLoad for\n\t\t",req_name
      break
  return dict_from_workload


numberofrequestnameprocessed=0
countOld=0
def parallel_test(arguments,force=False):
  DEBUGME=False
  global countOld
  req,old_useful_info = arguments
  try:
    if DEBUGME: print "+"
    global numberofrequestnameprocessed
    #print  "doing ",req["request_name"],numberofrequestnameprocessed
    numberofrequestnameprocessed+=1
    
    pdmv_request_dict={}    
    

    if DEBUGME: print "-"
    ##faking announced status
    if req["request_name"]=='etorassa_EWK-Summer12_DR53X-00089_T1_IT_CNAF_MSS_batch77res_v1__121009_233442_92':
      req["status"]='announced'
    if req["request_name"]=='etorassa_JME-Summer12-00060_batch1_v2__120209_133317_6868':
      req["status"]='announced'
    if req["request_name"]=='jbadillo_TOP-Summer12-00234_00073_v0__140124_154429_3541':
      req["status"]='announced'
    ##faking rejected status
    if req["request_name"]=='spinoso_SUS-Summer12pLHE-00001_4_v1_STEP0ATCERN_130914_172555_5537':
      req["status"]="rejected"

    if not "status" in req:
      ## this is garbage anyways
      return {}
    req_status=req["status"]

    if req_status in skippable_stati:
      return None
      #return {} ## return None so that you can remove the empty dict, without removing all failures, if ever

    # the name
    req_name=req["request_name"]
    pdmv_request_dict["pdmv_request_name"]=req_name

    phedexObj=None
    phedexObjInput=None
    
    #allowSkippingOnRandom=0.1
    allowSkippingOnRandom=None

    if DEBUGME: print "--"
    #transform the workload in a dictionnary for convenience , can also be made an object
    dict_from_workload={}


    # check if in the old and in complete_stati, just copy and go on
    matching_reqs=filter(lambda oldreq: oldreq['pdmv_request_name']==req_name ,old_useful_info)
    skewed=False
    deadWood=False
    if len(matching_reqs)==1:

      pdmv_request_dict=matching_reqs[0]
      if pdmv_request_dict['pdmv_completion_eta_in_DAS']<0 and req["status"].startswith('running'):        skewed=True
      if req["status"].startswith('running'):        skewed=True
      if req["status"] == 'completed': skewed=True
      if 'pdmv_expected_events' in pdmv_request_dict and pdmv_request_dict['pdmv_expected_events']==-1:        skewed=True
      if pdmv_request_dict['pdmv_status_in_DAS']=='?': skewed=True
      if pdmv_request_dict['pdmv_dataset_name']=='?' : skewed=True
      if pdmv_request_dict['pdmv_dataset_name']=='None Yet' and req["status"] in priority_changable_stati:      skewed=True
      if pdmv_request_dict['pdmv_evts_in_DAS']<0 : skewed=True
      if pdmv_request_dict['pdmv_evts_in_DAS']==0 and req["status"] in ['announced']: skewed=True
      if pdmv_request_dict['pdmv_status_in_DAS'] in [None,'PRODUCTION'] and req["status"] in ['announced','normal-archived']: skewed=True

      if pdmv_request_dict["pdmv_status_from_reqmngr"]!=req_status and req_status!="normal-archived":
        print "CHANGE OF STATUS, do something !"
        skewed=True
        
      if 'pdmv_monitor_time' in pdmv_request_dict:
        up=time.mktime(time.strptime(pdmv_request_dict['pdmv_monitor_time']))
        now=time.mktime(time.gmtime())
        deltaUpdate = (now-up) / (60. * 60. * 24.)
        ##this (with a small number) will create a huge blow to the updating
        ## Oct 5 : > 40
        ## Oct 6 : > 35
        ## Oct 7 : > 30
        ## Oct 9 : > 20
        ## OCt 11: > 10
        ## Oct 12: > 5 ## and stay like this
        if deltaUpdate > 10 and countOld<=100:
          print 'too long ago'
          skewed=True
          countOld+=1

      if not 'pdmv_monitor_time' in pdmv_request_dict:
        skewed=True
        
      ##known bad status
      for bad in []:#'JME-Summer12_DR53X-00098','JME-Summer12_DR53X-00097','vlimant_Run2012']:
        if bad in req_name:
          skewed=True
          break
        
      #if not 'pdmv_open_evts_in_DAS' in pdmv_request_dict or pdmv_request_dict['pdmv_open_evts_in_DAS']<0 : skewed=True

      #add that field after the fact
      if not 'pdmv_running_sites' in pdmv_request_dict:
        pdmv_request_dict['pdmv_running_sites']=[]

      ##needs to be used by user drives the need to T2/T3 field to be up to date
      needsToBeUsed=True
      notNeededByUSers=['GEN-SIM','GEN-RAW']
      for eachTier in notNeededByUSers:
        if pdmv_request_dict["pdmv_dataset_name"].endswith(eachTier):
          needsToBeUsed=False

      if 'pdmv_status_in_DAS' in pdmv_request_dict and not pdmv_request_dict['pdmv_status_in_DAS'] in ['VALID','PRODUCTION']:
        needsToBeUsed=False
        
      if not needsToBeUsed:
        print "not doing phedex call"

      noSites=True
      if 'pdmv_at_T2' in pdmv_request_dict and len(pdmv_request_dict['pdmv_at_T2']):
        noSites=False
      if 'pdmv_at_T3' in pdmv_request_dict and len(pdmv_request_dict['pdmv_at_T3']):
        noSites=False

      if not force:
        noSites=False
        
      if noSites and needsToBeUsed and (not 'pdmv_at_T2' in pdmv_request_dict or pdmv_request_dict['pdmv_at_T2']==[]):
        if not phedexObj:
          phedexObj=phedex(pdmv_request_dict["pdmv_dataset_name"])
        pdmv_request_dict['pdmv_at_T2']=atT2(phedexObj)
        #print "added",pdmv_request_dict['pdmv_at_T2']
      elif not 'pdmv_at_T2' in pdmv_request_dict:
        pdmv_request_dict['pdmv_at_T2']=[]

      if noSites and needsToBeUsed and (not 'pdmv_at_T3' in pdmv_request_dict or pdmv_request_dict['pdmv_at_T3']==[]):
        if not phedexObj:
          phedexObj=phedex(pdmv_request_dict["pdmv_dataset_name"])
        pdmv_request_dict['pdmv_at_T3']=atT3(phedexObj)
      elif not 'pdmv_at_T3' in pdmv_request_dict:
        pdmv_request_dict['pdmv_at_T3']=[]


      if 'pdmv_input_dataset' not in pdmv_request_dict:
        if not dict_from_workload: dict_from_workload=getDictFromWorkload(req_name)
        if not dict_from_workload: return {}
        if 'InputDatasets' in dict_from_workload['request']['schema'] and len(dict_from_workload['request']['schema']['InputDatasets']):
          pdmv_request_dict['pdmv_input_dataset'] = dict_from_workload['request']['schema']['InputDatasets'][0]
        else:
          pdmv_request_dict['pdmv_input_dataset'] = ''


      if not 'pdmv_custodial_sites' in pdmv_request_dict or pdmv_request_dict['pdmv_custodial_sites']==[]:
        if not phedexObj:
          phedexObj=phedex(pdmv_request_dict["pdmv_dataset_name"])
        pdmv_request_dict['pdmv_custodial_sites']=custodials(phedexObj)
        ## the problem with trying to assign custodial from the input dataset is that later on, it cannot be changed, and will probably be wrong downstream
        #if pdmv_request_dict['pdmv_custodial_sites']==[] and pdmv_request_dict['pdmv_input_dataset']!='':
        #  ## the ouput dataset might not even exists yet.
        #  if not phedexObjInput:
        #    phedexObjInput=phedex(pdmv_request_dict['pdmv_input_dataset'])
        #  pdmv_request_dict['pdmv_custodial_sites']=custodials(phedexObjInput)
          
        
      if not 'pdmv_open_evts_in_DAS' in pdmv_request_dict:
        pdmv_request_dict['pdmv_open_evts_in_DAS']=0
        

      if 'amaltaro' in req_name and ('type' in req and req['type'] == 'TaskChain'):
        skewed=False

      #needs to be put by hand once in all workflows
      if (pdmv_request_dict['pdmv_status_from_reqmngr'] in complete_stati) and ('pdmv_performance' not in pdmv_request_dict or pdmv_request_dict['pdmv_performance']=={}):
        print "skewed with no perf"
        from Performances import Performances
        pdmv_request_dict['pdmv_performance']=Performances(req_name)
        #print pdmv_request_dict['pdmv_performance']
        #pdmv_request_dict['pdmv_performance']={}

        
      ##this pulls in way too many requests
      #if (pdmv_request_dict['pdmv_status_from_reqmngr'] in complete_stati) and pdmv_request_dict['pdmv_completion_eta_in_DAS']<90:
      #  skewed=True

      # this is treated later on. was there only for transitionning
      ##if not 'pdmv_dataset_list' in pdmv_request_dict or pdmv_request_dict['pdmv_dataset_list']==[] or force:
      ##  dataset,dataset_list=get_dataset_name(req_name)
      ##  pdmv_request_dict['pdmv_dataset_list']=dataset_list
        
      if (pdmv_request_dict['pdmv_status_from_reqmngr'] in complete_stati) and not skewed and not force:
        print "** %s is there already"%req_name
        #print pdmv_request_dict['pdmv_performance']
        #print pdmv_request_dict['pdmv_at_T2']
        return pdmv_request_dict



      print req_name," is skewed ? ",skewed
      if allowSkippingOnRandom!=None and skewed and random.random()> allowSkippingOnRandom and not force:
        #print req_name,"is there already, needs updating, but skipping for now"
        return pdmv_request_dict

    #if needs to be added to the db since it is not present already
    else:
      decide=random.random()
      if allowSkippingOnRandom!=None and decide > allowSkippingOnRandom:
         #update only 1 out of 10
         print "Skipping new request",req_name,len(matching_reqs)
         return {}

    if len(matching_reqs)==1:
      print "Updating",req_name
    else:
      print "Processing",req_name

    if not 'pdmv_configs' in pdmv_request_dict or pdmv_request_dict['pdmv_configs'] ==[] :
      if not dict_from_workload: dict_from_workload=getDictFromWorkload(req_name)
      if not dict_from_workload: return {}
      pdmv_request_dict['pdmv_configs'] = configsFromWorkload( dict_from_workload )

    #dict_from_workload=getDictFromWorkload(req_name)
    #if not dict_from_workload:      return {}

    # assign the date
    ### JRout pdmv_request_dict["pdmv_submission_date"]=get_submission_date(req["request_name"])
    if not 'pdmv_submission_date' in pdmv_request_dict or not 'pdmv_submission_time' in pdmv_request_dict:
      ##load it on demand only
      if not dict_from_workload: dict_from_workload=getDictFromWorkload(req_name)
      if not dict_from_workload: return {}
      
      pdmv_request_dict["pdmv_submission_date"]=datelist_to_str(dict_from_workload['request']['schema']['RequestDate'])
      pdmv_request_dict["pdmv_submission_time"]=timelist_to_str(dict_from_workload['request']['schema']['RequestDate'])
      if DEBUGME: print "----"
      if  pdmv_request_dict["pdmv_submission_date"][:2] in ["11","12"]:
        print "Very old request "+req_name
        return {}


    if DEBUGME: print "-----"      
    ##put an update time in the json
    
    # the request itself!
    pdmv_request_dict["pdmv_request"]=req        
    
    # check the status
    req_status=req["status"]
    pdmv_request_dict["pdmv_status_from_reqmngr"]=req_status
    
    if req_status in priority_changable_stati:
      pdmv_request_dict["pdmv_status"]="ch_prio"
    else:
      pdmv_request_dict["pdmv_status"]="fix_prio"

    #request type
    pdmv_request_dict['pdmv_type']=req["type"]        
    if DEBUGME: print "------"      
    # number of running days
    if pdmv_request_dict["pdmv_status_from_reqmngr"].startswith('running'):
      #set only when the requests is in running mode, not anytime after
      pdmv_request_dict["pdmv_running_days"]=get_running_days(pdmv_request_dict["pdmv_submission_date"])
    elif not "pdmv_running_days" in pdmv_request_dict:
      pdmv_request_dict["pdmv_running_days"]=0

    if DEBUGME: print "-------"      
    # get the running jobs
    pdmv_request_dict["pdmv_all_jobs"]=get_all_jobs(req)        
        
    # get the running jobs
    pdmv_request_dict["pdmv_running_jobs"]=get_running_jobs(req)
    
    # get the jobs pending in the batch systems
    pdmv_request_dict["pdmv_pending_jobs"]=get_pending_jobs(req)
    
    # get Extras --> slow down---------------

    raw_expected_evts=None
    priority=-1
    # assign the campaign and the prepid guessing from the string, then try to get it from the extras
    if not dict_from_workload: dict_from_workload=getDictFromWorkload(req_name)
    if not dict_from_workload: return {}
    if 'PrepID' in dict_from_workload['request']['schema']:
      prep_id = dict_from_workload['request']['schema']['PrepID']
    else:
      prep_id='No-Prepid-Found'
    #prep_id=get_prep_id(req)
    pdmv_request_dict["pdmv_prep_id"]=prep_id
    campaign=get_campaign_from_prepid(prep_id)
    pdmv_request_dict["pdmv_campaign"]=campaign    
    req_extras={}


    # Priority
    ###JR out pdmv_request_dict["pdmv_priority"]=priority
    retrievePriority=False
    if not 'pdmv_priority' in pdmv_request_dict:
      retrievePriority=True
    if not 'pdmv_present_priority' in pdmv_request_dict:
      retrievePriority=True
    if pdmv_request_dict['pdmv_status_from_reqmngr'] in priority_changable_stati+['acquired','running','running-open','running-closed']:
      retrievePriority=True
    
    if retrievePriority:
      if not dict_from_workload: dict_from_workload=getDictFromWorkload(req_name)
      if not dict_from_workload: return {}
      
      pdmv_request_dict["pdmv_priority"]=dict_from_workload['request']['schema']['RequestPriority']
      if DEBUGME: print "----------"      
      # Present priority
      ###JR out pdmv_request_dict["pdmv_present_priority"]=get_present_priority(req)
      pdmv_request_dict["pdmv_present_priority"]=dict_from_workload['request']['priority']
    
    if DEBUGME: print "-----------"      
    #------------------------------------------
    
    # Query yet another service to get the das entry of the prepid
    ## try and reduce the number of calls to get_dataset_name url
    dataset_name="None Yet"
    dataset_list=[]
    if 'pdmv_dataset_name' in pdmv_request_dict:
      dataset_name=pdmv_request_dict["pdmv_dataset_name"]
      #print "Already know as",dataset_name
    makedsnquery=False
    if (not 'pdmv_dataset_name' in pdmv_request_dict):
      makedsnquery=True
    if 'pdmv_dataset_name' in pdmv_request_dict and (pdmv_request_dict["pdmv_dataset_name"] in ['?','None Yet'] or 'None-' in pdmv_request_dict["pdmv_dataset_name"] or '24Aug2012' in pdmv_request_dict["pdmv_dataset_name"]):
      makedsnquery=True

    if force:
      makedsnquery=True

    if req_status in priority_changable_stati:
      makedsnquery=False
            
    #print makedsnquery
    try:
      if makedsnquery:
        dataset_name,dataset_list=get_dataset_name(pdmv_request_dict["pdmv_request_name"])
    except:
      pass
      """
      try:
        if makedsnquery:
          dataset_name,dataset_list=get_dataset_name(pdmv_request_dict["pdmv_request_name"])
      except:
        print "Totally failed to get a dataset name for:",pdmv_request_dict["pdmv_request_name"]
        pass
      """
      pass
    
    pdmv_request_dict["pdmv_dataset_name"]=dataset_name
    pdmv_request_dict["pdmv_dataset_list"]=dataset_list

    deltaUpdate = 0
    ##remove an old field
    if 'pdmv_update_time' in pdmv_request_dict:
      pdmv_request_dict.pop('pdmv_update_time')

    if 'pdmv_monitor_time' in pdmv_request_dict:
      up=time.mktime(time.strptime(pdmv_request_dict['pdmv_monitor_time']))
      now=time.mktime(time.gmtime())
      deltaUpdate = (now-up) / (60. * 60. * 24.)
    else:
      pdmv_request_dict["pdmv_monitor_time"]=time.asctime()
      
    #if allowSkippingOnRandom!=None or random.random() > 0.0 or
    if deltaUpdate > 2. or DEBUGME or force or pdmv_request_dict['pdmv_status_from_reqmngr'].startswith('running') or skewed:
      #do the expensive procedure rarely or for request which have been update more than 2 days ago
      print "\tSumming for",req_name
      status,evts,openN=get_status_nevts_from_dbs(pdmv_request_dict["pdmv_dataset_name"])
      ## aggregate number of events for all output datasets
      pdmv_request_dict['pdmv_dataset_statuses'] = {}
      for other_ds in pdmv_request_dict['pdmv_dataset_list']:
        if other_ds == pdmv_request_dict["pdmv_dataset_name"]:
          other_status,other_evts,other_openN = status,evts,openN
        else:
          other_status,other_evts,other_openN = get_status_nevts_from_dbs( other_ds )
        pdmv_request_dict['pdmv_dataset_statuses'][other_ds] = {
          'pdmv_status_in_DAS' : other_status,
          'pdmv_evts_in_DAS' : other_evts,
          'pdmv_open_evts_in_DAS' : other_openN
          }
          
      if status:
        print "\t\tUpdating %s %s %s"%( status,evts,openN )
        pdmv_request_dict["pdmv_status_in_DAS"]=status
        pdmv_request_dict["pdmv_evts_in_DAS"]=evts
        pdmv_request_dict["pdmv_open_evts_in_DAS"]=openN
        ## add this only when the summing is done
      else:
        print "\t\tPassed %s %s %s"%( status,evts,openN )
        pass
      pdmv_request_dict["pdmv_monitor_time"]=time.asctime()
    else:
      print "\tSkipping summing for",req_name
      ## move the next line out to go over the "pass" above
    if not "pdmv_status_in_DAS" in pdmv_request_dict:
      pdmv_request_dict["pdmv_status_in_DAS"]=None
    if not "pdmv_evts_in_DAS" in pdmv_request_dict:
      pdmv_request_dict["pdmv_evts_in_DAS"]=0
    if not "pdmv_open_evts_in_DAS" in pdmv_request_dict:
      pdmv_request_dict["pdmv_open_evts_in_DAS"]=0


    if not 'pdmv_expected_events' in pdmv_request_dict:
      pdmv_request_dict['pdmv_expected_events']=-1

    if not 'pdmv_expected_events_per_ds' in pdmv_request_dict:
      pdmv_request_dict['pdmv_expected_events_per_ds'] = {}

    ## why having "expected events" not calculated if the output dataset has no status yet ?
    #to prevent stupid update from garbage requests announced or skewed but enrecoverable
    ##if ((pdmv_request_dict["pdmv_expected_events"]<0) or skewed) and pdmv_request_dict['pdmv_status_in_DAS']:
    if pdmv_request_dict["pdmv_expected_events"]<0 or (skewed and pdmv_request_dict['pdmv_status_in_DAS'] and not pdmv_request_dict['pdmv_status_in_DAS'] in ['DELETED','DEPRECATED'] and pdmv_request_dict["pdmv_expected_events"]<0) or force:
      print "Getting expected events"
      ## JR on Sept 25 removed <=0
      #if ((pdmv_request_dict["pdmv_expected_events"]<0) and pdmv_request_dict['pdmv_status_in_DAS']) or force:
      #if pdmv_request_dict["pdmv_expected_events"]<0: ## this will trigger a lot of queries on fuck up requests

      if not dict_from_workload: dict_from_workload=getDictFromWorkload(req_name)
      if not dict_from_workload: return {}
      
      raw_expected_evts=get_expected_events_withdict( dict_from_workload )
      if DEBUGME: print "--------"      
      #if DEBUGME: print "Expected are %s"%raw_expected_evts
    
      # get the expected number of evts    
      expected_evts=-1
      if raw_expected_evts==None or raw_expected_evts=='None':
        expected_evts=-1
      else:
        expected_evts=int(raw_expected_evts)
      if DEBUGME: print "---------"      
      pdmv_request_dict["pdmv_expected_events"]=expected_evts
      ## get an expected per output dataset if possible
      pdmv_request_dict['pdmv_expected_events_per_ds'] = get_expected_events_by_output( req_name )

      #print pdmv_request_dict["pdmv_expected_events"]

      
    completion=0
    if  pdmv_request_dict["pdmv_expected_events"]>0.:
      completion=100*(float(pdmv_request_dict["pdmv_evts_in_DAS"])+float(pdmv_request_dict["pdmv_open_evts_in_DAS"]))/pdmv_request_dict["pdmv_expected_events"]
    #pdmv_request_dict["pdmv_completion_in_DAS"]="%2.2f" %completion
    pdmv_request_dict["pdmv_completion_in_DAS"]=float("%2.2f" %completion)
    if DEBUGME: print "----------"      
    pdmv_request_dict["pdmv_completion_eta_in_DAS"]=calc_eta(pdmv_request_dict["pdmv_completion_in_DAS"],pdmv_request_dict["pdmv_running_days"])



    if not 'pdmv_running_sites' in pdmv_request_dict:
      pdmv_request_dict['pdmv_running_sites']=[]

    #find open blocks for running at sites
    if pdmv_request_dict['pdmv_status_from_reqmngr'].startswith('running'):
      if not phedexObj:
        phedexObj=phedex(pdmv_request_dict["pdmv_dataset_name"])
      pdmv_request_dict['pdmv_running_sites']=runningSites(phedexObj)

    if (not 'pdmv_custodial_sites' in pdmv_request_dict or pdmv_request_dict['pdmv_custodial_sites']==[]):
      pdmv_request_dict['pdmv_custodial_sites']=[]
      if pdmv_request_dict['pdmv_status_in_DAS']:
        if not phedexObj:
          phedexObj=phedex(pdmv_request_dict["pdmv_dataset_name"])
          pdmv_request_dict['pdmv_custodial_sites']=custodials(phedexObj)

      if pdmv_request_dict['pdmv_custodial_sites']==[]:
        ##try something new
        if not dict_from_workload: dict_from_workload=getDictFromWorkload(req_name)
        if not dict_from_workload:          return {}
        #print dict_from_workload['tasks']['StepOneProc']['constraints']
        taskNameInSchema='StepOneProc'
        try:
          if not taskNameInSchema in dict_from_workload['tasks']:
            taskNameInSchema='DataProcessing'
          sitesList=filter(lambda s : s.startswith('T1_'), dict_from_workload['tasks'][taskNameInSchema]['constraints']['sites']['whitelist'])
          pdmv_request_dict['pdmv_custodial_sites']=sitesList
        except:
          print "Could not get site white list for",req_name,taskNameInSchema

    needsToBeUsed=True
    notNeededByUSers=['GEN-SIM','GEN-RAW']
    for eachTier in notNeededByUSers:
      if pdmv_request_dict["pdmv_dataset_name"].endswith(eachTier):
        needsToBeUsed=False
                  
    noSites=True
    if 'pdmv_at_T2' in pdmv_request_dict and len(pdmv_request_dict['pdmv_at_T2']):
      #print len(pdmv_request_dict['pdmv_at_T2'])
      noSites=False
    if 'pdmv_at_T3' in pdmv_request_dict and len(pdmv_request_dict['pdmv_at_T3']):
      #print len(pdmv_request_dict['pdmv_at_T3'])
      noSites=False

    if noSites and needsToBeUsed and (not 'pdmv_at_T2' in pdmv_request_dict or pdmv_request_dict['pdmv_at_T2']==[]):
      if not phedexObj:
        phedexObj=phedex(pdmv_request_dict["pdmv_dataset_name"])
      pdmv_request_dict['pdmv_at_T2']=atT2(phedexObj)
      #print "setting sites to",pdmv_request_dict['pdmv_at_T2']
    elif not 'pdmv_at_T2' in pdmv_request_dict:
      #print "setting to no sites",noSites,needsToBeUsed
      pdmv_request_dict['pdmv_at_T2']=[]

    if noSites and needsToBeUsed and (not 'pdmv_at_T3' in pdmv_request_dict or pdmv_request_dict['pdmv_at_T3']==[]):
      if not phedexObj:
        phedexObj=phedex(pdmv_request_dict["pdmv_dataset_name"])
      pdmv_request_dict['pdmv_at_T3']=atT3(phedexObj)
    elif not 'pdmv_at_T3' in pdmv_request_dict:
      pdmv_request_dict['pdmv_at_T3']=[]

    #until we fix the certificate for couchDB access
    if (pdmv_request_dict['pdmv_status_from_reqmngr'] in complete_stati) and ('pdmv_performance' not in pdmv_request_dict or pdmv_request_dict['pdmv_performance']=={}):
      print "updating for perf"
      from Performances import Performances
      #print "Perf"
      pdmv_request_dict['pdmv_performance']=Performances(req_name)
    #else:
    #  print pdmv_request_dict['pdmv_performance']
    
    return pdmv_request_dict

  except:
    import traceback
    print req["request_name"],"IS A DEAD FAILING REQUEST"
    trf='traceback/traceback_%s.txt'%(req["request_name"])
    print trf
    tr=open(trf,'w')
    tr.write(traceback.format_exc())
    tr.close()
    
    ##could be failing on certificate issue and we truncate/loose all info of subsequent requests
    ## try to get info of a know request, just to fail on certificat for real, outside the try...
    ##if that fails, it's because of server or certificate, and will make the whole thing fail, rather than going on quietly
    from TransformRequestIntoDict import TransformRequestIntoDict
    #dict_from_workload=TransformRequestIntoDict( 'etorassa_EXO-Summer12_DR52X-00109_T1_US_FNAL_MSS_batch15_v1__120426_182026_2934' , ['request'], True )
    dict_from_workload=TransformRequestIntoDict( 'pdmvserv_HIG-Summer11pLHE-00079_00009_v0_STEP0ATCERN_131205_120245_8592' , ['request'], True )
    
    return {}

#------------------------------------------------------------------------------- 

def extract(akey, old_useful_info=[],merge=False):
  pdmv_request_list=[]
  req_list = get_requests_list()
  print len(req_list),"in reqmng"
  
  # filter on the ones which have a status  
  req_list=filter (lambda r: r.has_key("status"), req_list)
  print len(req_list),"with status"

  if type(akey)==list:
    match_req_list=[]
    for key in akey:
      if not key: continue
      match_req_list+=filter (lambda r: key in r["request_name"], req_list)
  else:
    match_req_list=filter (lambda r: akey in r["request_name"], req_list)

  print len(match_req_list),"filtered"

  for (n,req) in enumerate(match_req_list):
    print "Found",req["request_name"],":",n,"/",len(match_req_list)
    pdmv_request_list.append(
      parallel_test( [req,old_useful_info], force=True )
      )
    
  pdmv_request_list=filter(lambda r:r!={},pdmv_request_list)
  if merge:
    for req in req_list:
      if req in old_useful_info:
        print "pop one form old"
        old_useful_info.pop(req)
    return pdmv_request_list+old_useful_info
  else:
    return pdmv_request_list
  
  

def extract_useful_info_from_requests(old_useful_info=[],Nthreads=1):
  '''
  Put them in a Json
  ''' 
  pdmv_request_list=[]
  req_list = get_requests_list()

  print len(req_list)
  
  # filter on the ones which have a status  
  req_list=filter (lambda r: r.has_key("status"), req_list)

  #### filter on a certain list of campaigns
  ##req_list=filter (lambda r: "Summer12" in r["request_name"], req_list)
  ####req_list=filter (lambda r: "EXO-Summer12_DR52X-00202" in r["request_name"], req_list)

  # Multithreaded given the number of services to be queried
  print "Creating processing pool (%s processes)" %Nthreads
  pool = multiprocessing.Pool(Nthreads)
  print "Dispaching requests to processes..."  
  # this avoids an expensive copy
  repeated_old_useful_info=itertools.repeat(old_useful_info,len(req_list))
  pdmv_request_list = pool.map(parallel_test, itertools.izip(req_list,repeated_old_useful_info))
  print "End dispatching!"

  pdmv_request_list=filter(lambda r:r!={},pdmv_request_list)
     
  return pdmv_request_list


#------------------------------------------------------------------------------- 

def reduce_big_numbers(number):
  if number < -1:
    number=-1
  s_number=str(number)
  s_number=re.sub("000000$","M",s_number)
  s_number=re.sub("000$","k",s_number)
  return s_number

#-------------------------------------------------------------------------------

def linkToRunStats(req_name):
  link=runStats_address+req_name
  href='<a href="%s">%s</a>' %(link,req_name)
  return href

#------------------------------------------------------------------------------- 
# campaign,pdmv status,status,type,(priority,) name
def get_table_line(pdmv_req):
  line ="<tr>"
  for quality in [get_DASlink(pdmv_req["pdmv_dataset_name"]),
                  "%2.2f"%float(pdmv_req["pdmv_completion_in_DAS"]),
                  pdmv_req["pdmv_campaign"],
                  pdmv_req["pdmv_submission_date"],
                  pdmv_req["pdmv_running_days"],
                  pdmv_req["pdmv_completion_eta_in_DAS"],
                  reduce_big_numbers(pdmv_req["pdmv_expected_events"]),
                  pdmv_req["pdmv_evts_in_DAS"],                  
                  pdmv_req["pdmv_status_in_DAS"],
                  #pdmv_req["pdmv_status"],
                  pdmv_req["pdmv_status_from_reqmngr"],
                  #reduce_big_numbers(pdmv_req["pdmv_priority"]),
                  reduce_big_numbers(pdmv_req["pdmv_present_priority"]),
                  #pdmv_req["pdmv_type"].replace("MonteCarlo","MC"),
                  get_preplink(pdmv_req["pdmv_prep_id"]),
                  linkToRunStats(pdmv_req["pdmv_request_name"]),
                  pdmv_req["pdmv_monitor_time"]
                  ]:
    line+="<td>%s</td>"%quality
  line+="</tr>\n"
  return line
  
#-------------------------------------------------------------------------------

def get_preplink(prepid):
  url= "http://cms.cern.ch/iCMS/prep/requestmanagement?code=%s"%prepid
  link= "<a href=%s>%s</a>"%(url,prepid)
  return link

#------------------------------------------------------------------------------- 

def get_DASlink(dataset):
  #print "***%s***"%dataset
  das_url="https://cmsweb.cern.ch/das/request?view=list&limit=10&instance=cms_dbs_prod_global&input=dataset+dataset%%3D%s*+status%%3D*"
  dataset_enc=dataset.replace("/","%2F")
  das_url=das_url %dataset_enc
  return "<a href=%s>%s<a>" %(das_url,dataset)

#------------------------------------------------------------------------------- 
# print stats about requests
def print_stats(pdmv_req_list,prepids_to_filter=[],filter_on_req_name=''):
  
  
  # Filter by Ids
  section_prepid_list_not_there=""
  prepids_not_there=[]
  if prepids_to_filter!=[]:
    pdmv_req_list=filter(lambda pdmv_dict: pdmv_dict["pdmv_prep_id"] in prepids_to_filter,pdmv_req_list)
    available_prepids=map(lambda r: r["pdmv_prep_id"],pdmv_req_list)
    prepids_not_there=filter(lambda prepid: not prepid in available_prepids,prepids_to_filter)
  if prepids_not_there!=[]:
    section_prepid_list_not_there="<h2>Requested PREP-IDs not yed in the Request Manager:</h2>\n"
    section_prepid_list_not_there+="<ul>"
    for prepid in prepids_not_there:
      section_prepid_list_not_there+="<li>%s</li>"%get_preplink(prepid)
    section_prepid_list_not_there+="</ul>"

  if filter_on_req_name!='':
    pdmv_req_list = filter (lambda req: filter_on_req_name in req['pdmv_request_name'],pdmv_req_list)

  # Total events done
  total_evts_done=0
  for req in pdmv_req_list:
    total_evts_done+=req["pdmv_evts_in_DAS"]    

  # Total events done 
  total_evts_exp=0
  for req in pdmv_req_list:
    if 'pdmv_expected_events' in req:
      total_evts_exp+=req["pdmv_expected_events"]
    else:
      print "cannot sum up expected for",req['pdmv_request_name']
      req["pdmv_expected_events"]=0
  
  # Total Number of Jobs on the grid
  total_jobs=0
  for req in pdmv_req_list:
    total_jobs+=req["pdmv_all_jobs"]
  
  # Total Number of Jobs running on the grid
  total_running=0
  for req in pdmv_req_list:
    total_running+=req["pdmv_running_jobs"]

  # Total Number of Jobs pending in the batch
  total_pending=0
  for req in pdmv_req_list:
    total_pending+=req["pdmv_pending_jobs"]

  n_running_total=0
  n_running_campaign_dict={}
  n_changeable_total=0
  n_changeable_campaign_dict={}
  
  table_lines="<thead><tr>"
  for quality in ["Dataset",
                  "Completion DAS (%)",
                  "campaign",
                  "Sub. Date",
                  "Submitted since days",
                  #"Job Completion level (%)", 
                  "Eta (days)",
                  "Exp. Evts",               
                  "Evts DAS",                  
                  "DS Status",
                  #"PdmV Status", 
                  "Status from rqmngr", 
                  #"Sub. Prio.",
                  "Pres. Prio.",
                  #"Type", 
                  "PrepID", 
                  "Name",
                  "Updated"
                  ]:
    table_lines+="<th>%s</th>"%quality
  table_lines+="</tr></thead>\n"
  
  table_lines+="<tbody>\n"
  for pdmv_request_dict in pdmv_req_list:
    campaign=pdmv_request_dict["pdmv_campaign"]
    if pdmv_request_dict["pdmv_status_from_reqmngr"]=="running":
      n_running_total+=1      
      if not n_running_campaign_dict.has_key(campaign):
        n_running_campaign_dict[campaign]=1
      else:
        n_running_campaign_dict[campaign]+=1
    if pdmv_request_dict["pdmv_status"]=="ch_prio":
      n_changeable_total+=1
      if not n_changeable_campaign_dict.has_key(campaign):
        n_changeable_campaign_dict[campaign]=1
      else:
        n_changeable_campaign_dict[campaign]+=1
    
    
    
    # fill table lines
    table_lines+=get_table_line(pdmv_request_dict)
  
  table_lines+="</tbody>\n"
  
  # Print now the preamble
  preamble="Last heart-beat: %s\n" %time.asctime()
  preamble+= "<br> This page is experimental. Use it at your own risk!"
  preamble+="<h2>Total Evts in DAS (for the requests on this page): %s</h2>" %total_evts_done
  preamble+="<h2>Total Requests in Running status: %s</h2>\n" %n_running_total

  preamble+="<ul>"
  for campaign in sorted(n_running_campaign_dict.keys()):
    preamble+="<li>%s: %s</li>\n"%(campaign,n_running_campaign_dict[campaign])
  preamble+="</ul>"
  preamble+="<h2>Total Requests Priority Changeable: %s</h2>\n" %n_changeable_total
  preamble+="<ul>\n"
  for campaign in sorted(n_changeable_campaign_dict.keys()):
    preamble+="<li>%s: %s</li>\n"%(campaign,n_changeable_campaign_dict[campaign])
  preamble+="</ul>\n"    
  
  
  preamble+=section_prepid_list_not_there
  
  preamble+="<br>Job completion is calculated using DAS\n<br>"


  page_head="""
                <style type="text/css" title="currentStyle">
                        @import "http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/media/css/demo_page.css"; 
                        @import "http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/media/css/header.ccss";
                        @import "http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/media/css/demo_table_jui.css";
                        @import "http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/examples/examples_support/themes/smoothness/jquery-ui-1.8.4.custom.css";
                        @import "http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/extras/ColReorder/media/css/ColReorder.css";
                        @import "http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/extras/TableTools/media/css/TableTools.css";
                        div.dataTables_wrapper { font-size: 15px; }
                        table.display thead th, table.display td { font-size: 15px; }
                        


                </style>
                <script type="text/javascript" language="javascript" src="http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/media/js/jquery.js"></script>                
                <script type="text/javascript" language="javascript" src="http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/media/js/jquery.dataTables.js"></script>
                <script type="text/javascript" language="javascript" src="http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/media/js/jquery.dataTables.min.js"></script>
                <script type="text/javascript" language="javascript" src="http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/extras/ColReorder/media/js/ColReorder.js"></script>
                <script type="text/javascript" language="javascript" src="http://cms-pdmv.web.cern.ch/cms-pdmv/DataTables/extras/TableTools/media/js/TableTools.min.js"></script>
              
                <script type="text/javascript" charset="utf-8">
$(document).ready(function() {
oTable = $("#example").dataTable({
"bJQueryUI": true,
"sPaginationType": "full_numbers",
"iDisplayLength": 500
});
var params = getParams();
if ('search' in params) {
oTable.fnFilter( params['search'] )
}
} );

function getParams() {
var idx = document.URL.indexOf('?');
var tempParams = new Object();
if (idx != -1) {
var pairs = document.URL.substring(idx+1, document.URL.length).split('&');
for (var i=0; i<pairs.length; i++) {
nameVal = pairs[i].split('=');
tempParams[nameVal[0]] = nameVal[1];
}
}
return tempParams;
}

                </script>
  """


  page_html ="<html>"
  page_html+='<head>%s</head>\n'%page_head
  page_html+=preamble  
  page_html+='<table align="center" cellpadding="0" cellspacing="0" border="0" class="display" id="example">%s</table>'%table_lines
  page_html+="</body></html>"
  return page_html


#-------------------------------------------------------------------------------

def makeMon(filename,pageID,useful_info):
    try:
      ids = generic_get(filename)
      stats_page = print_stats(useful_info,ids)
      stats_file=open("stats_%s.html"%pageID,"w")
      stats_file.write(stats_page)
      stats_file.close()
    except:
      print "Error creating page for %s" %filename
      pass 
      
#------------------------------------------------------------------------------- 
import optparse
def build_parser():
  
    usage= "Usage:\n %prog options"
    parser = optparse.OptionParser(usage)
    parser.add_option("--no_cache",default=False,action='store_true',
                      help="Use not to use the cached stats json file. Default is False.")
    parser.add_option("--nprocesses",default="1",
                      help="Number of threads to query the CMS data services. Default is 1.")   
   
    parser.add_option("--refresh_interval",default="7200",
                      help="Number of seconds between two refreshes.Default is 7200")   
   
    options,args=parser.parse_args()
    return options,args
  

#------------------------------------------------------------------------------- 

if __name__ == "__main__":
    
  # Execution parameters
  options,args = build_parser()
  refresh_interval=int(options.refresh_interval)
  nprocesses = int(options.nprocesses)

  cycle=0
  
  while True:

    now=time.time()
    stats_json_name="stats_json.txt"
    stats_json_cache_name="stats_json_cache.txt"
    stats_json_present = os.path.exists(stats_json_name)
    lasttime=0 # 1st Jan 1970
    if stats_json_present:
      lasttime=os.path.getmtime(stats_json_name)
    
    useful_info=[]
    if now-lasttime > refresh_interval or options.no_cache:         
      print "File updated on %s now is %s : updating" %(time.ctime(lasttime),time.ctime(now))
      # Put the json used to generate the webpage on disk
      old_page_content=[]
      if os.path.exists(stats_json_cache_name):
        old_page_content_file=open(stats_json_cache_name,"r")
        try:
          old_page_content=eval(old_page_content_file.read())
          #old_page_content=json.loads(old_page_content_file.read())
        except:
          print "\n\n\n\n reading from cache failed. \n\n\n\n"
          sys.exit(-5)
        old_page_content_file.close()
        print "Got",len(old_page_content),"from cached old request statuses"
      else:
        print "No cache present. The Cache will be built."
        

      useful_info = extract_useful_info_from_requests(old_page_content,nprocesses)    

      isNotReabable=True
      timesFailed=0
      while isNotReabable or timesFailed>5:
        page_content_file=open(stats_json_name,"w")
        #make it readable
        page_content_file.write(pformat(useful_info))
        #page_content_file.write(json.dumps(useful_info,indent=4))
        page_content_file.close()
        try:
          rereadfile=open(stats_json_name)
          rereadinformation=eval(rereadfile.read())
          rereadfile.close()
          isNotReabable=False
        except:
          print "i/o of information failed, try again"
          timeFailed+=1
          
      shutil.copy(stats_json_name,stats_json_cache_name)

    else:
       page_content_file=open(stats_json_name,"r")
       #useful_info=eval(page_content_file.read())
       useful_info=json.loads(page_content_file.read())
       page_content_file.close()
            
    # Prepare a general webpage
    stats_page = print_stats(useful_info)
    ##stats_file=open("stats.html","w")
    ##write to the PdmV space directly
    stats_file=open("/afs/cern.ch/cms/PPD/PdmV/web/stats/index.html","w")
    stats_file.write(stats_page)
    stats_file.close()

    """
    ##JR remove because outdated
    # Prepare a webpage for some requests  
    monlist=[['http://vlimant.web.cern.ch/vlimant/Directory/specialRequests/PrepIdSummer12_HLT.txt','TSG'],
["http://vlimant.web.cern.ch/vlimant/Directory/specialRequests/PrepIdSummer12.txt",'Summer12'],
["http://vlimant.web.cern.ch/vlimant/Directory/specialRequests/PrepIdSummer12DR51X.txt",'Summer12DR'],
["http://vlimant.web.cern.ch/vlimant/Directory/specialRequests/PrepIdSummer11_Pub.txt",'Summer11_Pub'],
["http://vlimant.web.cern.ch/vlimant/Directory/specialRequests/PrepIdSummer12_PAG.txt",'PAG'],
["http://vlimant.web.cern.ch/vlimant/Directory/specialRequests/PrepIdSummer12_LowPU_dr.txt","LowPUDR"],
["http://vlimant.web.cern.ch/vlimant/Directory/specialRequests/PrepIdSummer12_HLT_dr.txt","TSGDR"],
["https://dpiparo.web.cern.ch/dpiparo/GlobalMonitoringScripts/highPriorityAnalyses.txt","HighPriority"]]

    for filename,nick in monlist:
       makeMon(filename,nick,useful_info)

    # Summer12 52X
    S1252x_html = print_stats ( useful_info,[],"52X")
    S1252x_ids_file = open("stats_52X.html","w")
    S1252x_ids_file.write(S1252x_html)
    S1252x_ids_file.close()

    """

    l=open('stats.log','a')
    l.write(time.asctime()+'\n')
    l.close()

    #nsecs=3600*2 - 100
    nsecs=refresh_interval
    print "\n\n\n\n \t\tSleeping %s secs \n\n\n\n" %nsecs
    time.sleep(nsecs)

    
    
