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

N=10000      # Initial population
I=1         # Initially infected people
R=0         # 0 Recovered
S=N-I-R     # Susceptible (N=S+I+R)

beta=4.5         # Rate of infection
gamma=.5           # Rate of recovery
    

T=14       # Time-play

def SIR(vals,t,b,g):
    S,I,R=vals
    
    dS=-b*S*I/N     # dS/dt
    dI=b*S*I/N - g*I
    dR=g*I
    
    return [dS,dI,dR]

    
t=np.linspace(0,T,1000)
x=[S,I,R]           # Initial params
rates=(beta,gamma)
sol=odeint(SIR,x,t,args=rates)

# Plot ODE solutions
plt.plot(t,sol[:,0])
plt.plot(t,sol[:,1])
plt.plot(t,sol[:,2])

plt.xlabel('Time')
plt.ylabel('Population')
plt.legend(['S','I','R'],shadow=True)
plt.title('COVID')
plt.draw()
savefig("/home/paul/Documents/COVID/"+"diff_b"+str(beta)+"_g"+str(gamma)+".png",dpi=400)

