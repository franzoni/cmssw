
import ConfigParser as ConfigParser


class EOSNode:
    """
    Object representing a single node on EOS.
    """
    def __init__(self, name, config):
        self.eosPath = config.get(name, 'eosPath')
        return






# --------------------------------------------------------------------------------
# configuration

# read a global configuration file
cfgfile = ConfigParser.ConfigParser()
cfgfile.optionxform = str

CONFIGFILE = "configs/eos_CERNT3.cfg"
print 'Reading configuration file from ',CONFIGFILE
cfgfile.read([ CONFIGFILE ])


nodeNames         = cfgfile.get('Common','nodes').split(',')
afsTargetDir      = cfgfile.get('Common','afsTargetDir')
digestFileName    = cfgfile.get('Common','digestFileName')
dumpFileName      = cfgfile.get('Common','dumpFileName')

nodes = []
for nodeName in nodeNames:
    node = EOSNode(nodeName, cfgfile)
    nodes.append(node)
