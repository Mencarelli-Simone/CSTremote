import numpy as np
import scipy as sp
from mycom import *
import matplotlib.pyplot as plt

runid = 0

def errorfunction(mws :object, epsilon :float, sigma :float, 
                  gamma_ref, freq_ref, fmin, fmax):
    """error function

    :param mws: MWS com object
    :param epsilon: dielectiric constant
    :type epsilon: float
    :param sigma: material conductivity
    :type sigma: float
    :param gamma_ref: reference curve for complex propagation constant
    :param freq_ref: reference datum frequency axis
    :param fmin: minimum frequency for error integration
    :parem fmax: maximum frequency for error integration
    """
    ## 1 set epsilon and sigma
    # Result Tree item path
    TreeItem = str('1D Results\\Port Information\\Gamma\\1(1)')
    # set parameter
    if invoke(mws, 'DoesParameterExist', 'epsilon_h'):
        epsilon_h = invoke(mws,'RestoreParameter','epsilon_h')
        print('old epsilon ',epsilon_h)
        # change parameter
        invoke(mws, 'StoreParameter','epsilon_h', epsilon)
        # verify
        epsilon_h = invoke(mws, 'RestoreParameter', 'epsilon_h')
        print('new epsilon ', epsilon_h)
        #mws._FlagAsMethod("DoesParameterExist")
    else:
        print('Error: wrong string identifier')
    # set other parameter
    if invoke(mws, 'DoesParameterExist', 'sigma'):
        sig = invoke(mws,'RestoreParameter','sigma')
        print('old sigma ', sig)
        # change parameter
        invoke(mws, 'StoreParameter','sigma', sigma)
        # verify
        sig = invoke(mws, 'RestoreParameter', 'sigma')
        print('new sigma ', sig)
        #mws._FlagAsMethod("DoesParameterExist")
    else:
        print('Error: wrong string identifier')

    invoke(mws, 'Save')
    invoke(mws, 'Rebuild')
    invoke(mws, 'Save')


    ## 2 run simulation 
    solver = invoke(mws,'Solver')
    print('starting solver')
    a = invoke(solver, 'start')
    print('solver return value ', a)


    ## 3 get results
    rtree = invoke(mws, 'ResultTree')
    # Run Ids applicable to the current tree item
    ids = invoke(rtree,'GetResultIDsFromTreeItem',TreeItem)
    # Result of last tree item
    res = invoke(rtree, 'GetResultFromTreeItem', TreeItem, ids[0])
    # I know the return is a 'Result1DComplex' object, 
    # the correct way to access the data is the following:
    res_x = np.array(res.GetArray('x'))
    res_yre = np.array(res.GetArray('yre'))
    res_yim = np.array(res.GetArray('yim'))
    t_sim =  res_yre + 1j*res_yim


    # 4 compute error
    # 1 resample the reference and simulation data (res_x is not uniform)
    gamma = sp.interpolate.interp1d(freq_ref, gamma_ref,kind='linear')
    gamma_sim = sp.interpolate.interp1d(res_x, t_sim, kind='linear')

    # new axis for the desired bandwidth
    freq = np.linspace(fmin,fmax,50);
    G = gamma(freq)
    G_s = gamma_sim(freq)

    error = np.abs(G - G_s)
    error_tot = np.sum(error) # quantity to be minimized
    # error plot
    plt.figure(300)
    plt.plot(freq, error)
    plt.draw()
    plt.pause(0.001)
    plt.show(block = False)
    # error plot
    plt.figure(301)
    global runid # get ahold of the global variable, objects are for idiots
    plt.scatter(runid, error_tot)
    plt.draw()
    plt.show(block = False)
    plt.pause(0.001)
    runid += 1
    print('runID', runid,': error value ',error_tot)

    return error_tot