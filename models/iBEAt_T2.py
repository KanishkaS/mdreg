#!/ur/bin/python
# -*- coding: utf-8 -*-
"""
@author: Kanishka Sharma
iBEAt study; T2 mapping sequence using T2 prep times
Siemens 3T PRISMA - Leeds
"""

import numpy as np
from scipy.optimize import curve_fit


## TODO: Generalise to add echo times for other scanners in the iBEAt study
def read_prep_times():
    """
    This function manually reads the T2 prep times for the iBEAt study T2-prep sequence
    and returns  T2 prep times as a list 
    """
    T2_prep_times = []
    ## hard coded as these are not available in the anonymised Siemens dicom tags
    T2_prep_times = [0,30,40,50,60,70,80,90,100,110,120]
    
    return T2_prep_times



def exp_func(T2_prep_times,S0,T2):
    """
    mono-exponential function used to perform T2-fitting
    """
  
    return S0*np.exp(-T2_prep_times/T2)



def T2_fitting(images_to_be_fitted, T2_prep_times):
    """
    curve_fit returns T2-fitting based: fit, S0, and T2map
    """
    
    lb = [0,0]
    ub = [np.inf,np.inf]
    initial_guess = [np.max(images_to_be_fitted),80] 

    popt, pcov = curve_fit(exp_func, xdata = T2_prep_times, ydata = images_to_be_fitted, p0=initial_guess, bounds=(lb,ub), method='trf')

    fit = []

    for te in T2_prep_times:
        fit.append(exp_func(te, *popt))

    S0 = popt[0]
    T2 = popt[1]

    return fit, S0, T2



def fitting(images_to_be_fitted, signal_model_parameters):
    '''
    images_to_be_fitted: single pixel at different T2-prep times
    '''
    
    fitted_parameters = []
   
    T2_prep_times = signal_model_parameters[1]

    results = T2_fitting(images_to_be_fitted, T2_prep_times)

    fit = results[0]
    S0 = results[1]
    T2 = results[2]
    
    fitted_parameters = [S0, T2]

    return fit, fitted_parameters



