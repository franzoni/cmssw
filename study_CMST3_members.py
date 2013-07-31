#!/usr/bin/python2.4
import os, socket

from optparse import OptionParser
parser = OptionParser()

parser.add_option("-v", "--verbose",
                  action="store_true", dest="isDebug", default=False,
                  help="in DEBUG mode, with more verbosity than minimal")

parser.add_option("-p", "--prod",
                  action="store_true", dest="isProd", default=False,
                  help="in PROD mode, produces list of enabled members who need to be removed")

parser.add_option("-r", "--fileReal",
                  action="store_true", dest="fileReal", default='',
                  help="fileReal is a comma-separate file listing real (i.e. entitled to be ) CMST3 users")

parser.add_option("-e", "--fileEnabled",
                  action="store_true", dest="fileEnabled", default='',
                  help="fileEnabled is a comma-separate file listing CMST3 enabled users (wether they're entitled or not)")

(options, args) = parser.parse_args()



# handle different units of disk space
def convert_TB(num,unit):
    if unit=='B':
        num/=(1024.*1024.*1024.*1024.)
    elif unit=='kB':
        num/=(1024.*1024.*1024.)
    elif unit=='MB':
        num/=(1024.*1024.)
    elif unit=='GB':     
        num/=1024.
    elif unit=='TB':     
        num/=1.
    elif unit=='PB':     
        num*=1024.
    else:
        pass
    return num        



print 
print ' looping over files of REAL and ENABLED members and making the matcghing (takes a while) ... '

hostname = socket.gethostname()
if 'cern.ch' in hostname:
    print ' hostname is: %s ==> good\n'%(hostname)
else:
    print ' ++ you\'re not on a CERN machine (%s) this script won\'t work '%(hostname)
    

enab_f = open('the-enabled-members.txt')
real_f = open('cmg-real-members-mod.csv')


### parse files and prepare 2 list of lists

#currently enabled CMSt3 users (get CERN login)
enab_l = list()
for line in enab_f:
    list_tmp = (line.split())
    enab_l.append(list_tmp)

#make list of real users (from PJ's email of names and last names)
real_l          = list()
real_surnames_l = list()
real_login_l    = list()
for line in real_f:
    list_tmp = (line.split(','))
    real_l.append(list_tmp)
    surname = list_tmp[1]
    # turn surnames to lower case to avoid ambiguities
    real_surnames_l.append( surname.lower()  )
    # contemplate the case of real users with more than one login:
    # ==> put all the logins matcing a surname into the list real_login
    # ==> FIX: some surnames match more than one user...
    real_login = list( (  os.popen('phonebook --surname "%s" --all | grep zh | grep afs | awk \'{print $1}\''%surname).read().split('\n') )  )
    # cleanup '' elements in list of matching login
    real_login = list(filter(('').__ne__, real_login))
    if len(real_login)>0:
        real_login_l.extend( real_login  )
    if options.isDebug:
        print '\nlisting real surname: %s login: %s'%(surname,real_login)

# dump summary of all the logins correspoding to users entitled to the CMST3
if options.isDebug:
        print ''
        print  'list of login of real users: %s'%real_login_l
        print ''

# initialize accumulators
quota_total=0.
tostay_total=0.
tostay_used=0.
tostay_users=0
toclean_total=0.
toclean_used=0.
toclean_users=0


# loop over _enabled_ users (one list per user => identify his/her login)
# and check wether they're part of the _real_ CERN users 
for enab_u in enab_l:
    enab_login = enab_u[0] 

    tostay_used =0.
    toclean_used=0.
    # handle the different units MB,GB,TB,PB
    space_used=convert_TB( float(enab_u[3]), enab_u[4] )

    ###
    if enab_login in real_login_l:
        tostay_used=space_used
        tostay_total+=tostay_used
        tostay_users+=1
        if options.isDebug:
            enab_surname = ( (  os.popen('phonebook --login %s'%enab_login).read().split('    ')   )[0] ).lower()
            print '\n%s CAN be in CMSt3 %s %s    (%s TB)'%(enab_surname,enab_u[3],enab_u[4],tostay_used)
    else:
        toclean_used=space_used
        toclean_total+=toclean_used
        toclean_users+=1
        if options.isDebug:
            enab_surname = ( (  os.popen('phonebook --login %s'%enab_login).read().split('    ')   )[0] ).lower()
            print '\n                                                %s should NOT be in CMSt3 %s %s    (%s TB)'%(enab_surname,enab_u[3],enab_u[4],toclean_used)
        if options.isProd:
            surname = (((  os.popen('phonebook --login %s --all | grep "Display Name"'%enab_login).read())).split(' '))[-1]
            name = (((  os.popen('phonebook --login %s --all | grep "Display Name"'%enab_login).read())).split(' '))[-2]
            email        =  ((  os.popen('phonebook --login %s --all | grep "E-mail"'%enab_login).read()).split('    ') )[-1] 
            name.replace(' ','')
            surname.replace(' ','')
            print '%s %s email: %s'%(name,surname,email)

print ''
print ''
print '+++ total SPACE toclean: %s and total SPACE to stay: %s [TB]'%(  float('%.3g' %  toclean_total) ,    float('%.3g' %  tostay_total)   )
print '+++ total USERS toclean: %s and total USERS to stay: %s '%(toclean_users,tostay_users)
print        
print        
