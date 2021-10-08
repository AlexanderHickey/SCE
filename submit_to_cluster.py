# -*- coding: utf-8 -*-
"""
@author: Alex Hickey
This module is used to submit multiple tasks to a Compute Canada cluster, by
sweeping over a specified parameter and keeping the others fixed.
"""
import numpy as np
import os
import subprocess
import sys


L = 15 #Square lattice will be of size LxL
Jx = 0.5
start_indx = 100

Tlist = np.linspace(2.0,8.0,601)
time = '23:59:59' #Maximum run time
memory = '3G' #Memory per core required, this is NOT shared between jobs!!!
email = 'a2hickey@uwaterloo.ca'


preamble = ["#!/bin/bash\n",
            "#SBATCH --account=def-gingras\n",
            "#SBATCH --time={}\n".format(time),
            "#SBATCH --nodes=1\n",
            "#SBATCH --ntasks=1\n",
            "#SBATCH --mem={}\n".format(memory),
            "#SBATCH --mail-user={}\n".format(email),
            "#SBATCH --mail-type=FAIL\n",
            "\n",
            "module load miniconda2\n"]

def execute(Jx,T,L,filename,read = False):


    #Generate shell file
    with open('run.sh','w') as shell:

        shell.write("".join(preamble))
        shell.write("python __runALPS.py {} {} {} {}".format(filename,L,Jx,T))
    
    #Print out contents of shell file
    if read:
        with open('run.sh','r') as file:    
            print(file.read())
    
    #Submit job to scheduler
    #subprocess in Python 2.7 does not print terminal output
    subprocess.check_output(['sbatch run.sh'], shell=True)
    
    print('Job {} submitted'.format(filename))
    #Delete shell file
    os.remove('run.sh')
   
#Sweep over T only
def main1():
    indx = start_indx
    for T in Tlist:
        execute(Jx,T,L,indx)
        indx += 1
        
#Sweep over T, Jx, and L
def main2():
    indx = 0
    Jxlist = [.03,.05,.07,.09,.11,.13,.15]
    Llist = [10,12,15]
    for Jx in Jxlist:
        for L in Llist:
            indx += 100
            for j in range(len(Tlist)):
                nme = '{}'.format(indx+j)
                execute(Jx,Tlist[j],L,nme)
                

if __name__ == '__main__':
 
    main1() 