import numpy as np
from matplotlib import pyplot as plt
import re

## Variable Initialization
gy = 0
rho_l = 0
rho_g = 0
sigma = 0
minLx=2e-2
maxLx=3e-2
nLx=11
Lx=np.linspace(minLx,maxLx,num=nLx)
sims= []
ampSim = np.array([])
tim = np.array([])

# Process the input file to obtain simulation parameters
with open('input') as fobj:
    for line in fobj:
        line_data = re.split(':',line)
        if line_data[0].rstrip()=='Gravity':
            gx=float(line_data[1].split()[0])
            gy=float(line_data[1].split()[1])
            gz=float(line_data[1].split()[2])
        if line_data[0].rstrip()=='Liquid density':
            rho_l=float(line_data[1])
        if line_data[0].rstrip()=='Gas density':
            rho_g=float(line_data[1])
            mu_g=float(line_data[1])
        if line_data[0].rstrip()=='Surface tension coefficient':
            sigma=float(line_data[1])

# Plot reference inviscid
k=2*np.pi/Lx
ngr = np.sqrt(k**2/(rho_l+rho_g)*(abs(gy)*(rho_l-rho_g)/k-sigma*k))

# Plot results from result file
with open('result') as fobj:
    for ind, line in enumerate(fobj):
        line_data = line.split()
        if ind < 3: continue
        try:
            ampSim = np.append(ampSim, float(line_data[4]))
            tim = np.append(tim, float(line_data[1]))
        except:
            if line_data[0] == 'Timestep':
                sims.append(ampSim)
                sims.append(tim)
                ampSim = []
                tim = []
            continue
    sims.append(ampSim)
    sims.append(tim)

ngrSim = np.zeros(int(len(sims)/2))
for ind in np.arange(int(len(sims)/2)):
    p = np.polyfit(sims[ind*2 + 1][750:1250], np.log(sims[ind*2][750:1250]), 1)
    ngrSim[int(ind)] = p[0]
    # plt.figure(ind + 1)
    # plt.plot(np.arange(len(sims[ind*2 + 1])), sims[ind*2], color='red',label='nga2')

# Plot
plt.plot(k,ngr,'-',lw=2,color='blue',label='Inviscid exact')
plt.plot(k[0:len(ngrSim)], ngrSim, color='red',label='nga2')
plt.title('Multiphase Rayleigh-Taylor Instability')
plt.xlabel('Wavenumber')
plt.ylabel('Growth Rate')
plt.ylim(bottom=0,top=1.2*max(ngr))
plt.legend()
plt.show()