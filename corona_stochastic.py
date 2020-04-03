#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 18:46:49 2020

@author: paul
"""

# A stochastic SIR model!

from random import uniform as u
import math
import numpy as np
import matplotlib.pyplot as plt
from pylab import *        # for savefig()

N=1002252      # Initial population
I=1         # Initially 3 infected people
R=0         # 0 Recovered
S=N-I-R     # Susceptible (N=S+I+R)

beta=0.6671291         # Rate of infection
gamma=0.3328710           # Rate of recovery

T=70       # Time-play  days?
t=0         # current time
  

data=[]

x=[S,I,R]           # Initial params
rates=(beta,gamma)

i=0
while (i<10):         # coz you might want to run it a thousand million times!
    S,I,R=x
    b,g=rates       # taking the same conditions, but these are for here!
    ctr=0              
    
    # Gillespie algo...

    while t<T:
        if I==0:
            break
        
        dS=b*S*I/N
        dR=g*I
        W=dS+dR         # As a scale factor...
        
        step=u(0,1)
        dt=-math.log(step)/W
        t+=dt
        
        if u(0,1) <dS/W:
            S=S-1
            I=I+1
        else:
            I=I-1
            R=R+1
        # Okay, so we are gonna average time! Makes mathematical sense...    
        
        if i==0:        # 1st run
            data.append([t,S,I,R,1])        # 1 means that one value is added ... needed below!
        else:
            if (ctr>=len(data)):            # So some data is lost here! But that's averaged out!
                break       # break out of inner loop!
            else:
                data[ctr][0]+=t
                data[ctr][1]+=S
                data[ctr][2]+=I
                data[ctr][3]+=R
                data[ctr][4]+=1
            
        ctr+=1
    


    if i==0:
        data=np.array(data)
    t=0
    i+=1


for i in range(len(data)):
    n=data[i][4]         # Number of times a value has been added!
    data[i]/=n
    

# Plot Stochastic sim...

plt.plot(data[:,0],data[:,1])
plt.plot(data[:,0],data[:,2])
plt.plot(data[:,0],data[:,3])

plt.xlabel('Time')
plt.ylabel('Population')
plt.legend(['S','I','R'],shadow=True)
plt.title('COVID-Sim')
plt.draw()
savefig("/home/paul/Documents/COVID/"+"sim_b"+str(beta)+"_g"+str(gamma)+".png",dpi=400)






        
    



