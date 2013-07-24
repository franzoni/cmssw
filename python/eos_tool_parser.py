
def toTBConversion(unit):
    ret = 1
    if unit == 'PB':
        ret = 1E3
    elif unit == 'TB':
        ret = 1
    elif unit == 'GB':
        ret = 1E-3
    elif unit == 'MB':
        ret = 1E-6
    elif unit == 'kB':
        ret = 1E-9
    elif unit == 'B':
        ret = 1E-12
    else:
        print "[toTBConversion]***Error; unknown unit:",unit
    return ret


def tokFilesConversion(unit):
    ret = 1
    if unit == 'G-':
        ret = 1E6
    elif unit == 'M-':
        ret = 1E3
    elif unit == 'k-':
        ret = 1
    elif unit == '-':
        ret = 1E-3
    else:
        print "[tokFilesConversion]***Error; unknown unit:",unit
        
    return ret





class EOSQuotaReport:
    """ Stores the report for a given user/group of eos dump quota
    It is created starting from a given line in the output of 'eos ls quota' command

    NOTE: units are TB for space and kFiles for of files.
    """ 
    
    def __init__(self, quotaline_list):
        self.user = quotaline_list[0]
        self.used_bytes = float(quotaline_list[1])*toTBConversion(quotaline_list[2])
        self.logi_bytes = float(quotaline_list[3])*toTBConversion(quotaline_list[4])
        self.used_files = float(quotaline_list[5])*tokFilesConversion(quotaline_list[6])
        self.aval_bytes = float(quotaline_list[7])*toTBConversion(quotaline_list[8])
        self.aval_logib = float(quotaline_list[9])*toTBConversion(quotaline_list[10])
        self.aval_files = float(quotaline_list[11])*tokFilesConversion(quotaline_list[12])
        self.filled = float(quotaline_list[13])
        self.vol_status = quotaline_list[14]
        self.ino_status = quotaline_list[15]


    def __str__(self):
        ret = "user\t used bytes\t logi bytes\t used files\t aval bytes\t aval logib\t aval files\t filled[%]\t  vol-status\t ino-status\n"
        ret += '%s\t %0.2f TB\t %0.2f TB\t %0.2f k-\t %0.2f TB\t %0.2f TB\t %0.2f k-\t %0.2f\t\t %s\t %s' % (self.user,self.used_bytes,self.logi_bytes,self.used_files,self.aval_bytes,self.aval_logib,self.aval_files,self.filled,self.vol_status,self.ino_status)
        return ret



def parse_groupsummay_quota_dump(dump):
    """
    parse the quota dump for a given node and returns:
    used bytes logi bytes used files aval bytes aval logib aval files filled[%]  vol-status ino-status
    for the group summary
    """
    #print dump.split('\n')
    summary_fileds = dump.split('\n')[-1].split()
    return EOSQuotaReport(summary_fileds)



