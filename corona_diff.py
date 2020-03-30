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

N=3500      # Initial population
I=1         # Initially 3 infected people
R=0         # 0 Recovered
S=N-I-R     # Susceptible (N=S+I+R)


T=1       # Time-play

def SIR(vals,t ):
    S,I,R=vals
    b=20.1         # Rate of infection
    g=1.5           # Rate of recovery
    
    dS=-b*S*I/N     # dS/dt
    dI=b*S*I/N + g*I
    dR=g*I
    
    return [dS,dI,dR]

    
t=np.linspace(0,T,1000)
x=[S,I,R]
sol=odeint(SIR,x,t)


plt.plot(t,sol[:,0])
plt.plot(t,sol[:,1])
plt.plot(t,sol[:,2])

plt.xlabel('t')
plt.legend(['S','I','R'],shadow=True)
plt.title('COVID')
plt.draw()
savefig("/home/paul/Documents/"+"difff.png",dpi=400)
