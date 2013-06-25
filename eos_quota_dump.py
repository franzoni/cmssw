#!/usr/bin/env python

import sys
import os
import commands
import datetime
import gzip
import python.eos_tool_config as config



def parse_groupsummay_quota_dump(dump):
    """
    parse the quota dump for a given node and returns:
    used bytes logi bytes used files aval bytes aval logib aval files filled[%]  vol-status ino-status
    for the group summary
    """
    #print dump.split('\n')
    summary_fileds = dump.split('\n')[-1].split()
    return (float(summary_fileds[1]), float(summary_fileds[3]), float(summary_fileds[5]), float(summary_fileds[7]), float(summary_fileds[9]), float(summary_fileds[11]), float(summary_fileds[13]), summary_fileds[14], summary_fileds[15])
    


if __name__     ==  "__main__":


    todaydate = datetime.datetime.today()
    todaydate_string = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")

    digest_lines = []
    digest_lines.append('| *Quota Node* | *quota (logical TB)* | *used (logical TB)* | *used (%)* | *status* |')


    # tgz the old dump and unlink it
    olddump = os.readlink(os.path.join(config.afsTargetDir,config.dumpFileName))
    olddumpfile = open(olddump, 'rb')
    olddumpfile_zip = gzip.open(olddump + '.gzip', 'wb')
    olddumpfile_zip.writelines(olddumpfile)
    olddumpfile.close()
    olddumpfile_zip.close()
    os.unlink(os.path.join(config.afsTargetDir,config.dumpFileName))
    os.remove(olddump)
    
    dumpFileNameWithDate = config.dumpFileName.split('.')[0]+'_' + todaydate_string +'.wiki'
    dumpFile = open(os.path.join(config.afsTargetDir,dumpFileNameWithDate), 'w')


    
    for node in config.nodes:

        print 'Quota node path:',node.eosPath
        #eos_quota_ls = "/afs/cern.ch/project/eos/installation/0.2.31/bin/eos.select quota ls -p %s" % node.eosPath
        eos_quota_ls = "/afs/cern.ch/project/eos/installation/pro/bin/eos.select quota ls -p %s" % node.eosPath
        eos_quota_ls_out = commands.getstatusoutput(eos_quota_ls)
        print  eos_quota_ls
        if eos_quota_ls_out[0] == 0:
            values = parse_groupsummay_quota_dump(eos_quota_ls_out[1])
            #print values

            line = '| =%s= | %0.2f | %0.2f | %0.2f | %s |' % (node.eosPath, values[4], values[1], values[6], values[7])
            #print line
            digest_lines.append(line)
            dumpFile.write('\nQuota dump for node =%s= run on %s\n' % (node.eosPath, todaydate))
            dumpFile.write('<verbatim>\n')
            dumpFile.write(eos_quota_ls_out[1]+'\n')
            dumpFile.write('</verbatim>\n\n')

        else:
            print eos_quota_ls_out[1]

    digest_lines.append('Last updated on %s' % todaydate)

    digestFile = open(os.path.join(config.afsTargetDir,config.digestFileName), 'w')
    for item in digest_lines:
        digestFile.write("%s\n" % item)
    digestFile.close()
    dumpFile.close()

    os.symlink(os.path.join(config.afsTargetDir,dumpFileNameWithDate),os.path.join(config.afsTargetDir,config.dumpFileName))

    sys.exit(0)


#TODO add parameters e-gorup for notifications
