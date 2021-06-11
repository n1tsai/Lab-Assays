"""Classes used throughout project"""

import numpy as np
import pandas as pd


class TotalProteinAssay():

    '''This class takes a csv file from a spectrophotometer plate reader to create a dataframe for analysis.
    
    Instance Attributes
    -------------------
    csvfile : string
        The file output of the spectrophotometer saved as a csv file.

    bca : dataframe
        A dataframe that reads the absorbance data from the csv file. 
    '''

    def __init__(self, csvfile):
        
        self.csvfile = csvfile

        # specifies columns and rows to read from standard csv file format of the lab spectrophotometer
        collist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        self.bca = pd.read_csv(self.csvfile, skiprows = 2, skipfooter = 4, usecols = collist, engine = 'python')
        # rename rows of dataframe to read like 96 well plate
        self.bca.index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
