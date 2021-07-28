#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import subprocess
import re


def get_uncertainty(ncell_list, value_list, num_exe="numerical_uncertainty"):
    """Wrapper for Eca's numerical uncertainty analysis tool
    handles only 'steady' case
    
    Parameters
    ----------
    
    ncell_list : list of int
        list of cell counts of 3D mesh
        
    value_list : list of float
        "value" associated to each mesh
    
    num_exe : string, optional, default=numerical_uncertainty
        Compiled executable of the numerical uncertainty tool, 
        if already in the path, the default value should work
    
    Returns 
    -------
    uncertainty : list of float
        Uncertainty associated to each value (given in the same order as the input)
        
    p : float
        p value for fit like phi+alpha^p
        
    fit_function : function: float -> float
        Function detected for the fit, 
        for example fit_function(h) = phi0+alpha*h**p
    
    """
    tmp_folder = "tmp_uncertainty"
    try:
        os.mkdir(tmp_folder)
    except FileExistsError:
        pass
    
    with open(tmp_folder+"/data.dat", "w") as f:
        f.write("ncell value\n")
        f.write("0 {}\n".format(len(ncell_list)))
        
        # Needs to be sorted from finest mesh to coarsest one
        idx = np.argsort(ncell_list)[::-1]
        
        for ncell, value in zip(np.array(ncell_list)[idx], np.array(value_list)[idx]):
            f.write("{}  {}\n".format(int(ncell), value))
     
    with open(tmp_folder+"/input.ini", "w") as f:
        f.write("""[Numerical_uncertainty]
CaseName       = testcase
DatafileName   = data.dat
OutputFormat   = TEX             ; PS/TEX/PNG/WIN/TEC/PDF
IsUnsteady     = No
GridStepsizeMethod = 3
TimeStepsizeMethod = -1
UncertaintySolution = 1
Showp          = Yes
ShowAllUncertainties = Yes
""")
    
    os.chdir(tmp_folder)
    output = subprocess.run(['numerical_uncertainty', 'input.ini'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    os.chdir("..")
    
    #print(output)
    
    uncertainty = np.zeros(len(ncell_list))
    for i in range(len(ncell_list)):
        uncertainty[i] = float(re.search(r"^  {}  ([^ ]+)".format(i+1), output, re.M).group(1))
    
    # Sort uncertainties similarly to input
    uncertainty = np.array(uncertainty)[idx]
        
    def search_var(name):
        return float(re.search("^{}\ *=\ *([^\ ]+)$".format(name), output, re.M).group(1))
        
    
    fit = re.search("^Fit\ *=\ phi=([^\ ]+)\ *$", output, re.M).group(1)
    
    if fit == "phi0+alfa*h^p":
        phi0 = search_var("phi0")
        alpha = search_var("alfa")
        p = search_var("p")
        fit_function = lambda h: phi0+alpha*h**p
    elif fit == "phi0+alfa*h":
        phi0 = search_var("phi0")
        alpha = search_var("alfa")
        p = 1
        fit_function = lambda h: phi0+alpha*h
    elif fit == "phi0+alfa*h^2":
        phi0 = search_var("phi0")
        alpha = search_var("alfa")
        p = 2
        fit_function = lambda h: phi0+alpha*h**p
    elif fit == "phi0+alfa_1*h+alfa_2*h^2":
        phi0 = search_var("phi0")
        alpha_1 = search_var("alfa_1")
        alpha_2 = search_var("alfa_2")
        p = 2
        fit_function = lambda h: phi0+alpha_1*h + alpha_2*h**2
 
    return uncertainty, p, fit_function
    
    
    
# unit tests
    
uncertainty1, p, fit_function = get_uncertainty([33883564, 19301374, 13242528, 9757986],
                                              [0.17538037479294386, 0.1755676298532007, 0.1761267846323142, 0.1767604882350247])

assert(p == 2)
assert(fit_function(0) == 0.17417) #phi0
assert(fit_function(1) - fit_function(0) == 0.0010864999999999903) # alpha


uncertainty2, p, fit_function = get_uncertainty([19301374, 33883564, 13242528, 9757986],
                                              [0.1755676298532007, 0.17538037479294386, 0.1761267846323142, 0.1767604882350247])

assert(p == 2)
assert(fit_function(0) == 0.17417) #phi0
assert(fit_function(1) - fit_function(0) == 0.0010864999999999903) # alpha
assert(uncertainty1[0] == uncertainty2[1])
assert(uncertainty1[1] == uncertainty2[0])
assert(uncertainty1[2] == uncertainty2[2])
