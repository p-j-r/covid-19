#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 12:31:24 2020

@author: paul
"""


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from random import randrange,randint,uniform
from pylab import savefig
import time

"Adapts corona_walk into a class, to create a net of lattices connected by small-world networks"
 

class Cluster:
    
    " This creates a lattice of random size (m*n) which models any population cluster: big, small, cities, villages, etc."
    
    max_size=100  
    L=20       # Lifetime params
    max_iter=1000      # in like discrete time-steps
    
    steps=10         # total number of times 
    ## DOES THIS COMPLICATE?
    
    neighbors=[]      # Store the neighbors here 
    nodes=[]
    walkers={}

    def __init__(self):
        
        self.cluster_id=0   
        ### GET AN ID!!!
        
        self.m=randint(self.max_size/2,self.max_size)     # self?: Do length & breadth interest us?
        self.n=randint(self.max_size/2,self.max_size)
        
        self.N=self.m*self.n      # Lattice size
        self.density=uniform(.4,.6)       # Density per node!
        # Social-distancing affects density!!!
        
        # A node represents a point in the cluster where walkers are free to go!
        # shops, malls, etc,etc...
        # 'density' means the intial average number of people per node!
        
        self.W=int(self.density*self.N)       # Number of random walkers
        self.sick, self.dead, self.iterate=0,0,0     # counters
    
    
        self.Lat=nx.grid_2d_graph(self.m,self.n)       # A 2-D Lattice
        
        for i in self.Lat.nodes():
            self.nodes.append(i)
            self.walkers[i]=[]
        
        nx.set_node_attributes(self.Lat,0,'infected')        # Sets the attribute infected, the number of infected peeps at a node at any temporal point 
        nx.set_node_attributes(self.Lat,self.walkers,'walkers')         # Sets the attribute walkers, the walkers at a node

        # 2: One of the nodes will be the 'exit node' for the lattice...{A small world of all exit-nodes}
        self.exit_node=self.nodes[randrange(len(self.nodes))]       # Look after this!?
        
        
        
        
        #? Should walker be a different class?
        #? No, a walker is selfless, and for the lattice[We are not interested in individuals!]
        self.x, self.y=np.zeros(self.W), np.zeros(self.W)    # walker x,y coord
        self.infect=np.zeros(self.W)              # walker health status
        self.lifespan=self.L*np.ones(self.W)            # Time left to live
        self.ts_sick=np.zeros(self.max_iter)      # time series of sick walkers
        #ts_dead=np.zeros(max_iter)
        self.ts_ctr=np.zeros(self.max_iter)       # counter to record each iter for averaging
        self.iter_high=0                 # The max count of iter (it doesn't go on till max_iter)
        
        
        
    
    
    
    def place(self):            
        "Place walkers on lattice"
            
        for j in range(self.W):                   
            ( self.x[j] , self.y[j] )= self.nodes[randrange(len(self.nodes))]
            self.Lat.nodes[ (self.x[j],self.y[j]) ]['walkers'].append(j)       # add this walker at node
    
    
    def first_case(self):        
        "Infect a random walker" 
            
        while(True):
            cx,cy= self.nodes[randrange(len(self.nodes))]     
            temp=self.Lat.nodes[(cx,cy)]['walkers']          # may be empty if nodes>walkers....! So empty range Error
            if (len(temp)!=0):
                break
    
        first_case=temp[randrange(len(temp))]   
        self.infect[first_case]=1
        self.Lat.nodes[(cx,cy)]['infected']+=1
        self.sick=1
            
        
    def walk(self,j):         
        "Walk the walker to a new location"
            
        for i in self.Lat.neighbors( (self.x[j],self.y[j]) ):
                self.neighbors.append(i)
              
        # remove a walker from node!
        self.Lat.nodes[(self.x[j],self.y[j])]['walkers'].remove(j)               
        ( self.x[j] , self.y[j] )=self.neighbors[randrange(len(self.neighbors))]
        # add him to the new node!
        self.Lat.nodes[(self.x[j],self.y[j])]['walkers'].append(j)

    

    def kill(self,j):   
        " Kill a walker"
            
        self.infect[j]=2
        self.sick-=1
        self.dead+=1
                
        self.Lat.nodes[(self.x[j],self.y[j])]['walkers'].remove(j)
        # 'infected' attribute is not updated as it gives the count of infected people at a hotspot. Going dead doesn't change that
        # Maybe a new attribute for people dying in a location would be great!
           
    # Too much of self's...Uff
        
        
    def actions(self,j):
        "To infect or to kill!?"
    
        if self.infect[j]<2:     #still alive
            self.walk(j)
            
        if self.infect[j]==1:    #sick
            self.lifespan[j]-=1
            self.Lat.nodes[(self.x[j],self.y[j])]['infected']+=1           # so this guy is infected!
            
            if self.lifespan[j]<=0:  #go die!
                self.kill(j)
                
            for k in self.Lat.nodes[(self.x[j],self.y[j])]['walkers'] :        ##!
                if self.infect[k]==0 and k!=j: # healthy guy
                    self.infect[k]=1     # infect him!
                
                    self.sick+=1
                    self.Lat.nodes[(self.x[j],self.y[j])]['infected']+=1
                        
                        
                        
    def reset(self):
        "Reset the params because this runs ... times?"
            
        self.sick,self.dead,self.iterate=0,0,0
    
    
    def cluster_controller(self):
        " Overlook the happenings in an individual Cluster"
    
        while(self.steps>0):   
            self.place()
            self.first_case()         

            while(self.sick>0) and (self.iterate < self.max_iter):
                for j in range(0,self.W):
        
                    self.actions(j)
                    self.neighbors.clear()
                        
                self.ts_sick[self.iterate]+=self.sick
                #        ts_dead[iterate]=dead
                self.ts_ctr[self.iterate]+=1
                self.iterate+=1 
        
            if (self.iterate>self.iter_high) :
                self.iter_high=self.iterate
                self.reset()
                self.steps-=1
  
        # Averaging

        for i in range(self.iter_high):
            self.ts_sick[i]/=self.ts_ctr[i]


    def plot(self): # You might want to mod this!
        " Plot each cluster data"
        plt.plot(range(0,self.iter_high+10),self.ts_sick[0:self.iter_high+10])
        #plt.plot(range(0,iterate+10),ts_dead[0:iterate+10])
        plt.ylabel('Infected')
        plt.xlabel('Discrete Time steps')
        plt.title("Cluster-"+str(self.cluster_id))
        savefig("/home/paul/Documents/COVID/Networks/Cluster"+str(self.cluster_id)+".png",dpi=400)

        #plt.show()
                  




start_time=time.time()

c1=Cluster()
c1.cluster_controller()
c1.plot()
 
elapsed_time=time.time()-start_time
print( time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) )