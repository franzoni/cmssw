# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.MIMEText import MIMEText


def sendMonitoringMail(subject, from_address, to_address, cc_address, replyto_address, templatefile, replaces):
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    fp = open(templatefile, 'rb')
    # Create a text/plain message


    message_txt = fp.read()
    for replacepair in replaces:
        message_txt = message_txt.replace(replacepair[0], replacepair[1])
    msg = MIMEText(message_txt)
    fp.close()

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    if cc_address != None:
        msg['Cc'] = cc_address
    if replyto_address != None:
        msg['Reply-to'] = replyto_address

    #print msg


    to_address_list = to_address.split(',')
    if cc_address != None:
        to_address_list = to_address_list + cc_address.split(',')
    
    
    #print to_address_list
    #return        
    

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(from_address, to_address_list, msg.as_string())
    s.quit()


if __name__     ==  "__main__":

    templatefile = "data/test_mailtemplate.txt"
    quotanode = "/mynode/eos/pippo/"
    replaces = [("@NODE@", quotanode)]

    subject = 'Mail test'
    from_address = raw_input("from: ")
    to_address = raw_input("to: ")
    sendMonitoringMail(subject, from_address, to_address, "cms-cernt3-manager@cern.ch", None, templatefile, replaces)



    from_address = raw_input("from: ")
    to_address = raw_input("to: ")
    sendMonitoringMail(subject, from_address, to_address, None, None, templatefile, replaces)
