# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.MIMEText import MIMEText


def sendMonitoringMail(subject, from_address, to_address, templatefile, replaces):
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

    #print msg

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(from_address, [to_address], msg.as_string())
    s.quit()


if __name__     ==  "__main__":

    templatefile = "data/quota_warning_mailtemplate.txt"
    quotanode = "/mynode/eos/pippo/"
    status = 30
    replaces = [("@NODE@", quotanode), ("@DUMP@", "pluto")]
    subject = 'WARNING: EOS quota for node %s is now %0.2f %% full' % (quotanode, status)
    from_address = 'gianluca.cerminara@cern.ch'
    to_address = 'gianluca.cerminara@gmail.com'
    sendMonitoringMail(subject, from_address, to_address, templatefile, replaces)



