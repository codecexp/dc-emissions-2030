import numpy as np
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

G_PER_KWH_TO_G_PER_MWH_CONVERTER = 1e3
G_PER_KWH_TO_G_PER_TWH_CONVERTER = 1e9
G_TO_MEGATON = 1e-12


EPRI_YEAR_RANGE = [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
LBNL_YEAR_RANGE = [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
KOOT_YEAR_RANGE = [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
IEA_YEAR_RANGE = [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]

# LBNL US DC Emissions (whole US)
def analyzeLBNLUSEmissions(energyFile, ciFile, ciSource="emaps"):
    energyData = pd.read_excel(energyFile, header=0, sheet_name="Table 1") # load is in TWh/year

    for year in LBNL_YEAR_RANGE:
        print(year)
        row = energyData[energyData["Year"] == year]

        # For Energy
        yearEnergyValues = np.array([row["LBNL_BEST"].values[0], row["LBNL_WORST"].values[0]])

        # For CI
        if (ciSource == "emaps"):
            ciData = pd.read_excel(ciFile, header=[0, 1], sheet_name="Table 2") # CI is in gCO2eq/kWh
            if (year < 2025):
                yearCIValues = ciData[("Annual Avg CI (lifecycle, ground truth)", year)].values[-1:] # only US CI
                if (len(yearEnergyValues.shape)>1):
                    yearCIValues = np.tile(yearCIValues, (yearEnergyValues.shape[1], 1)).T
                emissions = np.multiply(yearEnergyValues, yearCIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
            else:
                method1CIValues = ciData[("Projected Avg CI (lifecycle, No Change)", year)].values[-1:] # only US CI
                method2CIValues = ciData[("Projected Avg CI (lifecycle, Current Decarbonization)", year)].values[-1:] # only US CI
                method3CIValues = ciData[("Projected Avg CI (lifecycle, Zero Carbon 2050)", year)].values[-1:] # only US CI

                if (len(yearEnergyValues.shape)>1):
                    method1CIValues = np.tile(method1CIValues, (yearEnergyValues.shape[1], 1)).T
                    method2CIValues = np.tile(method2CIValues, (yearEnergyValues.shape[1], 1)).T
                    method3CIValues = np.tile(method3CIValues, (yearEnergyValues.shape[1], 1)).T
                method1Emissions = np.multiply(yearEnergyValues, method1CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method2Emissions = np.multiply(yearEnergyValues, method2CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method3Emissions = np.multiply(yearEnergyValues, method3CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
        else: 
            #ciSource == "ember"
            yearEnergyValues = yearEnergyValues[-1:] # only Total US
            ciData = pd.read_excel(ciFile, header=[0, 1], sheet_name="Table 1") # CI is in gCO2eq/kWh
            ciData = ciData.loc[ciData[("Year", "Unnamed: 1_level_1")] == year]

            if (year < 2025):
                yearCIValues = np.array(ciData[("Annual Avg CI", "Grount Truth")].values)
                if (len(yearEnergyValues.shape)>1):
                    yearCIValues = np.tile(yearCIValues, (yearEnergyValues.shape[1], 1)).T
                emissions = np.multiply(yearEnergyValues, yearCIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
            else:
                method1CIValues = ciData[("Annual Avg CI", "No Change")].values
                method2CIValues = ciData[("Annual Avg CI", "Current Decarbonization")].values
                method3CIValues = ciData[("Annual Avg CI", "Zero Carbon 2050")].values

                if (len(yearEnergyValues.shape)>1):
                    method1CIValues = np.tile(method1CIValues, (yearEnergyValues.shape[1], 1)).T
                    method2CIValues = np.tile(method2CIValues, (yearEnergyValues.shape[1], 1)).T
                    method3CIValues = np.tile(method3CIValues, (yearEnergyValues.shape[1], 1)).T
                method1Emissions = np.multiply(yearEnergyValues, method1CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method2Emissions = np.multiply(yearEnergyValues, method2CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method3Emissions = np.multiply(yearEnergyValues, method3CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq

        # print(yearEnergyValues)
        if (year < 2025):
            # print(yearCIValues)
            print(emissions)
        else:
            # print(method1CIValues)
            print(method1Emissions)
            print(method2Emissions)
            print(method3Emissions)
    return

# EPRI US DC Emissions (whole US & top 15 states with most DC load)
def analyzeEPRIUSEmissions(energyFile, ciFile, ciSource="emaps"):
    energyData = pd.read_excel(energyFile, header=[0, 1], sheet_name="Table 1") # load is in MWh/year

    for year in EPRI_YEAR_RANGE:
        print(year)

        # For Energy
        if (year < 2024):
            yearEnergyValues = energyData[(f"{year} load", "(Mwh/y)")].values
        else:
            yearEnergyValues = energyData[f"{year} load"].values

        # For CI
        if (ciSource == "emaps"):
            ciData = pd.read_excel(ciFile, header=[0, 1], sheet_name="Table 2") # CI is in gCO2eq/kWh
            if (year < 2025):
                yearCIValues = ciData[("Annual Avg CI (lifecycle, ground truth)", year)].values
                if (len(yearEnergyValues.shape)>1):
                    yearCIValues = np.tile(yearCIValues, (yearEnergyValues.shape[1], 1)).T
                emissions = np.multiply(yearEnergyValues, yearCIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
            else:
                method1CIValues = ciData[("Projected Avg CI (lifecycle, No Change)", year)].values
                method2CIValues = ciData[("Projected Avg CI (lifecycle, Current Decarbonization)", year)].values
                method3CIValues = ciData[("Projected Avg CI (lifecycle, Zero Carbon 2050)", year)].values

                if (len(yearEnergyValues.shape)>1):
                    method1CIValues = np.tile(method1CIValues, (yearEnergyValues.shape[1], 1)).T
                    method2CIValues = np.tile(method2CIValues, (yearEnergyValues.shape[1], 1)).T
                    method3CIValues = np.tile(method3CIValues, (yearEnergyValues.shape[1], 1)).T
                method1Emissions = np.multiply(yearEnergyValues, method1CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method2Emissions = np.multiply(yearEnergyValues, method2CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method3Emissions = np.multiply(yearEnergyValues, method3CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
        else: 
            #ciSource == "ember"
            yearEnergyValues = yearEnergyValues[-1:] # only Total US
            ciData = pd.read_excel(ciFile, header=[0, 1], sheet_name="Table 1") # CI is in gCO2eq/kWh
            ciData = ciData.loc[ciData[("Year", "Unnamed: 1_level_1")] == year]

            if (year < 2025):
                yearCIValues = np.array(ciData[("Annual Avg CI", "Grount Truth")].values)
                if (len(yearEnergyValues.shape)>1):
                    yearCIValues = np.tile(yearCIValues, (yearEnergyValues.shape[1], 1)).T
                emissions = np.multiply(yearEnergyValues, yearCIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
            else:
                method1CIValues = ciData[("Annual Avg CI", "No Change")].values
                method2CIValues = ciData[("Annual Avg CI", "Current Decarbonization")].values
                method3CIValues = ciData[("Annual Avg CI", "Zero Carbon 2050")].values

                if (len(yearEnergyValues.shape)>1):
                    method1CIValues = np.tile(method1CIValues, (yearEnergyValues.shape[1], 1)).T
                    method2CIValues = np.tile(method2CIValues, (yearEnergyValues.shape[1], 1)).T
                    method3CIValues = np.tile(method3CIValues, (yearEnergyValues.shape[1], 1)).T
                method1Emissions = np.multiply(yearEnergyValues, method1CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method2Emissions = np.multiply(yearEnergyValues, method2CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method3Emissions = np.multiply(yearEnergyValues, method3CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq

        # print(yearEnergyValues)
        if (year < 2025):
            # print(yearCIValues)
            print(emissions)
        else:
            # print(method1CIValues)
            print(method1Emissions)
            print(method2Emissions)
            print(method3Emissions)

            
    return

# Global DC Emissions based on DC load estimates by IEA
def analyzeIEAGlobalEmissions(energyFile, ciFile, ciSource, lbnlCagr=False):
    energyData = pd.read_excel(energyFile, header=0, sheet_name="Table 1") # load is in TWh/year
    if (lbnlCagr is True):
        energyData = pd.read_excel(energyFile, header=0, sheet_name="Table 2") # load is in TWh/year

    for year in IEA_YEAR_RANGE:
        print(year)
        row = energyData[energyData["Year"] == year]

        # For Energy
        if (year < 2025):
            yearEnergyValues = np.array([row["Historical"].values[0]])
        else:
            if (lbnlCagr is False):
                yearEnergyValues = np.array([row["Base"].values[0], row["High Efficiency"].values[0], row["Headwinds"].values[0], row["Lift-Off"].values[0]])
            else:
                yearEnergyValues = np.array([row["Projection_LBNL_best"].values[0], row["Projection_LBNL_worst"].values[0]])
        # print(yearEnergyValues)

        # For CI
        if (ciSource == "ember"):
            ciData = pd.read_excel(ciFile, header=[0, 1], sheet_name="Table 1") # CI is in gCO2eq/kWh
            ciData = ciData.loc[ciData[("Year", "Unnamed: 1_level_1")] == year]

            if (year < 2025):
                yearCIValues = np.array(ciData[("Annual Avg CI", "Grount Truth")].values)
                if (len(yearEnergyValues.shape)>1):
                    yearCIValues = np.tile(yearCIValues, (yearEnergyValues.shape[1], 1)).T
                emissions = np.multiply(yearEnergyValues, yearCIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
            else:
                method1CIValues = ciData[("Annual Avg CI", "No Change")].values
                method2CIValues = ciData[("Annual Avg CI", "Current Decarbonization")].values
                method3CIValues = ciData[("Annual Avg CI", "Zero Carbon 2050")].values

                if (len(yearEnergyValues.shape)>1):
                    method1CIValues = np.tile(method1CIValues, (yearEnergyValues.shape[1], 1)).T
                    method2CIValues = np.tile(method2CIValues, (yearEnergyValues.shape[1], 1)).T
                    method3CIValues = np.tile(method3CIValues, (yearEnergyValues.shape[1], 1)).T
                method1Emissions = np.multiply(yearEnergyValues, method1CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method2Emissions = np.multiply(yearEnergyValues, method2CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method3Emissions = np.multiply(yearEnergyValues, method3CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq

        np.set_printoptions(precision=2)
        if (year < 2025):
            print(emissions)
        else:
            print(method1Emissions)
            print(method2Emissions)
            print(method3Emissions)
    return

# Global DC Emissions based on estimates by Koot et al.
def analyzeKootGlobalEmissions(energyFile, ciFile, ciSource="emaps"):
    energyData = pd.read_excel(energyFile, header=0, sheet_name="Table 1") # load is in TWh/year

    for year in KOOT_YEAR_RANGE:
        print(year)
        row = energyData[energyData["Year"] == year]

        # For Energy
        yearEnergyValues = np.array([row["99% Lower"].values[0], row["Median"].values[0], row["99% Upper"].values[0]])

        # For CI
        if (ciSource == "ember"):
            ciData = pd.read_excel(ciFile, header=[0, 1], sheet_name="Table 1") # CI is in gCO2eq/kWh
            ciData = ciData.loc[ciData[("Year", "Unnamed: 1_level_1")] == year]

            if (year < 2025):
                yearCIValues = np.array(ciData[("Annual Avg CI", "Grount Truth")].values)
                if (len(yearEnergyValues.shape)>1):
                    yearCIValues = np.tile(yearCIValues, (yearEnergyValues.shape[1], 1)).T
                emissions = np.multiply(yearEnergyValues, yearCIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
            else:
                method1CIValues = ciData[("Annual Avg CI", "No Change")].values
                method2CIValues = ciData[("Annual Avg CI", "Current Decarbonization")].values
                method3CIValues = ciData[("Annual Avg CI", "Zero Carbon 2050")].values

                if (len(yearEnergyValues.shape)>1):
                    method1CIValues = np.tile(method1CIValues, (yearEnergyValues.shape[1], 1)).T
                    method2CIValues = np.tile(method2CIValues, (yearEnergyValues.shape[1], 1)).T
                    method3CIValues = np.tile(method3CIValues, (yearEnergyValues.shape[1], 1)).T
                method1Emissions = np.multiply(yearEnergyValues, method1CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method2Emissions = np.multiply(yearEnergyValues, method2CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
                method3Emissions = np.multiply(yearEnergyValues, method3CIValues) * G_PER_KWH_TO_G_PER_TWH_CONVERTER * G_TO_MEGATON # in MtCO2eq

            # print(yearEnergyValues)
            if (year < 2025):
                # print(yearCIValues)
                print(np.round(emissions, 2))
            else:
                # print(method1CIValues)
                print(np.round(method1Emissions, 2))
                print(np.round(method2Emissions, 2))
                print(np.round(method3Emissions, 2))
    return

def analyzeStateEmissionsDifferentCAGR(energyFile, ciFile):
    energyData = pd.read_excel(energyFile, header=0, sheet_name="Table 3") # load is in MWh/year
    cagrData = pd.read_excel(energyFile, header=0 , sheet_name="Table 3")
    cagrValues = cagrData["CAGR"].values
    yearEnergyValues = energyData["2023 Load"].values

    for year in EPRI_YEAR_RANGE:
        print(year)
        if (year > 2023):
            yearCAGR = (1+cagrValues*1.0/100)
            for i in range(len(yearEnergyValues)):
                yearEnergyValues[i] = yearEnergyValues[i]*1.0*yearCAGR[i]
        
        ciData = pd.read_excel(ciFile, header=[0, 1], sheet_name="Table 2") # CI is in gCO2eq/kWh
        if (year < 2025):
            yearCIValues = ciData[("Annual Avg CI (lifecycle, ground truth)", year)].values
            if (len(yearEnergyValues.shape)>1):
                yearCIValues = np.tile(yearCIValues, (yearEnergyValues.shape[1], 1)).T
            emissions = np.multiply(yearEnergyValues, yearCIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
        else:
            method1CIValues = ciData[("Projected Avg CI (lifecycle, No Change)", year)].values
            method2CIValues = ciData[("Projected Avg CI (lifecycle, Current Decarbonization)", year)].values
            method3CIValues = ciData[("Projected Avg CI (lifecycle, Zero Carbon 2050)", year)].values

            if (len(yearEnergyValues.shape)>1):
                method1CIValues = np.tile(method1CIValues, (yearEnergyValues.shape[1], 1)).T
                method2CIValues = np.tile(method2CIValues, (yearEnergyValues.shape[1], 1)).T
                method3CIValues = np.tile(method3CIValues, (yearEnergyValues.shape[1], 1)).T
            method1Emissions = np.multiply(yearEnergyValues, method1CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
            method2Emissions = np.multiply(yearEnergyValues, method2CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
            method3Emissions = np.multiply(yearEnergyValues, method3CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq

        print(energyData["State"].values)
        if (year < 2025):
            print(np.round(emissions, 2))
        else:
            print(np.round(method1Emissions, 2))
            print(np.round(method2Emissions, 2))
            print(np.round(method3Emissions, 2))
    return

def minimizeEmissionIncrease(energyFile, ciFile, cagrLimit=30, year=2030, topKStates=10):
    print("CAGR limit = ", cagrLimit)
    energyData = pd.read_excel(energyFile, header=0, sheet_name="Table 3") # load is in MWh/year
    cagrData = pd.read_excel(energyFile, header=0 , sheet_name="Table 3")
    cagrValues = cagrData["CAGR"].values
    yearEnergyValues = energyData["2023 Load"].values[:topKStates]
    states = energyData["State"].values
    total2023Energy = np.sum(yearEnergyValues)
    energyValues2030 = yearEnergyValues.copy()
    energyValues2030 = energyValues2030.astype(np.float64)
    for i in range(len(yearEnergyValues)):
        energyValues2030[i] = yearEnergyValues[i]*1.0*(1+cagrValues[i]*1.0/100)**(year-2023)
    total2030Energy = np.sum(energyValues2030)
    energyIncreaseIn2030 = total2030Energy - total2023Energy

    ciData = pd.read_excel(ciFile, header=[0, 1], sheet_name="Table 2") # CI is in gCO2eq/kWh
    method1CIValues = ciData[("Projected Avg CI (lifecycle, No Change)", year)].values[:topKStates]
    method2CIValues = ciData[("Projected Avg CI (lifecycle, Current Decarbonization)", year)].values[:topKStates]
    method3CIValues = ciData[("Projected Avg CI (lifecycle, Zero Carbon 2050)", year)].values[:topKStates]

    print("=============NC============")
    energyRemaining = energyIncreaseIn2030
    ncEnergyValues = yearEnergyValues.copy()
    # ncSortedCI = np.argsort(method1CIValues)
    ncSortedCI = np.lexsort((-np.arange(len(method1CIValues)), method1CIValues)) # getting indices in sorted order of CIs
    # if 2 regions have same CI, getting the later index first as the later region has less initial load.
    ncCAGR = np.zeros_like(ncEnergyValues, dtype=np.float64)
    idx = 0
    while(energyRemaining > 0):
        energy2030 = ncEnergyValues[ncSortedCI[idx]]*(1+cagrLimit*1.0/100)**(year-2023)
        addedEnergy = energy2030 - ncEnergyValues[ncSortedCI[idx]]
        if (addedEnergy < energyRemaining):
            ncEnergyValues[ncSortedCI[idx]] = energy2030
            ncCAGR[ncSortedCI[idx]] = cagrLimit
        else:
            addedEnergy = energyRemaining
            ncCAGR[ncSortedCI[idx]] = (ncEnergyValues[ncSortedCI[idx]]+addedEnergy)/ncEnergyValues[ncSortedCI[idx]]
            ncCAGR[ncSortedCI[idx]] = (ncCAGR[ncSortedCI[idx]]**(1/(year-2023)*1.0) - 1)*100
            ncEnergyValues[ncSortedCI[idx]] += addedEnergy
        energyRemaining -= addedEnergy
        # print(states[ncSortedCI[idx]], energy2030, addedEnergy, energyRemaining, ncEnergyValues[ncSortedCI[idx]], ncCAGR[ncSortedCI[idx]])
        idx += 1
    print(states[:topKStates])
    print("Alternate demand (green):", ncEnergyValues)
    print("Alternate CAGR (green):", ncCAGR)


    print("=============CD============")
    energyRemaining = energyIncreaseIn2030
    cdEnergyValues = yearEnergyValues.copy()
    # cdSortedCI = np.argsort(method2CIValues)
    cdSortedCI = np.lexsort((-np.arange(len(method2CIValues)), method2CIValues)) # getting indices in sorted order of CIs
    # if 2 regions have same CI, getting the later index first as the later region has less initial load.
    cdCAGR = np.zeros_like(cdEnergyValues, dtype=np.float64)
    idx = 0
    while(energyRemaining > 0):
        energy2030 = cdEnergyValues[cdSortedCI[idx]]*(1+cagrLimit*1.0/100)**(year-2023)
        addedEnergy = energy2030 - cdEnergyValues[cdSortedCI[idx]]
        if (addedEnergy < energyRemaining):
            cdEnergyValues[cdSortedCI[idx]] = energy2030
            cdCAGR[cdSortedCI[idx]] = cagrLimit
        else:
            addedEnergy = energyRemaining
            cdCAGR[cdSortedCI[idx]] = (cdEnergyValues[cdSortedCI[idx]]+addedEnergy)/cdEnergyValues[cdSortedCI[idx]]
            cdCAGR[cdSortedCI[idx]] = (cdCAGR[cdSortedCI[idx]]**(1/(year-2023)*1.0) - 1)*100
            cdEnergyValues[cdSortedCI[idx]] += addedEnergy
        energyRemaining -= addedEnergy
        # print(states[cdSortedCI[idx]], energy2030, addedEnergy, energyRemaining, cdEnergyValues[cdSortedCI[idx]], cdCAGR[cdSortedCI[idx]])
        idx += 1
    print(states[:topKStates])
    print("Alternate demand (green):", cdEnergyValues)
    print("Alternate CAGR (green):", cdCAGR)

    print("=============ZC50============")
    energyRemaining = energyIncreaseIn2030
    zc50EnergyValues = yearEnergyValues.copy()
    # zc50SortedCI = np.argsort(method3CIValues)
    zc50SortedCI = np.lexsort((-np.arange(len(method3CIValues)), method3CIValues)) # getting indices in sorted order of CIs
    # if 2 regions have same CI, getting the later index first as the later region has less initial load.
    zc50CAGR = np.zeros_like(zc50EnergyValues, dtype=np.float64)
    idx = 0
    while(energyRemaining > 0):
        energy2030 = zc50EnergyValues[zc50SortedCI[idx]]*(1+cagrLimit*1.0/100)**(year-2023)
        addedEnergy = energy2030 - zc50EnergyValues[zc50SortedCI[idx]]
        if (addedEnergy < energyRemaining):
            zc50EnergyValues[zc50SortedCI[idx]] = energy2030
            zc50CAGR[zc50SortedCI[idx]] = cagrLimit
        else:
            addedEnergy = energyRemaining
            zc50CAGR[zc50SortedCI[idx]] = (zc50EnergyValues[zc50SortedCI[idx]]+addedEnergy)/zc50EnergyValues[zc50SortedCI[idx]]
            zc50CAGR[zc50SortedCI[idx]] = (zc50CAGR[zc50SortedCI[idx]]**(1/(year-2023)*1.0) - 1)*100
            zc50EnergyValues[zc50SortedCI[idx]] += addedEnergy
        energyRemaining -= addedEnergy
        # print(states[zc50SortedCI[idx]], energy2030, addedEnergy, energyRemaining, zc50EnergyValues[zc50SortedCI[idx]], ncCAGR[zc50SortedCI[idx]])
        idx += 1
    print(states[:topKStates])
    print("Alternate demand (green):", zc50EnergyValues)
    print("Alternate CAGR (green):", zc50CAGR)

    method1Emissions = np.multiply(ncEnergyValues, method1CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
    method2Emissions = np.multiply(cdEnergyValues, method2CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
    method3Emissions = np.multiply(zc50EnergyValues, method3CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq

    # avgEmissions = (method1Emissions + method2Emissions + method3Emissions) / 3
    # avgEmissions = (method1Emissions + method2Emissions + method3Emissions) / 3
    print("Emissions (green)...")
    print(f"NC: {sum(method1Emissions)}, CD: {sum(method2Emissions)}, ZC50: {sum(method3Emissions)}")
    print("US as sum of states averaged over all CI projections:", sum((method1Emissions + method2Emissions + method3Emissions) / 3))
    return


def maximizeEmissionIncrease(energyFile, ciFile, cagrLimit=30, year=2030, topKStates=10):
    print("CAGR limit = ", cagrLimit)
    energyData = pd.read_excel(energyFile, header=0, sheet_name="Table 3") # load is in MWh/year
    cagrData = pd.read_excel(energyFile, header=0 , sheet_name="Table 3")
    cagrValues = cagrData["CAGR"].values
    yearEnergyValues = energyData["2023 Load"].values[:topKStates]
    states = energyData["State"].values
    total2023Energy = np.sum(yearEnergyValues)
    energyValues2030 = yearEnergyValues.copy()
    energyValues2030 = energyValues2030.astype(np.float64)
    for i in range(len(yearEnergyValues)):
        energyValues2030[i] = yearEnergyValues[i]*1.0*(1+cagrValues[i]*1.0/100)**(year-2023)
    total2030Energy = np.sum(energyValues2030)
    energyIncreaseIn2030 = total2030Energy - total2023Energy

    ciData = pd.read_excel(ciFile, header=[0, 1], sheet_name="Table 2") # CI is in gCO2eq/kWh
    method1CIValues = ciData[("Projected Avg CI (lifecycle, No Change)", year)].values[:topKStates]
    method2CIValues = ciData[("Projected Avg CI (lifecycle, Current Decarbonization)", year)].values[:topKStates]
    method3CIValues = ciData[("Projected Avg CI (lifecycle, Zero Carbon 2050)", year)].values[:topKStates]

    print("=============NC============")
    energyRemaining = energyIncreaseIn2030
    ncEnergyValues = yearEnergyValues.copy()
    # ncSortedCI = np.argsort(method1CIValues)
    ncSortedCI = np.lexsort((-np.arange(len(method1CIValues)), -method1CIValues)) # getting indices in sorted order of CIs
    # if 2 regions have same CI, getting the later index first as the later region has less initial load.
    ncCAGR = np.zeros_like(ncEnergyValues, dtype=np.float64)
    idx = 0
    while(energyRemaining > 0):
        energy2030 = ncEnergyValues[ncSortedCI[idx]]*(1+cagrLimit*1.0/100)**(year-2023)
        addedEnergy = energy2030 - ncEnergyValues[ncSortedCI[idx]]
        if (addedEnergy < energyRemaining):
            ncEnergyValues[ncSortedCI[idx]] = energy2030
            ncCAGR[ncSortedCI[idx]] = cagrLimit
        else:
            addedEnergy = energyRemaining
            ncCAGR[ncSortedCI[idx]] = (ncEnergyValues[ncSortedCI[idx]]+addedEnergy)/ncEnergyValues[ncSortedCI[idx]]
            ncCAGR[ncSortedCI[idx]] = (ncCAGR[ncSortedCI[idx]]**(1/(year-2023)*1.0) - 1)*100
            ncEnergyValues[ncSortedCI[idx]] += addedEnergy
        energyRemaining -= addedEnergy
        # print(states[ncSortedCI[idx]], energy2030, addedEnergy, energyRemaining, ncEnergyValues[ncSortedCI[idx]], ncCAGR[ncSortedCI[idx]])
        idx += 1
    print(states[:topKStates])
    print("Alternate demand (brown):", ncEnergyValues)
    print("Alternate CAGR (brown):", ncCAGR)

    print("=============CD============")
    energyRemaining = energyIncreaseIn2030
    cdEnergyValues = yearEnergyValues.copy()
    # cdSortedCI = np.argsort(method2CIValues)
    cdSortedCI = np.lexsort((-np.arange(len(method2CIValues)), -method2CIValues)) # getting indices in sorted order of CIs
    # if 2 regions have same CI, getting the later index first as the later region has less initial load.
    cdCAGR = np.zeros_like(cdEnergyValues, dtype=np.float64)
    idx = 0
    while(energyRemaining > 0):
        energy2030 = cdEnergyValues[cdSortedCI[idx]]*(1+cagrLimit*1.0/100)**(year-2023)
        addedEnergy = energy2030 - cdEnergyValues[cdSortedCI[idx]]
        if (addedEnergy < energyRemaining):
            cdEnergyValues[cdSortedCI[idx]] = energy2030
            cdCAGR[cdSortedCI[idx]] = cagrLimit
        else:
            addedEnergy = energyRemaining
            cdCAGR[cdSortedCI[idx]] = (cdEnergyValues[cdSortedCI[idx]]+addedEnergy)/cdEnergyValues[cdSortedCI[idx]]
            cdCAGR[cdSortedCI[idx]] = (cdCAGR[cdSortedCI[idx]]**(1/(year-2023)*1.0) - 1)*100
            cdEnergyValues[cdSortedCI[idx]] += addedEnergy
        energyRemaining -= addedEnergy
        # print(states[cdSortedCI[idx]], energy2030, addedEnergy, energyRemaining, cdEnergyValues[cdSortedCI[idx]], cdCAGR[cdSortedCI[idx]])
        idx += 1
    print(states[:topKStates])
    print("Alternate demand (brown):", cdEnergyValues)
    print("Alternate CAGR (brown):", cdCAGR)

    print("=============ZC50============")
    energyRemaining = energyIncreaseIn2030
    zc50EnergyValues = yearEnergyValues.copy()
    # zc50SortedCI = np.argsort(method3CIValues)
    zc50SortedCI = np.lexsort((-np.arange(len(method3CIValues)), -method3CIValues)) # getting indices in sorted order of CIs
    # if 2 regions have same CI, getting the later index first as the later region has less initial load.
    zc50CAGR = np.zeros_like(zc50EnergyValues, dtype=np.float64)
    idx = 0
    while(energyRemaining > 0):
        energy2030 = zc50EnergyValues[zc50SortedCI[idx]]*(1+cagrLimit*1.0/100)**(year-2023)
        addedEnergy = energy2030 - zc50EnergyValues[zc50SortedCI[idx]]
        if (addedEnergy < energyRemaining):
            zc50EnergyValues[zc50SortedCI[idx]] = energy2030
            zc50CAGR[zc50SortedCI[idx]] = cagrLimit
        else:
            addedEnergy = energyRemaining
            zc50CAGR[zc50SortedCI[idx]] = (zc50EnergyValues[zc50SortedCI[idx]]+addedEnergy)/zc50EnergyValues[zc50SortedCI[idx]]
            zc50CAGR[zc50SortedCI[idx]] = (zc50CAGR[zc50SortedCI[idx]]**(1/(year-2023)*1.0) - 1)*100
            zc50EnergyValues[zc50SortedCI[idx]] += addedEnergy
        energyRemaining -= addedEnergy
        # print(states[zc50SortedCI[idx]], energy2030, addedEnergy, energyRemaining, zc50EnergyValues[zc50SortedCI[idx]], ncCAGR[zc50SortedCI[idx]])
        idx += 1
    print(states[:topKStates])
    print("Alternate demand (brown):", zc50EnergyValues)
    print("Alternate CAGR (brown):", zc50CAGR)

    method1Emissions = np.multiply(ncEnergyValues, method1CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
    method2Emissions = np.multiply(cdEnergyValues, method2CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq
    method3Emissions = np.multiply(zc50EnergyValues, method3CIValues) * G_PER_KWH_TO_G_PER_MWH_CONVERTER * G_TO_MEGATON # in MtCO2eq

    # avgEmissions = (method1Emissions + method2Emissions + method3Emissions) / 3
    print("Emissions (brown)...")
    print(f"NC: {sum(method1Emissions)}, CD: {sum(method2Emissions)}, ZC50: {sum(method3Emissions)}")
    print("US as sum of states averaged over all CI projections:", sum((method1Emissions + method2Emissions + method3Emissions) / 3))
    return



if __name__ == "__main__":

    def analyzeEmissions(choice):
        match choice:
            case 1:
                print("1. US Emissions based on LBNL and EMaps data")
                # ### LBNL US DC emissions (whole US)    
                # ### Energy source: LBNL 
                # ### CI source 1: Electricity Maps
                analyzeLBNLUSEmissions(energyFile="../data/electricity-demand/LBNL-US-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/EMaps-US-annual-CI.xlsx",
                                       ciSource="emaps")
            case 2:
                print("2. US Emissions based on LBNL and Ember data")
                # ### LBNL US DC emissions (whole US)    
                # ### Energy source: LBNL 
                # ### CI source 2: Ember
                analyzeLBNLUSEmissions(energyFile="../data/electricity-demand/LBNL-US-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/Ember-US-annual-CI.xlsx",
                                       ciSource="ember")
            case 3:
                print("3. US Emissions based on EPRI and EMaps data")
                # ### EPRI US DC emissions (whole US & top 10 states)    
                # ### Energy source: EPRI data
                # ### CI source 1: Electricity Maps
                analyzeEPRIUSEmissions(energyFile="../data/electricity-demand/EPRI-US-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/EMaps-US-annual-CI.xlsx",
                                       ciSource="emaps")
            case 4:
                print("4. US Emissions based on EPRI and Ember data")
                # ### EPRI US DC emissions (whole US & top 10 states)    
                # ### Energy source: EPRI data
                # ### CI source 2: Ember
                analyzeEPRIUSEmissions(energyFile="../data/electricity-demand/EPRI-US-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/Ember-US-annual-CI.xlsx",
                                       ciSource="ember")
            case 5:
                print("5. Global Emissions based on IEA and Ember data")
                ### Global DC emissions
                ### Energy source: IEA
                ### CI source : Ember
                analyzeIEAGlobalEmissions(energyFile="../data/electricity-demand/IEA-Global-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/Ember-Global-annual-CI.xlsx",
                                       ciSource="ember",
                                       lbnlCagr=False)
            case 6:
                print("6. Global Emissions based on IEA (w/ LBNL CAGR) and Ember data")
                ### Global DC emissions
                ### Energy source: IEA w/ LBNL CAGR
                ### CI source : Ember
                analyzeIEAGlobalEmissions(energyFile="../data/electricity-demand/IEA-Global-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/Ember-Global-annual-CI.xlsx",
                                       ciSource="ember",
                                       lbnlCagr=True)
            case 7:
                print("7. Global Emissions based on Koot et al. and Ember data")
                # ### Global DC emissions
                # ### Energy source: Koot et al.
                # ### CI source : Ember
                analyzeKootGlobalEmissions(energyFile="../data/electricity-demand/Koot-Global-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/Ember-Global-annual-CI.xlsx",
                                       ciSource="ember")
            case 8:
                print("8. US Statewise Emissions based on EPRI and EMaps data (different CAGR)")
                ### EPRI US DC emissions (top 10 states)    
                ### Energy source: EPRI data
                ### CI source 1: Electricity Maps
                analyzeStateEmissionsDifferentCAGR(energyFile="../data/electricity-demand/EPRI-US-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/EMaps-US-annual-CI.xlsx")
            case 9:
                print("9. US Statewise Emissions for alternate demand scenarios")
                ### EPRI US DC emissions (top 10 states)    
                ### Energy source: EPRI data
                ### CI source 1: Electricity Maps
                print("\nGreen scenario...")
                print("=================================================================")
                minimizeEmissionIncrease(energyFile="../data/electricity-demand/EPRI-US-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/EMaps-US-annual-CI.xlsx")                
                print("=================================================================")
                print("\nBrown scenario...")
                maximizeEmissionIncrease(energyFile="../data/electricity-demand/EPRI-US-annual-demand.xlsx",
                                       ciFile="../data/carbon-intensity/EMaps-US-annual-CI.xlsx")
                print("=================================================================")
            case _:
                print("Wrong key pressed. Try again.")
        return
    
    while(1):
        print("=================================================================")
        print("Analysis:")
        print("1. US Emissions based on LBNL and EMaps data")
        print("2. US Emissions based on LBNL and Ember data")
        print("3. US Emissions based on EPRI and EMaps data")
        print("4. US Emissions based on EPRI and Ember data")
        print("5. Global Emissions based on IEA and Ember data")
        print("6. Global Emissions based on IEA (w/ LBNL CAGR) and Ember data")
        print("7. Global Emissions based on Koot et al. and Ember data")
        print("8. US Statewise Emissions based on EPRI and EMaps data (different CAGR)")
        print("9. US Statewise Emissions for alternate demand scenarios")
        print("Press 0 to exit")
        print("=================================================================")
        choice = int(input())
        if (choice == 0):
            print("Analysis done.")
            break
        print("=================================================================")
        analyzeEmissions(choice)

    


    
    
    
    

    

    

    
    
    


    