#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 12:31:24 2020

@author: paul
"""


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from random import randrange,uniform
from pylab import savefig

"Adapts corona_walk into a class, to create a net of clusters (lattices) connected by Multigraph network"
 # I think epydemic is there too! But couldn't get it at first go... :)
 



# Global events...
max_timescale=1000
#g_sick, g_dead, g_iterate=0,0,0     # counters
global_sick=np.zeros(max_timescale)      # time series of sick walkers







class Cluster:
    
    " This creates a lattice of random size (m*n) which models any population cluster: big, small, cities, villages, etc."
    
    
    L=20       # Lifetime params
    #max_iter=1000      # in like discrete time-steps
    
    #steps=1         # total number of times 
    ## DOES THIS COMPLICATE? Make this run just once!
    
    neighbors=[]      # Store the neighbors here 
    nodes=[]
    walkers={}
    
    
    n_clusters=0        # (Total number of clusters)-1
    
    total_sick=0
    total_dead=0
    
    def __init__(self, length, width, time_steps, t_gen, density=uniform(1.4,1.6), Lifetime=20 ):
        
        " Generating the length & width randomly helps to create diverse clusters in any random-walk"
        
        self.cluster_id=Cluster.n_clusters      # Each cluster has a cluster-id
        self.t_gen=t_gen        # time of generation of this cluster!
        # t = t' + t_gen
        self.t_p=0      # t'
        
        self.m=length     # self?: Do length & breadth interest us?
        self.n=width
        
        self.N=self.m*self.n      # Lattice size
        self.density=density       # Density per node!
        # Social-distancing affects density!!!
        # HOW??? DENSITY DOESN'T HAVE MUCH OF A ROLL BEYOND POPU. INSTANTIATION!!!
        
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
        self.ts_sick=np.zeros(time_steps)      # time series of sick walkers
        #ts_dead=np.zeros(max_iter)
        
        
        #self.ts_ctr=np.zeros(self.max_iter)       # counter to record each iter for averaging
        #self.iter_high=0                 # The max count of iter (it doesn't go on till max_iter)
        
        Cluster.n_clusters+=1
        
        
    
    
    
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
        
        ##???
        Cluster.total_sick+=1
            
        
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
        
        Cluster.total_sick-=1
        Cluster.total_dead+=1
                
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
                    
                    Cluster.total_sick+=1
                    
                    self.Lat.nodes[(self.x[j],self.y[j])]['infected']+=1
                        
                        
                        
    def reset(self):
        "Reset the params because this runs ... times?"
            
        self.sick,self.dead,self.iterate=0,0,0
    
    
    def initialise(self):
        " Overlook the happenings in an individual Cluster"
    
        #while(self.steps>0):   
        self.place()
        self.first_case()         

        #while(self.sick>0) and (self.iterate < self.max_iter):
        
        
    def cluster_controller(self):
        for j in range(0,self.W):
        
            self.actions(j)
            self.neighbors.clear()
                        
        self.ts_sick[self.t_p]+=self.sick
        #        ts_dead[iterate]=dead
        #self.ts_ctr[self.iterate]+=1
        
        self.t_p+=1
        #self.iterate+=1 
        #??? Updating depends not on Cluster!!!
        
        
        #if (self.iterate>self.iter_high) :
            #print(self.iter_high)
            #self.iter_high=self.iterate
            #self.reset()
            #self.steps-=1
  
        # Averaging

        #for i in range(self.iter_high):
            #self.ts_sick[i]/=self.ts_ctr[i]


    def plot(self): # You might want to mod this!
        " Plot each cluster data"
        plt.plot(range(0,self.t_p+10),self.ts_sick[0:self.t_p+10])
        #plt.plot(range(0,iterate+10),ts_dead[0:iterate+10])
        plt.ylabel('Infected')
        plt.xlabel('Discrete Time steps')
        plt.title("Cluster-"+str(self.cluster_id))
        savefig("/home/paul/Documents/COVID/Networks/Cluster"+str(self.cluster_id)+".png",dpi=400)

        #plt.show()
                  
    
    def show_cluster(self):
        nx.draw(self.Lat)
        savefig("/home/paul/Documents/COVID/Networks/cluster_view.png",dpi=800)


t=0
#start_time=time.time()
time_max=1000
c1=Cluster(50,50,time_max,t)
c1.initialise()

while(c1.sick>0):
    
    c1.cluster_controller()

    
    t+=1
    
c1.plot()
#c1.show_cluster()    
 
#elapsed_time=time.time()-start_time
#print( time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) )


" Okayy! the crooked graph is coz u removed time"
" From the cluster_controller()"