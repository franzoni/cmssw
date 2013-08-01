import python.eos_tool_parser    as parser
import python.eos_tool_phonebook as phonebook
import python.eos_tool_mail      as mail



if __name__     ==  "__main__":

    filename = 'data/20130726-eoscms-mode-777.log'
    thefile = open(filename, 'rb')


    users = []
    userFileMap = {}

    for line in thefile.readlines():
        #print line
        report = parser.EOSLsReport(line.split())
        print report
        if not report.user in userFileMap:
            userFileMap[report.user] = []
        
        userFileMap[report.user].append(line)

        if not report.user in users:
            users.append(report.user)


    

    print "# of users: " + str(len(users))
    print users

    
    for user in ['meridian']:
        templatefile = "data/permission_notification_mailtemplate.txt"
        
        
        dump = ''.join(userFileMap[user])
        #print dump

        phnbookentry = phonebook.lookupByLogin(user)
        


        replaces = [("@NAME@", phnbookentry.firstname), ("@DUMP@", dump)]
        subject = 'Permissions on some of your EOS files'
     

        
        from_address = "gianluca.cerminara@cern.ch"
        to_address = "giovanni.franzoni@cern.ch"
        cc_address = "gianluca.cerminara@gmail.com"
        replyto_address = "cms-cernt3-manager@cern.ch"
        mail.sendMonitoringMail(subject, from_address, to_address, cc_address, replyto_address, templatefile, replaces)




    thefile.close()
