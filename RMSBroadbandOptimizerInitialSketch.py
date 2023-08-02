#%% Requierements
# varies one or more parameters to try match a simulation result curve within a specified bandwidth
# uses a standard optimization method like scipy minimize 

#%% imports
import numpy as np
import scipy as sp
from mycom import *
import matplotlib.pyplot as plt

#%% Target curve ( complex )
t = np.loadtxt('tavg.csv', delimiter=",", dtype=str)
T = np.zeros(len(t)) * 1j
for i in range(len(T)):
    t[i] = t[i].replace('i', 'j')
    T[i] = complex(t[i])
f = np.loadtxt('fax.csv', delimiter=",", dtype=float) / 1e9 # let's make this in GHz

# l line length
l =  219e-3 - 40e-3
alpha = np.log(np.abs(T)) / l
n = 0
beta = (np.unwrap(np.angle(T)) + n * 2 * np.pi) / l 

#%% Simulated curve
# Simulation initialization  
cst = connect('CSTStudio.Application')
# close project before running this, also run this once only
cst.CloseProject(r"C:\Users\smen851\OneDrive - The University of Auckland\CST\microstripFitting1.cst")
mws = Dispatch(cst.OpenFile("C:\\Users\\smen851\\OneDrive - The University of Auckland\\CST\\microstripFitting1.cst"))
# Result Tree item path
TreeItem = str('1D Results\\Port Information\\Gamma\\1(1)')




#%% Simulation setup and runner
sigma = 0.05
epsilon = 3.69

# set parameter
if invoke(mws, 'DoesParameterExist', 'epsilon_h'):
    epsilon_h = invoke(mws,'RestoreParameter','epsilon_h')
    print(epsilon_h)
    # change parameter
    invoke(mws, 'StoreParameter','epsilon_h', epsilon)
    # verify
    epsilon_h = invoke(mws, 'RestoreParameter', 'epsilon_h')
    print(epsilon_h)
    #mws._FlagAsMethod("DoesParameterExist")
else:
    print('wrong string identifier')
# set other parameter
if invoke(mws, 'DoesParameterExist', 'sigma'):
    sig = invoke(mws,'RestoreParameter','sigma')
    print(sig)
    # change parameter
    invoke(mws, 'StoreParameter','sigma', sigma)
    # verify
    sig = invoke(mws, 'RestoreParameter', 'sigma')
    print(sig)
    #mws._FlagAsMethod("DoesParameterExist")
else:
    print('wrong string identifier')

invoke(mws, 'Save')
invoke(mws, 'Rebuild')
invoke(mws, 'Save')

#%% run simulation
solver = invoke(mws,'Solver')
print('starting solver')
a = invoke(solver, 'start')
print(a)



#%
# Result Tree
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

# #% plot  
# %matplotlib qt 
# # beta
# fig, ax = plt.subplots(1)
# ax.plot(f, alpha)
# ax.plot(res_x, np.real(t_sim))
# # alpha
# fig, ax = plt.subplots(1)
# ax.plot(f, beta)
# ax.plot(res_x, np.imag(t_sim))


#% error function core
# 1 resample the reference and simulation data (res_x is not uniform)
gamma = alpha + 1j* beta
gamma = sp.interpolate.interp1d(f, gamma,kind='linear')
gamma_sim = sp.interpolate.interp1d(res_x, t_sim, kind='linear')

# new axis for the desired bandwidth
freq = np.linspace(7,13,50);
G = gamma(freq)
G_s = gamma_sim(freq)


# beta
plt.figure(1)
plt.plot(freq, np.real(G))
plt.plot(freq, np.real(G_s))
# alpha
plt.figure(2)
plt.plot(freq, np.imag(G))
plt.plot(freq, np.imag(G_s))


error = np.abs(G - G_s)
error_tot = np.sum(error) # quantity to be minimized
# error plot
plt.figure(3)
plt.plot(freq, error)

print(error_tot)

# %%
