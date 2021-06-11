"""Test for my functions."""

from functions import standard_averages, standard_equation, sample_concentrations, loading
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


d1 = {'1' : 0, '2' : 0.125, '3' : 0.25, '4' : 0.5, '5' : 1, '6' : 2, 
      '7' : 0, '8' : 0.125, '9' : 0.25, '10' : 0.5, '11' : 1, '12' : 2}
d2 = {'1' : 0, '2' : 0.125, '3' : 0.25, '4' : 0.5, '5' : 1, '6' : 2, 
      '7' : 0, '8' : 0.125, '9' : 0.25, '10' : 0.5, '11' : 1, '12' : 2}
d3 = {'1' : 1, '2' : 1, '3' : 1, '4' : 1, '5' : 1, '6' : 1, 
      '7' : 1, '8' : 1, '9' : 1, '10' : 1, '11' : 1, '12' : 1}

test = pd.DataFrame([d1, d2, d3], ['A', 'B', 'C'])


def test_standard_averages():

    assert callable(standard_averages)

    assert standard_averages(test, 'A') == [0, 0.125, 0.25, 0.5, 1, 2]

    assert isinstance(standard_averages(test, 'A'), list)

    assert len(standard_averages(test, 'A')) == 6


def test_standard_equation():

    assert callable(standard_equation)

    assert isinstance(standard_equation(standard_averages(test, 'C')), str)

    assert standard_equation(standard_averages(test, 'C')) == 'absorbance = 0.0(concentration) + 1.0'


def test_loading():

    assert callable(standard_equation)

    assert isinstance(loading({'Sample 1' : 20}), dict) 

    assert loading({'Sample 1' : 20, 'Sample 2' : 10}, 15) == {'Sample 1' : 1, 'Sample 2' : 2}

    assert len(loading({'Sample 1' : 20, 'Sample 2' : 10}, 15)) == 2
