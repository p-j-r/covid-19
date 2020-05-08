#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 12:31:24 2020

@author: paul
"""


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from random import randrange,uniform,randint
from pylab import savefig
import time
"Adapts corona_walk into a class, to create a net of clusters (lattices) connected by Multigraph network"
 

# Global events...
max_timescale=5000
global_sick=np.zeros(max_timescale)      # time series of sick walkers



max_clusters=15

transfer_infect={}      # monitors the infected tranferred b/w nodes
G=nx.Graph()
spam=0
max_size=100        # choose even

def spawn_cluster(t,n):
    
    l=randint(max_size/2,max_size)
    b=randint(max_size/2,max_size)
    G.add_node(Cluster(l,b,max_timescale,t))
    
    list(G.nodes)[n].initialise()
    
    #global spam
    #spam+=1




class Cluster:
    
    " This creates a lattice of random size (m*n) which models any population cluster: big, small, cities, villages, etc."
    
    
    L=20       # Lifetime params
    
    
    
    n_clusters=0        # (Total number of clusters)
    
    total_population=0
    total_sick=0
    total_dead=0
    total_sick_series=np.zeros(max_timescale)     # Global sick series!
    cluster_health=np.zeros(max_clusters)       # 0-> infection starts & is ongoing, 1->infection over!
    
    
    def __init__(self, length, width, time_steps, t_gen, density=uniform(0.4,0.6), Lifetime=20 ):
        
        " Generating the length & width randomly helps to create diverse clusters in any random-walk"
        Cluster.n_clusters+=1
        
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
        Cluster.total_population+=self.W
        
        self.sick, self.dead, self.iterate=0,0,0     # counters
    
    
        self.Lat=nx.grid_2d_graph(self.m,self.n)       # A 2-D Lattice
        
        self.neighbors=[]      # Store the neighbors here 
        self.nodes=[]
        self.walkers={}
    
        for i in self.Lat.nodes():
            self.nodes.append(i)
            self.walkers[i]=[]
        
        nx.set_node_attributes(self.Lat,0,'infected')        # Sets the attribute infected, the number of infected peeps at a node at any temporal point 
        nx.set_node_attributes(self.Lat,self.walkers,'walkers')         # Sets the attribute walkers, the walkers at a node

        # 2: One of the nodes will be the 'exit node' for the lattice...{A small world of all exit-nodes}
        self.exit_node=self.nodes[randrange(len(self.nodes))]       # Should a cluster have multiple exits!?
        
        
        
        
        #? Should walker be a different class?
        #? No, a walker is selfless, and for the lattice[We are not interested in individuals!]
        self.x, self.y=np.zeros(self.W), np.zeros(self.W)    # walker x,y coord
        self.infect=np.zeros(self.W)              # walker health status
        self.lifespan=self.L*np.ones(self.W)            # Time left to live
        self.ts_sick=np.zeros(time_steps)      # time series of sick walkers
        #ts_dead=np.zeros(max_iter)
        
        
        
        
        
    
    def place(self):            
        "Place walkers on lattice"
        #print(self.nodes)     
        for j in range(self.W):                   
            self.x[j] , self.y[j]= self.nodes[randrange(len(self.nodes))]
            #print(self.Lat.nodes[ (self.x[j],self.y[j]) ]['walkers']   )
            #print(( self.x[j] , self.y[j] ))
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
        
        
        Cluster.total_sick+=1
        
     
        
    def exit_node_handler(self,j):
        
        global spam
        spam+=1
        where=randint(1,Cluster.n_clusters)
        if(where==self.cluster_id and Cluster.n_clusters!= max_clusters):     # Self-loops aren't allowed: 0 cluster is covered
            spawn_cluster(self.t_gen+self.t_p,Cluster.n_clusters)
            G.add_edge( list(G.nodes)[self.cluster_id-1], list(G.nodes)[Cluster.n_clusters-1] )
            where=Cluster.n_clusters
                
                
        else:
            G.add_edge( list(G.nodes)[self.cluster_id-1], list(G.nodes)[where-1] )
                
        list(G.nodes)[where-1].Lat.nodes[ list(G.nodes)[where-1].exit_node ]['walkers'].append(j)     # Can duplicate id's exist!?   
        if (self.infect[j]==1):     # sick!
            pass
        
        
        self.infect[j]=3    # Removed from this cluster!
        
    def walk(self,j):         
        "Walk the walker to a new location"
            
        for i in self.Lat.neighbors( (self.x[j],self.y[j]) ):
                self.neighbors.append(i)
              
        # remove a walker from node!
        self.Lat.nodes[(self.x[j],self.y[j])]['walkers'].remove(j)     
          
        self.x[j] , self.y[j] =self.neighbors[randrange(len(self.neighbors))]
        
        
        if( ( self.x[j] , self.y[j] ) == self.exit_node):
            self.exit_node_handler(j)
             
        else:
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
    
        self.place()
        self.first_case()         

        
        
    def cluster_controller(self):
        
        if(Cluster.cluster_health[self.cluster_id-1]==1):
            return
        for j in range(0,self.W):
        
            self.actions(j)
            self.neighbors.clear()
                        
        self.ts_sick[self.t_p]+=self.sick
        Cluster.total_sick_series[ (self.t_p + self.t_gen) ] +=self.sick
        #        ts_dead[iterate]=dead
        
        self.t_p+=1
        
        if(self.sick==0):   # Infection over!
            self.plot()
            Cluster.cluster_health[self.cluster_id-1]=1 # Over!
            
        

    def plot(self): # You might want to mod this!
        " Plot each cluster data"
        
        #self.figure=plt.figure()
        x=np.array(range(0,self.t_p))+self.t_gen
        y=np.array(self.ts_sick[0:self.t_p])
        
        plt.plot(x,y)
        #plt.plot(range(0,iterate+10),ts_dead[0:iterate+10])
        plt.axhline(y=self.W,linestyle='--')
        plt.ylabel('Infected')
        plt.xlabel('Discrete Time steps')
        plt.title("Cluster-"+str(self.cluster_id))
        plt.savefig("/home/paul/Documents/COVID/Networks/Cluster"+str(self.cluster_id)+".png",dpi=400)
        plt.clf()
        #plt.show()
                  
    
    def show_cluster(self):
        nx.draw(self.Lat)
        savefig("/home/paul/Documents/COVID/Networks/cluster_view.png",dpi=800)
        plt.clf()
        
        
        
    def global_plot(t):     # Global stats are simply sum of individual cluster stats!
        
        plt.plot(range(0,t),Cluster.total_sick_series[0:t])
        #plt.plot(range(0,iterate+10),ts_dead[0:iterate+10])
        plt.axhline(y=Cluster.total_population,linestyle='--')
        plt.ylabel('Infected')
        plt.xlabel('Discrete Time steps')
        plt.title("Global data")
        savefig("/home/paul/Documents/COVID/Networks/Global.png",dpi=400)
        plt.clf()


t=0

start_time=time.time()

spawn_cluster(t,0)    # 1st cluster

while(Cluster.total_sick>0 and t<max_timescale):
    
    for i in range(Cluster.n_clusters):
        list(G.nodes)[i].cluster_controller()

    
    t+=1

for i in range(Cluster.n_clusters):
   
    list(G.nodes)[i].plot()
    

Cluster.global_plot(t) 

nx.draw(G)
savefig("/home/paul/Documents/COVID/Networks/Global_network.png",dpi=400)

elapsed_time=time.time()-start_time
print( time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) )

