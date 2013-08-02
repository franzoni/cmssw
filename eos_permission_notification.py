import python.eos_tool_parser    as parser
import python.eos_tool_phonebook as phonebook
import python.eos_tool_mail      as mail
import os


if __name__     ==  "__main__":

    filename = 'data/20130726-eoscms-mode-777.log'

    cachefilename = filename + ".cache"
    alreadysent = []
    if not os.path.exists(cachefilename):
        print cachefilename
        cachefile = open(cachefilename, 'w')
    else:
        cachefile = open(cachefilename, 'a+b')
        alreadysent = cachefile.readlines()
        print alreadysent
    thefile = open(filename, 'rb')


    users = []
    userFileMap = {}

    for line in thefile.readlines():
        #print line
        report = parser.EOSLsReport(line.split())
        if '/cms/store/user/' in report.path or \
           '/cms/store/cmst3/user/' in report.path or \
           '/cms/store/group/' in report.path or \
           '/cms/store/caf/user/' in report.path or \
           '/cms/store/cmst3/group/' in report.path:

            print report
            
            if not report.user in userFileMap:
                userFileMap[report.user] = []

            userFileMap[report.user].append(line)

            if not report.user in users:
                users.append(report.user)
        else:
            print "ignoring path: " + report.path

    #alreadysent=cachefile.readlines()

    print "# of users: " + str(len(users))
    print users

    
    for user in users:
        if user+'\n' in alreadysent:
            print "User: " + user + " already notified: skipping"
            continue
        if user == 'nobody':
            continue
        
        print user
        templatefile = "data/permission_notification_mailtemplate.txt"
        
        
        dump = ''.join(userFileMap[user])
        #print dump

        phnbookentry = phonebook.lookupByLogin(user)
        print phnbookentry

        
        replaces = [("@NAME@", phnbookentry.firstname), ("@DUMP@", dump)]
        subject = 'Permissions on some of your EOS files'
     
        print "--------------------------------------------------------"
        print "Mail: "
        from_address = "automated@cern.ch"
        to_address = phnbookentry.email
        cc_address = "toreplace@cern.ch"
        replyto_address = "cms-cernt3-manager@cern.ch"
        mail.sendMonitoringMail(subject, from_address, to_address, cc_address, replyto_address, templatefile, replaces)
        cachefile.write(user+'\n')

        
    cachefile.close()


    thefile.close()
