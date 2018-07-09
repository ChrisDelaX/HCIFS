# HCIFS
High Contrast Integral Field Spectrograph

Quick Start Guide
-------------------------------

```ruby
import HCIFS, HCIFS.Experiment, os.path
JSONfile = os.path.join(HCIFS.__path__[0],'Scripts','sampleScript_Lab_FPWC.json')
# create an experiment
expt = HCIFS.Experiment.Experiment(JSONfile)
# run a lab experiment
expt.runLaboratory()
# run a simulation
expt.runSimulation()
```
