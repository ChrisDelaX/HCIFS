# HCIFS
High Contrast Integral Field Spectrograph

Quick Start Guide
-------------------------------

```ruby
import hcifs, hcifs.experiment, os.path
from hcifs.experiment import Experiment

# select a JSON file containing your input parameters
jsonfile = os.path.join(hcifs.__path__[0],'scripts','sampleScript_Lab_FPWC.json')

# create a HCIFS experiment 
expt = Experiment(jsonfile)

# run a lab experiment
expt.runLaboratory()
# run a simulation
expt.runSimulation()
```
