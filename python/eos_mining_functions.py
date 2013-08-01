import subprocess

# return filename from a line of popularity file
def filePathFromLine( oneLine ):
    oneLineSplit = oneLine.split('\t')
    if len(oneLineSplit) < 6:
        print  'line is: %s '%(oneLine)
        return '** path-not-found'
    else :
        #print 'DEBUG %s '%(    ((oneLineSplit)[3].split())[0] )  # remove this        
        return  (  ((oneLineSplit)[3].split())[0],   oneLineSplit[5]  )



# get from eos userId, starting from a directory path in eos 
# set eos executable
eos = '/afs/cern.ch/project/eos/installation/cms/bin/eos.select'

def userIdFromFilePath( path ):
   p = subprocess.Popen( '%s ls %s -l '%(eos,path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   stdout, stderr = p.communicate()
   # to be EXTENDED
   # LIMITS: login is captured only for the FIRST listed file inside the directory
   stdoutList = ( stdout.split('\n')[0] ).split()
   if ( 'Unable to stat' in stderr ) :
       # print  '    folder: %s does NOT EXIST'%(path)
       # the following is an terror key 'facon grandmere'
       return '** folder does NOT EXIST'
   elif len(stdoutList)<9 :
       print  'stdoutList not long enough: %s (path: %s ) '%(stdoutList,path)
       return '** user not found'
   else :
       #print 'DEBUG %s '%( ( stdout.split('\n')[0] ).split() )  # remove this
       return ( ( stdout.split('\n')[0] ).split() )[2]


def nameAndSurnameFromLogin( login ):
    p = subprocess.Popen( 'phonebook --login %s '%(login), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    # to be EXTENDED
    stdoutList = ( stdout.split('\n')[0] ).split()
    if ( 'Unable to stat' in stderr ) :
        # the following is an terror key 'facon grandmere'
        return '** folder does NOT EXIST'
    elif len(stdoutList)<9 :
        print  'problem in values returned by phonebook'
        return '** phonebook result not valid'
    else :
        # chop off the last 7 elements of phonebook output to give you all the names + surnames of a person
        return ' '.join( stdout.split()[:-7] )
    

def emailFromLogin( login ):
    p = subprocess.Popen( 'phonebook --login %s --all | grep  E-mail'%(login), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    # to be EXTENDED
    stdoutList = ( stdout.split('\n')[0] ).split()
    #print stdoutList
    if ( 'Unable to stat' in stderr ) :
        # the following is an terror key 'facon grandmere'
        return '** folder does NOT EXIST'
    elif len(stdoutList)<2 :
        print  'problem in values returned by phonebook'
        return '** phonebook result not valid'
    else :
        # chop off the last 7 elements of phonebook output to give you all the names + surnames of a person
        return stdout.split()[-1]
        #return stdout
