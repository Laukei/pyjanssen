# pyjanssen

A Python library for interfacing with the MCM module by Janssen Precision Engineering via cacli.exe (provided on [the Janssen website](https://www.janssenprecisionengineering.com/page/cryo-positioning-systems-controller/))

## Usage

Standard import syntax: `from pyjanssen import MCM, FORWARD, BACKWARD`

Class MCM wraps `cacli.exe` provided by Janssen Precision Engineering for control of their low temperature piezoelectric positioners.

Example usage can be seen in `test.py`.
