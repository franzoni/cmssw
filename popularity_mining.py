#!/usr/bin/python2.4
import os, socket, sys, string
import python.eos_tool_phonebook as phonebook

import python.eos_mining_functions as funct

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--fileWithPath",
                  action="store", dest="fileWithPath", default="",
                  help="file (with full path) holding popularity statistics")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="verbose output for debug mode")
parser.add_option("-s", "--showEmail",
                  action="store_true", dest="showEmail", default=False,
                  help="show email address of person owner of directory present in popularity file")
parser.add_option("-n", "--nonexisting",
                  action="store_true", dest="nonexisting", default=False,
                  help="show non existing directories among those signalled by popularity")
parser.add_option("-e", "--emailSend",
                  action="store_true", dest="emailSend", default=False,
                  help="send templated email to people who have directories in popularity report")
(options, args) = parser.parse_args()


# check that input was given, otherwise bail out
if options.fileWithPath == "" :
    print 'please provide file with path (-f)'
    sys.exit(1)
else :
    print ''
    print '  popularity file benig analyzed: %s'%options.fileWithPath
    print '  the process may take time ( O(10s) or more if input file is >>100 lines )'
    print ''


theFile   = open(options.fileWithPath,'r') # open in read mode
fileLines = theFile.read()
fileLines = fileLines.split('\n')


linesCounter          =0
missingFoldersCounter =0
integralSpace         =0.
# dictionary with 0) userID as key, holding a list whose two members are
# 1) total size of his/her data and 2) a list of directories
dict = {}

##########################################################################
# loop over all lines of input file
for oneLine in fileLines:
    # protect against empty lines and newlines
    if len(oneLine)<3:
        continue
    linesCounter        +=1
    size=0.
    oneFilePath=''
    size, oneFilePath   = funct.filePathFromLine(oneLine)
    userId              = funct.userIdFromFilePath( oneFilePath )
    if options.verbose:
        print ''
        print 'eos folder number %s of size: %s GB  for user %s'%(linesCounter,size,userId)

    # count the number of eos directories which are in the input popularity file but don't exist in eos, at the time of script execution
    if '** folder does NOT EXIST' in userId:
        missingFoldersCounter+=1
        if options.nonexisting:
            print  '    folder: %s does NOT EXIST'%( oneFilePath )
        continue

    if not (userId in dict.keys() ) :
        dict[userId]=[float(size),[oneFilePath]]
    else :
        dict[userId][1].append(oneFilePath)
        dict[userId][0]+=float(size)

    integralSpace+=float(size)

    if options.verbose:
        print dict
##########################################################################

for userId in dict.keys():
    print '\n   ++ %s (%s) holds %s GB of data in %s directories: '%( phonebook.nameAndSurnameFromLogin( userId ),  userId, dict[userId][0], len( dict[userId][1] )  )
    if options.showEmail:
        print '      %s '%( phonebook.emailFromLogin( userId )  )
    print '\n     '.join( dict[userId][1]  )
    print ''
    


print ''        
print ''        
print '    popularity file analyzed: %s'%options.fileWithPath
print '    found % s folders in input file, of which %s don\'t exist'%(linesCounter,missingFoldersCounter)
print '    total eos space in this popularity report:  %s GB'%(integralSpace)
print '    %s user(s) involved'%( len( dict.keys() )  )
print ''
print ''

from sys import exit
if not options.emailSend :
    exit()

# Make sure that the user is CERTAIN about sending out all those emials.. 
print 'you\'re about to send %s emails - are you sure ? '%( len( dict.keys() )  )
print '    ******************************* '
confirm = raw_input('     Do you confirm? (y/N) ')
confirm = confirm.lower() #convert to lowercase
if confirm != 'y':
    exit()

print ' '

#start setting up the ingredients needed to send the email
templatefile = 'data/ask-feedback-popularity.txt'


import python.eos_tool_mail      as mail
for userId in dict.keys():
    listOfDirectories =   '\n     '.join( dict[userId][1]  )
    replaces = [("@NAME@", phonebook.nameAndSurnameFromLogin( userId ) ), ("@DUMP@",listOfDirectories) ]
    subject = 'CMS T3: feedback about data popularity'

    from_address = "giovanni.franzoni@cern.chh"
    to_address = "gianluca.cerminara@cern.ch"
    cc_address = "franzoni@gmail.com"
    replyto_address = "cms-cernt3-manager@cern.ch"
    mail.sendMonitoringMail(subject, from_address, to_address, cc_address, replyto_address, templatefile, replaces)
