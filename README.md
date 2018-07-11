# HCIFS
High Contrast Integral Field Spectrograph

Requirements
-------------------------------
The following python packages are required:
* ``win32com``	--	for Windows only, allows to control the camera
* ``json``		--	for scriptfiles
* ``astropy``	--	for units mainly


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
