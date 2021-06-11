"""A collection of function for doing my project."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def standard_averages(bca, row_number):

    '''This function calculates the average of the two replicates of standard dilutions loaded.

    Parameters
    ----------
    bca : dataframe
        The dataframe containing absorbance data from analyzing the 96 well plate.
    row_number : string
        The row in which BSA dilution standards were loaded.

    Returns
    -------
    standard_avgs : list
        A list of the average absorbances for the BSA dilution standards.
    '''

    standa = ['1', '2', '3', '4', '5', '6']
    standb = ['7', '8', '9', '10', '11', '12']
    standard_avgs = []

    # two replicates of standards are loaded, each dilution series covering half the plate 
    # replicates are zipped together based on related positions
    for a, b in zip(standa, standb):
        standard_avgs.append((bca.loc[row_number, a] + bca.loc[row_number, b]) / 2)

    return standard_avgs


def standard_equation(standard_avgs):

    '''This function calculates a standard curve comparing total protein concentration to absorbance at 562 nm.

    Parameters
    ----------
    standard_avgs : list
        The list of average absorbances for the BSA dilution standards.

    Returns
    -------
    equation : string
        The equation of the standard curve showing relationship between protein concentration and absorbance.
    '''

    # reshape changes the array of x values to a 2D format that is one column, required for Linear Regression model 
    x = np.array([0, 0.125, 0.25, 0.5, 1, 2]).reshape((-1, 1))
    y = np.array(standard_avgs)

    model = LinearRegression().fit(x, y)

    r_sq = model.score(x, y)
    print('coefficient of determination:', r_sq)

    equation = 'absorbance = {}(concentration) + {}'.format(str(model.coef_[0]), str(model.intercept_))

    plt.plot([0, 0.125, 0.25, 0.5, 1, 2], standard_avgs);

    return equation


def sample_concentrations(bca, *sample_rows):

    '''This function calculates protein concentrations based on absorbance using linear regression equation.

    Parameters
    ----------
    bca : dataframe
        The dataframe containing absorbance data from analyzing the 96 well plate.
    sample_rows : string(s)
        The rows in which samples were loaded.

    Returns
    -------
    sample_concentrations : dictionary
        A dictionary relating protein concentration in micrograms per microliter to sample number.
    '''

    odd_rows = ['1', '3', '5', '7', '9', '11']
    even_rows = ['2', '4', '6', '8', '10', '12']
    sample_absorbance = []

    # two replicates of sample are loaded side by side and can be zipped through by combining even and odd groups
    for row in sample_rows:
        for even, odd in zip(odd_rows, even_rows):
            sample_absorbance.append((bca.loc[row, even] + bca.loc[row, odd]) / 2)

    coefficient = input('Enter slope: ')
    intercept = input('Enter y intercept: ')

    count = 1
    sample_concentrations = {}

    for val in sample_absorbance:
        # 2 microliters sample are loaded compared to 20 microliters standard, need to adjust for loading difference
        conc = 10 * (float(val) - float(intercept)) / float(coefficient)
        # this conditional is used to skip empty wells containing no sample or resolving buffer 
        if conc < 0:
            continue
        else:
            sample_concentrations['Sample ' + str(count)] = conc
            count += 1
 
    return sample_concentrations


def loading(concentrations, protein_load = 15):

    '''This function takes the dictionary of sample concentrations and calculates amount of diluted sample to load.

    Parameters
    ----------
    concentrations : dictionary
        The dictionary relating protein concentration in micrograms per microliter to sample number.
    protein_load : integer
        The amount of total protein in micrograms to load in followup experiments.

    Returns
    -------
    volume_to_load : dictionary
        A dictionary relating volumes to load in microliters to sample number. 
    '''

    pre_dilution_conc = concentrations.values()
    volume_to_load = {}
    count = 1

    for samples in pre_dilution_conc:
        # 4x sample buffer is added to experimental samples before Western blot, 3/4 accounts for dilution
        vol = protein_load / (samples * 3 / 4)
        volume_to_load['Sample ' + str(count)] = vol
        count += 1

    return volume_to_load