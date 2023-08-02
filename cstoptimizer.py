#%% imports
from cstoptimizerfunctions import *
from scipy.optimize import minimize
from mycom import *
import numpy as np
import matplotlib.pyplot as plt
%matplotlib qt 
#%% step 0 Optimization parameters
# bandwidth
fmin = 8 #Ghz
fmax = 12 #Ghz
# initial value for the parameters to optimize
epsilon_init =3.69
sigma_init = 0.053
# minimization threshold
maxerr = 5
# maximum number of optimization runs
maxeval = 20

#%% step1 connect to cst
cst = connect('CSTStudio.Application')
# close project before running this, also run this once only
cst.CloseProject(r"C:\Users\smen851\OneDrive - The University of Auckland\CST\microstripFitting1.cst")
mws = Dispatch(cst.OpenFile("C:\\Users\\smen851\\OneDrive - The University of Auckland\\CST\\microstripFitting1.cst"))

#%% step2 load reference function goal
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
gamma = alpha + 1j*beta
# downsampling (to make optimizer faster)
g = sp.interpolate.interp1d(f, gamma, kind='linear')
fref = np.linspace(8,12,50)
gamma = g(fref)

#%% step3 define lambda function
fun = lambda x: errorfunction(mws, x[0], x[1], gamma, fref, 8, 12)

#%% step4 optimize
plt.figure(300)
plt.ion()
plt.show(block = False)
plt.pause(0.01)
plt.figure(301)
plt.ion()
plt.show(block = False)
plt.pause(0.01)
#%%
x = minimize(fun, [epsilon_init, sigma_init], method='CG', options={'maxiter':maxeval})
print(x)