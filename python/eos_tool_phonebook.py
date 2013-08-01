import commands

class PhonebookEntry:
    """ This class represet an entry in the phonebook DB"""
    def __init__(self, attrlist):
        self.firstname = attrlist[0]
        self.surname   = attrlist[1]
        self.login     = attrlist[2]
        self.email     = attrlist[3]
        
    def __str__(self):

        ret = "Name: " + self.surname +' '+ self.firstname+'\n' + \
              "Login: "+self.login+'\n' + \
              "Email: "+self.email
        return ret
        

# note the position of the various fileds is relevant for the parsing of the output, for this reason it is defined only here

phonebook_terse_command = '--terse firstname --terse surname --terse login --terse email'

def lookupByLogin(login):
    """ Lookup in phonebook by login. the output is configured via the --terse option. Other fields
    can be added trasnparently preserving the order of the existing ones and implementing
    them in the PhonebookEntry class"""
    phonebook_cmd = 'phonebook --login %s ' % login
    phonebook_cmd += phonebook_terse_command
    phonebook_out = commands.getstatusoutput(phonebook_cmd)
    if phonebook_out[0] == 0:
        ret = PhonebookEntry(phonebook_out[1].split(';'))
    else:
        print "Error looking up in phonebook: ", phonebook_out[1]
        #FIXME: raise?
        ret = '** phonebook result not valid'
    return ret


def nameAndSurnameFromLogin( login ):
    ret = lookupByLogin(login)
    return ret.surname + ' ' + ret.firstname 
    

def emailFromLogin( login ):
    ret = lookupByLogin(login)
    return ret.email



if __name__     ==  "__main__":
    login = raw_input("lookup login: ")
    
    print nameAndSurnameFromLogin(login)

    print emailFromLogin(login)

    print lookupByLogin(login)
