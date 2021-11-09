### Qopen tutorial

Qopen includes already a small tutorial which can be loaded with the `qopen create --tutorial` command. The tutorial in this repository is a bit larger and has a proper readme (this file).
In the metadata folder you will find a StationXML file with station meta data and an earthquake catalog in PHA format including picks of 17 events. The data folder contains the waveform data.
The plugin option in `conf.json` is used to load the data. The corresponding python module `data.py` loads the data and returns the requested waveforms. The `matplotlibrc` file changes some of matplotlib's standard options.
The same could be achieved by changing the plotting options in `conf.json`. The configuration file in this tutorial is not as heavily documented as the standard configuration file which can be created with the `qopen create` command.

Because qopen will be run several times, we will save results in different folders using the `--prefix` option. Please also check other commands and options with `qopen -h` and `qopen {cmd} -h`.
Most command line options can also be set in the config file and vice versa.
The documentation for these options can be found directly on the command line (`-h`), inside the default config file and finally in the [API documentation](https://qopen.readthedocs.io) (search).

We start by calling qopen with:
```
qopen go -v --prefix "01_go/"
```
If you are impatient you can also use only the 4 largest events by filtering the catalog beforehand:
```
qopen go -v --filter-events '["magnitude > 3.1"]' --prefix "01_go/"
```
We can pass up to 3 `-v` flags to the commands to get more verbose output on the command line. If something goes wrong you can check the log output for errors or warnings.
The following files and folders are created by this command:
```
$ ls 01_go
log.txt  mags.pdf  plots  results.json  results.pdf  sds.pdf  sites.pdf
```
Individual plots are located in the `plots` directory. The PDFs are aggregated plots. Additionally, a log file and a JSON file with all results is created. For example, plotting the Q values can be done by loading the results from the JSON file:
```python
import json
import matplotlib.pyplot as plt
import numpy as np

with open('results.json') as f:
    r = json.load(f)
v = 3400
f = np.array(r['freq'])
Qi = 2 * np.pi * f / np.array(r['b'])
Qsc = 2 * np.pi * f / (np.array(r['g0']) * v)

plt.loglog(f, 1 / Qi, label='Qi^-1')
plt.loglog(f, 1 / Qsc, label='Qsc^-1')
plt.xlabel('freq (Hz)')
plt.ylabel('inverse Q')
plt.legend()
plt.show()
```
Estimates for site amplification and source spectra are already created by `qopen go` command.
Still, in most cases it might be beneficial to recalculate site amplifications and source spectra with the `qopen fixed` command using fixed attenuation parameters if one is interested in these parameters.
The `qopen source` command can take this approach one step further by fixing attenuation and site amplification.
This approach can even be used to calculate source spectra of (new) earthquakes not analyzed with the previous commands, see the flowchart in the file `qopen_flow.pdf`.
The processing can be speeded up by disabling som of the plots (via command line or in the config file).
Possible calls to the relevant sub commands:
```
qopen fixed --input "01_go/results.json" --align-sites --prefix "02_sites/"
qopen source --input "01_go/results.json" --input-sites "02_sites/results.json" --prefix "03_source/"
```

Complementary to this tutorial, please have a look at the readme in the Qopen repository and the articles referenced therein.

Reference for the data used in this tutorial: WEBNET group, Martin Bachura & Laura Barth (2020), Seismological dataset for 2018 West Bohemia earthquake swarm, doi: [10.5281/zenodo.3741464](https://doi.org/10.5281/zenodo.3741464)
