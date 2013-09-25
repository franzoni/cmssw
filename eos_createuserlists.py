import python.eos_tool_parser    as parser
import python.eos_tool_phonebook as phonebook
#import python.eos_tool_mail      as mail
import ConfigParser as ConfigParser
import os
import commands
import sys

def eosList(options, path):
    print path
    ls_cmd = '/afs/cern.ch/project/eos/installation/cms/bin/eos.select ls -l ' + options + ' ' + path
    ls_out = commands.getstatusoutput(ls_cmd)
    lines = []
    ret = []
    if ls_out[0] == 0:
        lines = ls_out[1].split('\n')
        for line in lines:
            if line != "":
                #print line
                ret.append(parser.EOSLsReport(line.split()))
    else:
        print "ERROR:" + ls_out[1]
    return ret

class EOSTeam:
    def __init__(self, name, egroup, nodes):
        self.name   = name
        self.egroup = egroup
        self.nodes   = nodes


def eosUserListInDir(path):
    userlist = []
    files = eosList('',path)
    for fileline in files:
        if not fileline.user in userlist:
            userlist.append(fileline.user)
        if fileline.isDir:
            for username in eosUserListInDir(path + '/' + fileline.path):
                if not username in userlist:
                    userlist.append(username)

    return userlist

if __name__     ==  "__main__":


    # read a global configuration file
    cfgfile = ConfigParser.ConfigParser()
    cfgfile.optionxform = str

    CONFIGFILE = "configs/eos_teams.cfg"
    print 'Reading configuration file from ',CONFIGFILE
    cfgfile.read([ CONFIGFILE ])

    topnode           = cfgfile.get('Common','topnode')
    teamNames         = cfgfile.get('Common','teams').split(',')


    teams = []
    for teamName in teamNames:
        egroup = cfgfile.get(teamName,'egroup')
        nodes  = cfgfile.get(teamName,'nodes').split(',')
        team = EOSTeam(teamName, egroup, nodes)
        teams.append(team)


    #1 ls top-node
    topdirs = eosList('',topnode)
    print topdirs

    #2 identify the group
    for group in teams:
        print "GROUP: " + group.name

        filename = 'data/' + group.egroup + '.user.list'
        if not os.path.exists(filename):
            print "   Creating user list file: " + filename
        else:
            print "   WARNING: user list file: " + filename + " already exists, will skip this group!"
            continue

        #3 if user-file not yet created ls group recursively and collect users
        userlist = []
        for grpnode in group.nodes:
            filesindir = eosList('',topnode+grpnode)
            userlist.extend(eosUserListInDir(topnode+grpnode))
            
            
        #4 dump user list into a txt file. Format of each line: A,USERNAME,Comment        
        
        userlistfile = open(filename, 'w')
        for username in userlist:
            userlistfile.write('A,'+username+",Original user owning files in the team area\n")
        userlistfile.close()
        
            
    sys.exit(0)
