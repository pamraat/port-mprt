import numpy as np
import subprocess
import os
import time
import signal


# Input range of cases to run
minLx=2e-2
maxLx=3e-2
nLx=10
Lx=np.linspace(minLx,maxLx,num=nLx)
nx = Lx/(2e-4)
nx = nx.astype(int)

timeout = 8*60

# Data will be stored in 'result.txt' file
subprocess.run('cp result oldresult', shell=True)
subprocess.run('rm result', shell=True)
    
# Loop over cases, generate Lx, and run
for ind, myLx in enumerate(Lx):
    print('Running simulation for Lx=',myLx)
    command='mpiexec -n 6 ./nga.dp.gnu.opt.mpi.exe -i input --\"Lx={}\" --\"nx={}\"'.format(myLx, nx[ind])
    proc = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    time.sleep(timeout)
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    proc = []
    subprocess.run('cat ./monitor/simulation >> result', shell=True)
subprocess.run('python3 plot_results.py', shell=True)