# Data Centers Carbon Emissions at Crossroads: An Empirical Study

A repository for projecting Global, US, and per-state emissions in 2030. Read our paper [here]().

## Data

### Data Center Electricity Demand Data

Data center electricity demand data (estimates and projections) are obtained from the following sources:<br>
US data center data: [LBNL](https://escholarship.org/uc/item/32d6m0d1), [EPRI](https://www.epri.com/research/products/000000003002028905) (EPRI data includes US states).<br>
Global data center data: [IEA](https://www.iea.org/reports/energy-and-ai), [Koot et al.](https://www.sciencedirect.com/science/article/pii/S0306261921003019)

The relevant files are in the ```data/electricity-demand/``` folder.<br>
File naming convention: \<source\>-\<region\>-\<granularity\>-CI.xlsx. For example, EMaps-EU-annual-CI.xlsx.<br>
Each file has a Metadata sheet explaining the contents of the file.

### Carbon Intensity Data

Carbon Intensity (CI) data is obtained from the following sources:<br>
US CI data (including states): [Electricity Maps](https://portal.electricitymaps.com/datasets), [Ember](https://ember-energy.org/data/yearly-electricity-data/).<br>
Global CI data: [Ember](https://ember-energy.org/data/yearly-electricity-data/). 

The relevant files are in the ```data/carbon-intensity/``` folder.<br>
File naming convention: \<source\>-\<region\>-\<granularity\>-demand.xlsx. For example, LBNL-US-annual-demand.xlsx.<br>
Each file has a Metadata sheet explaining the contents of the file.

## Emission Analysis

All the analyses (US, Global, US states) can be reproduced using the ```src/emissionAnalysis.py``` file and selecting the appropriate analysis number as follows:<br>
1. US Emissions based on LBNL and EMaps data.
2. US Emissions based on LBNL and Ember data.
3. US Emissions based on EPRI and EMaps data.
4. US Emissions based on EPRI and Ember data.
5. Global Emissions based on IEA and Ember data.
6. Global Emissions based on IEA (w/ LBNL CAGR) and Ember data.
7. Global Emissions based on Koot et al. and Ember data.
8. US Statewise Emissions based on EPRI and EMaps data (different CAGR).
9. US Statewise Emissions for alternate demand scenarios.


The results are in ```data/emissions.xlsx``` file. Please refer to the metadata in ```data/emissions.xlsx``` for more details about the results.

### Plots
All the plots in the paper can be reproduced by running ```src/plots.ipynb``` file. The data for the plots are derived from ```data/emissions.xlsx``` and curated for each plot. 
The curated datasets can be found in ```plots/plot-data```.

We suggest creating a Python virtual environment and installing the packages listed in the ```requirements.txt``` file first to avoid any package-related errors.

## Citing Our Paper
If you use our analyses/dataset for your work, please consider citing our paper. The BibTex format is as follows: <br>
```bash
@inproceedings{maji2025data,
    title={Data Centers Carbon Emissions at Crossroads: An Empirical Study},
    author={Maji, Diptyaroop and Hanafy, Walid A and Wu, Li and Irwin, David and Shenoy, Prashant and Sitaraman, Ramesh K},
    booktitle={},
    pages={},
    year={2025}
}
```


## Acknowledgements
This work is part of the [CoDec]((https://codecexp.us/)) project, supported by National Science Foundation (NSF) grants 2213636, 2105494, 2211302, 2211888, 2325956, the U.S. Department of Energy Award DE-EE0010143, and support from VMware. This work used Amazon Web Services through the CloudBank, which is supported by NSF grant 19250001.


