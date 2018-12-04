# pyjanssen

An object-oriented Python library for interfacing with the MCM module by Janssen Precision Engineering via cacli.exe (provided on [the Janssen website](https://www.janssenprecisionengineering.com/page/cryo-positioning-systems-controller/)). Implements all functions except autocalibration (as it is interactive).

## Usage

Linear positioner import syntax: `from pyjanssen import MCM, FORWARD, BACKWARD`

Rotational positioner import syntax: `from pyjanssen import MCM, CW, CCW`

Class MCM provides an object-oriented wrapper for `cacli.exe` provided by Janssen Precision Engineering for control of their low temperature piezoelectric positioners

Example usage:

```python
from pyjanssen import MCM, FORWARD, BACKWARD

m = MCM() # connect to the Janssen MCM using cacli.exe in current directory
m.move(1, FORWARD) # moves in positive direction
m.move(2, BACKWARD, frequency=10, step_size=50, temperature=293, steps=100, profile='PROFILE1') # moves in negative direction; sets new frequency, step_size, temperature, steps, and profile config
print(m.get_position(1)) # ask the MCM for the position of axis 1 (requires OEM2 module)
```

## API Reference

### MCM(device=None, \*\*kwargs)

arguments: \*device (default None) to specify specific MCM module if multiple
returns: MCM instance

kwargs: exe (string) to specify path to cacli.exe if not in current directory
        server (bool) to specify use of cacli.exe in server mode (good for fast command responses)
        verbose (bool) to output commands and responses from cacli.exe for debugging

#### autocalibrate(self, address, channel, \*\*kwargs)

*Not implemented (needs input/output)*

#### disable_servodrive(self)

returns: dictionary of STATUS

#### enable_servodrive(self, pgain=300, \*\*kwargs)

arguments: \*pgain (default 300)
returns: dictionary of STATUS
 
uses values from channel 1 when setting TEMP, TYPE

#### frequency(self, address)

arguments: address
returns: frequency for given address

#### get_description(self, address, \*\*kwargs)
arguments: address
returns: dictionary of Version and Available Channels
 
kwargs: `force` command to run ignoring servodrive
gets module information

#### get_information(self, address, channel='1', \*\*kwargs)

arguments: address, \*channel (default 1)
returns: dictionary of TYPE and TAG
 
kwargs: force command to run ignoring servodrive
 
gets positioner information

#### get_position(self, address, channel=1, \*\*kwargs)

arguments: address, \*channel (default 1)
returns: position (integer)
 
kwargs: force command to run ignoring servodrive

#### get_position_raw(self, address, channel=1, \*\*kwargs)
arguments: address, \*channel (default 1)
returns: raw encoder value (integer)
 
kwargs: force command to run ignoring servodrive
 
returns 'rvl' value from POS command

#### get_status(self, address, \*\*kwargs)

arguments: address
returns: dictionary of FAILSAFE STATE and STATUS
 
kwargs: force command to run ignoring servodrive
 
gets status of address

#### move(self, address, direction, channel=1, \*\*kwargs)

arguments: address, direction, \*channel (default 1), \*\*kwargs
returns: dictionary of STATUS
 
kwargs: frequency, step_size, temperature, steps, profile
 
takes address of module to move and direction (FORWARD, BACKWARD)
as well as optional channel if using CADM module (not CADM2!)
plus optional kwargs to set frequency/step size/temperature
(these values are retained)

#### profile(self, address)

arguments: address
returns: profile for given address
reset_position(self, address, channel=1, \*\*kwargs)
arguments: address, \*channel (default 1)
returns: string
 
kwargs: force command to run ignoring servodrive
 
resets the position counter to 0

#### select_analogue_input(self, address, direction, channel=1, \*\*kwargs)

arguments: address, direction, \*channel (default 1), \*\*kwargs
returns: dictionary of STATUS
 
kwargs: frequency, step_size, temperature, steps, profile
 
!! NOTE !! From the manual:
The CADM2 module will perform an ‘automatic zero calibration’ upon power on to make sure the connected actuator will not move at an input voltage of o (zero) [V]14. However, this means that it is required to hold the input at 0 (zero) [V] during power on of the module (do not let the input float).

#### servodrive_emergency_stop(self, \*\*kwargs)

returns: dictionary of STATUS
servodrive_find_end_stops(self, direction, filter, zero, \*\*kwargs)
arguments: direction, filter, zero
returns: dictionary of STATUS
 
direction: FORWARD or BACKWARD 
filter: integer, 1-20, velocity polling delay (relative)
zero: boolean, reset position after completion

#### servodrive_go_to(self, pos1=0, pos2=0, pos3=0, \*\*kwargs)

arguments: \*pos1, \*pos2, \*pos3 (set 0 if not connected)
returns: dictionary of STATUS
servodrive_status_position(self, \*\*kwargs)
returns: dictionary of STATUS, ENABLED, BUSY, POS1, POS2, POS3, ERR1, ERR2, ERR3
 
ENABLED is 0 (disabled), 1 (enabled), 2 (find end stop active)
BUSY is 1 if minimizing error between setpoint and current point
POSx is current position information for each
ERRx is the difference between current position and target position

#### set_frequency(self, address, frequency)

arguments: address, frequency
 
in Hz, between 0 and 600

#### set_profile(self, address, profile)

arguments: address, profile
 
name of controller profile

#### set_step_size(self, address, step_size)

arguments: address, step_size
 
in %, between 0 and 100

#### set_steps(self, address, steps)

arguments: address, steps
 
number, between 0 and 50000

#### set_temperature(self, address, temperature)

arguments: address, temperature
 
in K, between 0 and 300

#### step_size(self, address)

arguments: address
returns: step_size for given address

#### steps(self, address)

arguments: address
returns: steps for given address

#### stop(self, address, \*\*kwargs)

arguments: address
returns: dictionary of STATUS
 
kwargs: force command to run ignoring servodrive
 
stops movement (Flexidrive only)

#### temperature(self, address)

arguments: address
returns: temperature for given address