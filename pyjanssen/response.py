#
# Python library for Janssen MCM controller
# Response processors
# By Rob Heath, 27/11/2018
#


def parse(request_type,stdout):
    '''
    arguments: request_type, stdout
    returns: usable data from string input
    '''
    return LIBRARY[request_type](stdout)

def break_up(stdout,conversions={}):
    # takes input of form:
    #  "thing : value\nthing2 : value2"
    # and returns
    # {"thing":"value","thing2":"value2"}
    data = {}
    for row in stdout.split('\n'):
        items = row.split(':')
        data[items[0].strip()] = items[1].strip() if items[0].strip() not in conversions else conversions[items[0].strip()](items[1].strip())
        #print('{} in {}: {}'.format(items[0].strip(),conversions,items[0].strip() in conversions))
    return data
    
def _parse_mov(stdout):
    # MOV Basedrive move command
    b = break_up(stdout)
    return b

def _parse_ext(stdout):
    # EXT Flexdrive external mode input command
    b = break_up(stdout)
    return b

def _parse_stp(stdout):
    # STP Basedrive stop command
    b = break_up(stdout)
    return b

def _parse_sts(stdout):
    # STS Basedrive status command
    b = break_up(stdout)
    return b

def _parse_info(stdout):
    # INFO information command
    b = break_up(stdout)
    return b

def _parse_pos(stdout):
    # POS encoder position command
    b = break_up(stdout,{'POS':int,'RVL':int})
    return b

def _parse_rst(stdout):
    # RST reset encoder position command
    return stdout

#def _parse_oemc(stdout): # this is interactive and must be handled using Popen separately
#    # OEMC encoder autocalibration command
#    return stdout

def _parse_desc(stdout):
    # DESC module description command
    b = break_up(stdout)
    return b

def _parse_fben(stdout):
    # FBEN Servodrive enable command
    b = break_up(stdout)
    return b

def _parse_fbxt(stdout):
    # FBXT Servodrive disable command
    b = break_up(stdout)
    return b

def _parse_fbcs(stdout):
    # FBCS Servodrive go to setpoint command
    b = break_up(stdout)
    return b

def _parse_fbes(stdout):
    # FBES Servodrive emergency stop command
    b = break_up(stdout)
    return b

def _parse_fbfe(stdout):
    # FBFE Servodrive find endstops command
    b = break_up(stdout)
    return b

def _parse_fbst(stdout):
    # FBST Servodrive get status position control command
    b = break_up(stdout,{'ENABLED':int,
        'BUSY':int,
        'POS1':int,
        'POS2':int,
        'POS3':int,
        'ERR1':int,
        'ERR2':int,
        'ERR3':int})
    return b
    
LIBRARY = {
    'MOV':_parse_mov,
    'EXT':_parse_ext,
    'STP':_parse_stp,
    'STS':_parse_sts,
    'INFO':_parse_info,
    'POS':_parse_pos,
    'RST':_parse_rst,
    #'OEMC':_parse_oemc, #this is interactive and must be handled separately
    'DESC':_parse_desc,
    'FBEN':_parse_fben,
    'FBXT':_parse_fbxt,
    'FBCS':_parse_fbcs,
    'FBES':_parse_fbes,
    'FBFE':_parse_fbfe,
    'FBST':_parse_fbst
    }