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
expt = Experiment('sampleScript')

# run wavefront control in imaging mode (QSI camera)
expt.runFPWC('Imag')
# run wavefront control in spectrograph mode (IFS)
expt.runFPWC('Spec')

# generate a datacube using the IFS
expt.getDatacube()
```

Publications
-------------------------------
* The shaped pupil coronagraph for planet finding coronagraphy: optimization, sensitivity, and laboratory testing, Kasdin et al. 2004
* Optimal dark hole generation via two deformable mirrors with stroke minimization, Pueyo et al. 2009
* Kalman filtering techniques for focal plane electric field estimation, Groff and Kasdin 2013
* Recursive starlight and bias estimation for high-contrast imaging with an extended Kalman filter, Riggs, Kasdin, and Groff 2016
* Methods and limitations of focal plane sensing, estimation, and control in high-contrast imaging, Groff et al. 2015
* Identification of the focal plane wavefront control system using EM algorithm, Sun, Kasdin, and Vanderbei 2017
* First light of the High Contrast Integral Field Spectrograph (HCIFS), Delacroix, Sun, Galvin, et al. 2018

Acknowledgements
-------------------------------
Created by Christian Delacroix

Written by Matthew Grossman, He Sun, and Christian Delacroix.
