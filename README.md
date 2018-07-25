# HCIFS 
High Contrast Integral Field Spectrograph 

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)

Requirements
-------------------------------
Using the free and open source Anaconda Python Distribution is recommended. It already contains the ``astropy`` package, and simplifies package management and deployment.

To run a laboratory experiment, the following python packages must be installed:
* ``win32com`` --- allows to control the camera (works on Windows only)
* ``serial`` ----- allows controlling the laser and filter wheel
* ``bmc`` -------- allows controlling the DMs (courtesy of Boston Micromachines Corporation)
* ``PyAPT`` ------ allows controlling the motorized stages (also requires ``APT.dll`` and ``APT.lib`` from https://github.com/mcleu/PyAPT/tree/master/APTDLLPack/DLL)

Quick Start Guide
-------------------------------

```python
import HCIFS
from HCIFS.Experiment import Experiment

# create an HCIFS Experiment 
expt = Experiment('sampleScript_Lab_FPWC')

# run a lab experiment
expt.runLab()
# run a simulation
expt.runSim()
```

Acknowledgements
-------------------------------
Created by Christian Delacroix

Written by Matthew Grossman, He Sun, Katherine Mumm, and Christian Delacroix.
