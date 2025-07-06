# Data Centers Carbon Emissions at Crossroads: An Empirical Study

A repository for projecting Global, US, and per-state emissions at 2030. Read our paper [here]().

## Data

### Data Center Electricity Demand Data

Data center electricity demand data (estimates and projections) are obtained from the following sources:

US data cneter data: [LBNL](https://escholarship.org/uc/item/32d6m0d1), [EPRI](https://www.epri.com/research/products/000000003002028905) (EPRI data inclused US states).

Global data center data: [IEA](https://www.iea.org/reports/energy-and-ai), [Koot et al.](https://www.sciencedirect.com/science/article/pii/S0306261921003019)

The relevant files are in the ```data/electricity-demand/``` folder.

File naming convention: \<source\>-\<region\>-\<granularity\>-CI.xlsx. For example, EMaps-EU-annual-CI.xlsx.

Each file has a Metadata sheet explaining the contents of the file.

### Carbon Intensity Data

Carbon Intensity data is obtained from [Electricity Maps](https://portal.electricitymaps.com/datasets) and [Ember](https://ember-energy.org/data/yearly-electricity-data/). The relevant files are in the ```data/carbon-intensity/``` folder.

File naming convention: \<source\>-\<region\>-\<granularity\>-demand.xlsx. For example, LBNL-US-annual-demand.xlsx.

Each file has a Metadata sheet explaining the contents of the file.

## Emission Analysis

The code will be uploaded soon.

### Plots
All the plots in the paper can be reproduced by running ```src/plots.ipynb``` file. We suggest creating a Python virtual environment and installing the packages listed in the ```requirements.txt``` file first to avoid any package-related errors.

## Citing Our Paper
If you use our analyses/dataset for your work, please consider citing our paper. The BibTex format is as follows: <br>
&nbsp; &nbsp; &nbsp; &nbsp;@inproceedings{maji2025data,<br>
&nbsp; &nbsp; &nbsp; &nbsp;  title={Data Centers Carbon Emissions at Crossroads: An Empirical Study},<br>
&nbsp; &nbsp; &nbsp; &nbsp;  author={Maji, Diptyaroop and Hanafy, Walid A and Wu, Li and Irwin, David and Shenoy, Prashant and Sitaraman, Ramesh K},<br>
&nbsp; &nbsp; &nbsp; &nbsp;  booktitle={},<br>
&nbsp; &nbsp; &nbsp; &nbsp;  pages={},<br>
&nbsp; &nbsp; &nbsp; &nbsp;  year={2025}<br>
&nbsp; &nbsp; &nbsp; &nbsp;}<br>

## Acknowledgements
This work is part of the [CoDec]((https://codecexp.us/)) project, supported by National Science Foundation (NSF) grants 2213636, 2105494, 2211302, 2211888, 2325956, the U.S. Department of Energy Award DE-EE0010143, and support from VMware. This work used Amazon Web Services through the CloudBank, which is supported by NSF grant 19250001.


