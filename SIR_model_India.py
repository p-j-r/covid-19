#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:05:45 2020

@author: paul
"""
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from pylab import *
import pandas as pd

"""
Certain portions in the code are taken from:
    https://github.com/rajeshrinet/pyross
    
This version of model is taken from their work:
    https://arxiv.org/abs/2003.12055v1
    
    This ArXiv pre-print lists the model...
    
    Data Sources can be found at Github.
    
"""

#  Age categories (0-79 in group[s] of 4)
M=16


"""
Load Data

""" 
# load age structure data
my_data = np.genfromtxt('/home/paul/Desktop/Research/COVID-19/India-2019.csv', delimiter=',', skip_header=1)
aM, aF = my_data[:, 1], my_data[:, 2]       # Male & Female Population

# contact matrices
my_data = pd.read_excel('/home/paul/Desktop/Research/COVID-19/contact_matrices_152_countries/MUestimates_home_1.xlsx', sheet_name='India',index_col=None)
CH = np.array(my_data)      # Home

my_data = pd.read_excel('/home/paul/Desktop/Research/COVID-19/contact_matrices_152_countries/MUestimates_work_1.xlsx', sheet_name='India',index_col=None)
CW = np.array(my_data)      # Work

my_data = pd.read_excel('/home/paul/Desktop/Research/COVID-19/contact_matrices_152_countries/MUestimates_school_1.xlsx', sheet_name='India',index_col=None)
CS = np.array(my_data)      # School

my_data = pd.read_excel('/home/paul/Desktop/Research/COVID-19/contact_matrices_152_countries/MUestimates_other_locations_1.xlsx', sheet_name='India',index_col=None)
CO = np.array(my_data)      # Other Locations

my_data = pd.read_excel('/home/paul/Desktop/Research/COVID-19/contact_matrices_152_countries/MUestimates_all_locations_1.xlsx', sheet_name='India',index_col=None)
CA = np.array(my_data)      # ALL




# set age groups
Ni=aM+aF;   Ni=Ni[0:M]; #i=0,...,15
N=np.sum(Ni)

# initial conditions    
Is = np.zeros((M));  Is[0:M]=3;  #Is[2:6]=1

Ia = np.zeros((M)); Ia[0:M]=1;
R  = np.zeros((M))
S  = Ni - (Ia + Is + R)

alpha=0.25         # Asymptomatic cases ratio
beta=0.1646692         # Rate of infection
gamma=1.0/7           # Rate of recovery/restored... Deaths too!


T=180       # Time-play


# matrix of total contacts
C=CH+CW+CS+CO       # Time dependent contact matrix : Linear Combination of contributing factors  

f=1         # Proportion of self-isolation (0-1) , f=0 (totally isolated)
#Cs=f*C      # Contact matrix for symptomatic cases 
#Ca=C

lm = np.zeros(M)       # Time-dependent lambda factor
    
def l(Ia_,Is_,i):       # for i th group
    """ Returns lambda(t)=l upgraded
        
        Dependence on time is due to change in contributing factors: Ij & Nj 
    """
    
    for j in range(M):
        lm[i]+= ( f*C[i,j]*Is_/Ni[j] + C[i,j]*Ia_/Ni[j] )
            
    lm[i]=beta*lm[i]
    
    return lm[i]
            

    


def SIR(vals,t,a,b,g,i):
    
    
    
    S,Ia,Is,R=vals
    lm=l(Ia,Is,i)     # Frozen at t
    
    
    dS=-lm*S     # dS/dt
    #dIa=0
    dIa=a*lm*S - g*Ia
    dIs=(1-a)*lm*S - g*Is
    dR=g*(Ia + Is)
    
    return [dS,dIa,dIs,dR]

steps=100
solution=np.zeros([steps,4])

#           # Initial params

for i in range (M):
    
    x=[ S[i],Ia[i],Is[i],R[i] ]      # i for the age-group
    rates=(alpha,beta,gamma,i)
       
    t=np.linspace(0,T,steps)


    sol=odeint(SIR,x,t,args=rates,mxstep=5000000)#,full_output=1) Repeated convergence failures (perhaps bad Jacobian or tolerances).
    solution+=sol
    
# Plot ODE solutions
    
plt.plot(t,solution[:,0])
plt.plot(t,solution[:,1])
plt.plot(t,solution[:,2])
plt.plot(t,solution[:,3])
    
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend(['S','Ia','Is','R'],shadow=True)
plt.autoscale(enable=True, axis='x', tight=True)
plt.title('COVID')
plt.draw()
savefig("/home/paul/Documents/COVID/"+"Analytic"+"_b"+str(beta)+"_g"+str(gamma)+".png",dpi=400)


    

