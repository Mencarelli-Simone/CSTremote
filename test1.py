#%%
from win32com.client import Dispatch
from win32com.client import VARIANT
import pythoncom
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, exp, log10, log, sin, cos, sqrt
# decorator for jupyter execution
# open plots in separate windows
%matplotlib qt 
#%%
cst = Dispatch('CSTStudio.Application')
# close project before running this, also run this once only
cst.CloseProject(r"C:\Users\smen851\OneDrive - The University of Auckland\CST\microstripFitting1.cst")
mws = Dispatch(cst.OpenFile("C:\\Users\\smen851\\OneDrive - The University of Auckland\\CST\\microstripFitting1.cst"))
mws.GetNumberOfParameters
#%%
# Result Tree item path
TreeItem = str('1D Results\\Port Information\\Gamma\\1(1)')
# Result Tree
rtree = mws.ResultTree
# Run Ids applicable to the current tree item
ids = rtree.GetResultIDsFromTreeItem(TreeItem)
# Result of last tree item
res = rtree.GetResultFromTreeItem(TreeItem, ids[0])
# I know the return is a 'Result1DComplex' object, 
# the correct way to access the data is the following:
res_x = res.GetArray('x')
res_yre = res.GetArray('yre')
res_yim = res.GetArray('yim')
#%% Visual
fig, ax = plt.subplots(1)
ax.plot(res_x, res_yim, res_x, res_yre)
#%% Plot the attenuation in dB/m and the effective permittivity 
# gamma = alpha + j beta
# alpha = attenuation constant
# beta = phase constant = 2 pi f sqrt(epsilon) / c
c = 3e8
f = np.array(res_x) * 1e9 # it's in GHz
epsilon_eff = (np.array(res_yim) * c / (2 * pi * f))**2
loss_dbm = -20 * np.array(res_yre) / log(10)
fig, ax = plt.subplots(1)
ax.plot(f, epsilon_eff)
fig, ax = plt.subplots(1)
ax.plot(f, loss_dbm)

#%% change a parameter and relaunch the solver
mws._FlagAsMethod("DoesParameterExist")
if mws.DoesParameterExist('epsilon_h'):
    mws._FlagAsMethod("RestoreParameter") 
    epsilon_h = mws.RestoreParameter('epsilon_h')
    print(epsilon_h)
    # change parameter
    mws._FlagAsMethod("StoreParameter")
    mws.StoreParameter('epsilon_h', 3.8)
    # verify
    mws._FlagAsMethod("RestoreParameter")   
    epsilon_h = mws.RestoreParameter('epsilon_h')
    print(epsilon_h)
    #mws._FlagAsMethod("DoesParameterExist")
else:
    print('wrong string identifier')

mws._FlagAsMethod("Save")   
mws.Save()
mws._FlagAsMethod("Rebuild")
mws.Rebuild()
mws._FlagAsMethod("Save")   
mws.Save()
#%%
mws._FlagAsMethod("UpdateResults")   
mws.UpdateResults


#edit for commit test