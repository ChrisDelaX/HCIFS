# HCIFS
High Contrast Integral Field Spectrograph

Requirements
-------------------------------
The following python packages are required:
* ``json`` ------- format used for scriptfiles
* ``astropy`` ---- allows using units and quantities
* ``win32com`` --- allows to control the camera (works on Windows only)
* ``serial`` ----- allows controlling the laser and filter wheel
* ``PyAPT`` ------ allows controlling the motorized stages (also requires ``APT.dll`` and ``APT.lib`` from ``https://github.com/mcleu/PyAPT/tree/master/APTDLLPack/DLL``


Quick Start Guide
-------------------------------

```python
import HCIFS
from HCIFS.Experiment import Experiment

# create an HCIFS Experiment 
expt = Experiment('sampleScript_Lab_FPWC')

# run a lab experiment
expt.runLaboratory()
# run a simulation
expt.runSimulation()
```

Acknowledgements
-------------------------------
Created by Christian Delacroix

Written by Matthew Grossman, He Sun, Katherine Mumm, and Christian Delacroix.
