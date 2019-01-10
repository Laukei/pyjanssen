#
# Python library for Janssen MCM controller
#
# by Rob Heath, 2018-11-23
#

import subprocess
import os

import pyjanssen.response

FORWARD = 1
CW = FORWARD
BACKWARD = 0
CCW = BACKWARD

class Counter:
    def __init__(self,value=0):
        super().__init__()
        self.value = value
        
    def get(self):
        self.value += 1
        return self.value-1

class MCM:
    def __init__(self,device=None,**kwargs):
        super().__init__()
        self.__exe = kwargs.get('exe','cacli.exe')
        self.__server = kwargs.get('server',False)
        self.__verbose = kwargs.get('verbose',False)
        self._check_cacli()
        self.__settings = {
            'frequency':{'1':100,'2':100},
            'step_size':{'1':100,'2':100},
            'temperature':{'1':293,'2':293},
            'steps':{'1':100,'2':100},
            'profile':{'1':'PROFILE1','2':'PROFILE1'},
            }
        self.__command_log = {}
        self.__counter = Counter()
        self.__device = device
        self.__servodrive_enabled = False
        
        
    def _check_cacli(self):
        '''
        checks path to cacli.exe; raises error if not a file
        '''
        try:
            assert os.path.isfile(self.__exe) == True
        except:
            raise CacliError('could not find file at {}'.format(self.__exe))

            
    def _run(self,*command_list):
        '''
        arguments: *command_list
        returns: parsed reply from cacli via __parse_reply()
        
        basic run command for cacli. requires only the commands to be run: MCM handles
        the device location and/or server
        
        will only output from functions with reply handler in response.py
        '''
        subprocess_parameters = [self.__exe]
        if self.__server == True:
            if self.__device == None:
                subprocess_parameters.append('@SERV')
            elif self.__device != None:
                subprocess_parameters.append('@SERV:{}'.format(self.__device))
        elif self.__device != None:
            subprocess_parameters.append('@{}'.format(self.__device))
        subprocess_parameters += command_list
        
        i = self.__counter.get()
        self.__command_log[i] = {'parameters':subprocess_parameters, 'commands':command_list}
        print(i,'\t','_run command log:',self.__command_log)
        response = subprocess.run(subprocess_parameters,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            universal_newlines = True)
        return self.__parse_reply(response,i)
        
        
    def __parse_reply(self,response,i):
        '''
        arguments: response, i
        returns: parsed response
        
        designed to be used by other functions 
        takes reply from MCM, matches it with what is expected, and converts it to programmatically-useful output
        '''
        stdout = response.stdout.strip()
        stderr = response.stderr.strip()
        if self.__verbose:
            print('args: {}\nstdout: {}\nstderr:{}'.format(response.args,response.stdout.strip(),response.stderr.strip()))
            
        self.__check_error(response,stdout)
        print(i,'\t','__parse_reply command log:',self.__command_log,'\t','response:',response,'\n')
        this_command_log = self.__command_log.pop(i)

        
        # check that the parameters from the log match the parameters from the response
        assert this_command_log['parameters'] == response.args
        
        request_type = this_command_log['commands'][0]
        return pyjanssen.response.parse(request_type,stdout)

        
    def __check_error(self,response,stdout):
        '''
        arguments: response, stdout
        
        designed to be used by other functions 
        raises CacliError if device returned an error
        '''
        if stdout == "ERROR: DEVICE NOT FOUND":
            raise CacliError("Error: {}; has another program connected to the controller?".format(stdout))
        elif stdout == "Unable to comply":
            raise CacliError("Error: {}; is controller in external input mode?")
        if response.returncode != 0:
            raise CacliError(stdout)
       
    def set_frequency(self,address,frequency):
        '''
        arguments: address, frequency
        
        in Hz, between 0 and 600
        '''
        assert frequency >= 0 and frequency <= 600
        self.__settings['frequency'][str(address)] = frequency
        
    def set_step_size(self,address,step_size):
        '''
        arguments: address, step_size
        
        in %, between 0 and 100
        '''
        assert step_size >= 0 and step_size <= 100
        self.__settings['step_size'][str(address)] = step_size
        
    def set_temperature(self,address,temperature):
        '''
        arguments: address, temperature
        
        in K, between 0 and 300
        '''
        assert temperature >= 0 and temperature <= 300
        self.__settings['temperature'][str(address)] = temperature
        
    def set_steps(self,address,steps):
        '''
        arguments: address, steps
        
        number, between 0 and 50000
        '''
        assert steps >= 0 and steps <= 50000
        self.__settings['steps'][str(address)] = steps
        
    def set_profile(self,address,profile):
        '''
        arguments: address, profile
        
        name of controller profile
        '''
        self.__settings['profile'][str(address)] = profile
        

    def frequency(self,address):
        '''
        arguments: address
        
        returns: frequency for given address
        '''
        return self.__settings['frequency'][str(address)]
        
    def step_size(self,address):
        '''
        arguments: address
        returns: step_size for given address
        '''
        return self.__settings['step_size'][str(address)]
        
    def temperature(self,address):
        '''
        arguments: address
        returns: temperature for given address
        '''
        return self.__settings['temperature'][str(address)]
        
    def steps(self,address):
        '''
        arguments: address
        returns: steps for given address
        '''
        return self.__settings['steps'][str(address)]
        
    def profile(self,address):
        '''
        arguments: address
        returns: profile for given address
        '''
        return self.__settings['profile'][str(address)]        

        
    def move(self,address,direction,channel=1,**kwargs):
        '''
        arguments: address, direction, *channel (default 1), **kwargs
        returns: dictionary of STATUS
        
        kwargs: frequency, step_size, temperature, steps, profile
        
        takes address of module to move and direction (FORWARD, BACKWARD)
        as well as optional channel if using CADM module (not CADM2!)
        plus optional kwargs to set frequency/step size/temperature
        (these values are retained)
        '''
        self._parse_settings_kwargs(address,kwargs)
        return self._move(address,channel,direction,kwargs)
    
    def _parse_settings_kwargs(self,address,kwargs):
        '''
        arguments: address, kwargs
        
        this helper function takes the kwargs for other functions and sets any 
        settings parameters contained within. takes keywords:
            frequency
            step_size
            temperature
            steps
            profile
        each input must match the conditions for set_frequency, set_step_size,
        set_temperature, set_steps, and set_profile
        '''
        if 'frequency' in kwargs:
            self.set_frequency(address,kwargs['frequency'])
        if 'step_size' in kwargs:
            self.set_step_size(address,kwargs['step_size'])
        if 'temperature' in kwargs:
            self.set_temperature(address,kwargs['temperature'])
        if 'steps' in kwargs:
            self.set_steps(address,kwargs['steps'])
        if 'profile' in kwargs:
            self.set_profile(address,kwargs['profile'])
    
    def _move(self,address,channel,direction,kwargs):
        '''
        arguments: address, channel, direction, kwargs
        returns: response
        
        kwargs: force command to run ignoring servodrive
        
        low-level move command requiring explicit channel
        '''
        self._is_servodrive(False,kwargs) #servodrive must be disabled
        return self._run('MOV',str(address),str(channel),self.profile(address),
                str(self.temperature(address)),str(direction),str(self.frequency(address)),
                str(self.step_size(address)),str(self.steps(address)))
    
    def get_position(self,address,channel=1,**kwargs):
        '''
        arguments: address, *channel (default 1)
        returns: position (integer)
        
        kwargs: force command to run ignoring servodrive
        '''
        self._is_servodrive(False,kwargs) #servodrive must be disabled
        return self._run('POS',str(address),str(channel))['POS']
    
    def get_position_raw(self,address,channel=1,**kwargs):
        '''
        arguments: address, *channel (default 1)
        returns: raw encoder value (integer)
        
        kwargs: force command to run ignoring servodrive
        
        returns 'rvl' value from POS command
        '''
        self._is_servodrive(False,kwargs) #servodrive must be disabled
        return self._run('POS',str(address),str(channel))['RVL']
        
    def get_status(self,address,**kwargs):
        '''
        arguments: address
        returns: dictionary of FAILSAFE STATE and STATUS
        
        kwargs: force command to run ignoring servodrive
        
        gets status of address
        '''
        self._is_servodrive(False,kwargs) #servodrive must be disabled
        return self._run('STS',str(address))
        
    def get_description(self,address,**kwargs):
        '''
        arguments: address
        returns: dictionary of Version and Available Channels
        
        kwargs: force command to run ignoring servodrive
        
        gets module information
        '''
        self._is_servodrive(False,kwargs) #servodrive must be disabled
        return self._run('DESC',str(address))
        
    def get_information(self,address,channel='1',**kwargs):
        '''
        arguments: address, *channel (default 1)
        returns: dictionary of TYPE and TAG
        
        kwargs: force command to run ignoring servodrive
        
        gets positioner information
        '''
        self._is_servodrive(False,kwargs) #servodrive must be disabled
        return self._run('INFO',str(address),str(channel))
        
    def stop(self,address,**kwargs):
        '''
        arguments: address
        returns: dictionary of STATUS
        
        kwargs: force command to run ignoring servodrive
        
        stops movement (Flexidrive only)
        '''
        self._is_servodrive(False,kwargs) #servodrive must be disabled
        return self._run('STP',str(address))
        
    def select_analogue_input(self,address,direction,channel=1,**kwargs):
        '''
        arguments: address, direction, *channel (default 1), **kwargs
        returns: dictionary of STATUS
        
        kwargs: frequency, step_size, temperature, steps, profile
        
        !! NOTE !! From the manual:
        The CADM2 module will perform an ‘automatic zero calibration’ upon power on to make sure the connected actuator will not move at an input voltage of o (zero) [V]14. However, this means that it is required to hold the input at 0 (zero) [V] during power on of the module (do not let the input float). 
        '''
        self._parse_settings_kwargs(address,kwargs)
        self._run('EXT',str(address),str(channel),self.profile(address),
                str(self.temperature(address)),str(direction),str(self.frequency(address)),
                str(self.step_size(address)))
        
    def reset_position(self,address,channel=1,**kwargs):
        '''
        arguments: address, *channel (default 1)
        returns: string
        
        kwargs: force command to run ignoring servodrive
        
        resets the position counter to 0
        '''
        self._is_servodrive(False,kwargs) #servodrive must be disabled
        return self._run('RST',str(address),str(channel))
        
    def autocalibrate(self,address,channel,**kwargs):
        # this is interactive and must be handled using Popen separately
        # OEMC encoder autocalibration command
        self._is_servodrive(False,kwargs) #servodrive must be disabled
        raise CacliError('command not implemented yet')

    def _is_servodrive(self,desired_state,kwargs):
        '''
        arguments: desired_state, kwargs
        
        raises error if MCM is not in desired_state, unless kwargs 
        force = True
        '''
        if 'force' in kwargs and kwargs.get('force') == True:
            return
        if self.__servodrive_enabled == desired_state:
            return
        elif self.__servodrive_enabled:
            raise CacliError('Servodrive is currently enabled and you sent a non-Servodrive command!')
        else:
            raise CacliError('Servodrive is currently disabled and you sent a Servodrive command!')
        
    def enable_servodrive(self,pgain=300,**kwargs):
        '''
        arguments: *pgain (default 300)
        returns: dictionary of STATUS
        
        uses values from channel 1 when setting TEMP, TYPE
        '''
        self.__servodrive_enabled = True
        if 'temperature' in kwargs:
            self.set_temperature('1',kwargs['temperature'])
        if 'profile' in kwargs:
            self.set_profile('1',kwargs['profile'])
        return self._run('FBEN',str(pgain),str(self.profile('1')),str(self.temperature('1')))
        
    def disable_servodrive(self):
        '''
        returns: dictionary of STATUS
        '''
        self.__servodrive_enabled = False
        return self._run('FBXT')
        
    def servodrive_go_to(self,pos1=0,pos2=0,pos3=0,**kwargs):
        '''
        arguments: *pos1, *pos2, *pos3 (set 0 if not connected)
        returns: dictionary of STATUS
        '''
        self._is_servodrive(True,kwargs)
        return self._run('FBCS',str(pos1),str(pos2),str(pos3))
        
    def servodrive_emergency_stop(self,**kwargs):
        '''
        returns: dictionary of STATUS
        '''
        self._is_servodrive(True,kwargs)
        return self._run('FBES')
        
    def servodrive_find_end_stops(self,direction,filter,zero,**kwargs):
        '''
        arguments: direction, filter, zero
        returns: dictionary of STATUS
        
        direction: FORWARD or BACKWARD 
        filter: integer, 1-20, velocity polling delay (relative)
        zero: boolean, reset position after completion
        '''
        self._is_servodrive(True,kwargs)
        return self._run('FBFE',str(direction),str(filter),str(int(zero)))
        
    def servodrive_status_position(self,**kwargs):
        '''
        returns: dictionary of STATUS, ENABLED, BUSY, POS1, POS2, POS3, ERR1, ERR2, ERR3
        
        ENABLED is 0 (disabled), 1 (enabled), 2 (find end stop active)
        BUSY is 1 if minimizing error between setpoint and current point
        POSx is current position information for each
        ERRx is the difference between current position and target position
        '''
        self._is_servodrive(True,kwargs)
        return self._run('FBST')
        
        
class CacliError(Exception):
    # Exception when returncode != 0
    def __init__(self,error):
        self.error = error
        
    def __str__(self):
        return repr(self.error)
    
