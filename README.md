# HCIFS
High Contrast Integral Field Spectrograph

Requirements
-------------------------------
The following python packages are required:
* win32com	--	for Windows only, allows to control the camera
* json		--	for scriptfiles
* astropy	--	for units mainly


Quick Start Guide
-------------------------------

```ruby
import hcifs
from hcifs.experiment import Experiment

# create an HCIFS Experiment 
expt = Experiment('sampleScript_Lab_FPWC')

# run a lab experiment
expt.runLaboratory()
# run a simulation
expt.runSimulation()
```
