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
max_timescale=10000
global_sick=np.zeros(max_timescale)      # time series of sick walkers



max_clusters=20

transfer_infect={}      # monitors the infected tranferred b/w nodes
G=nx.DiGraph()
spam=0
max_size=250        # choose even

def spawn_cluster(t,n):
    " Spawn a new object of class cluster"
    
    l=randint(max_size/2,max_size)
    b=randint(max_size/2,max_size)
    G.add_node(Cluster(l,b,max_timescale,t))
    
    list(G.nodes)[n].initialise()
    
    



class Cluster:
    
    " This creates a lattice of random size (m*n) which models any population cluster: big, small, cities, villages, etc."
    
    
    
    
    
    
    n_clusters=0        # (Total number of clusters)
    
    total_population=0
    total_sick=0
    total_dead=0
    total_sick_series=np.zeros(max_timescale)     # Global sick series!
    cluster_health=np.zeros(max_clusters)       # 0-> infection starts & is ongoing, 1->infection over!
    
    cluster_born=np.zeros(max_clusters)     # Stores t_gen for every cluster
    cluster_n=np.zeros(max_clusters)        # Stores n_clusters corresponding to t_gen
    
    def __init__(self, length, width, time_steps, t_gen, density=uniform(0.4,1.6), Lifetime=14 ):
        
        " Generating the length & width randomly helps to create diverse clusters in any random-walk"
        Cluster.n_clusters+=1
        
        Cluster.cluster_n[ Cluster.n_clusters-1 ]=Cluster.n_clusters
        Cluster.cluster_born[ Cluster.n_clusters-1 ]=t_gen
        
        self.cluster_id=Cluster.n_clusters      # Each cluster has a cluster-id
        self.t_gen=t_gen        # time of generation of this cluster!
        # t = t' + t_gen
        self.t_p=0      # t'
        
        self.m=length     # self?: Do length & breadth interest us?
        self.n=width
        self.L=Lifetime
        
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
         
        #No, a walker is selfless, and for the lattice[We are not interested in individuals!]
        self.x, self.y= [] , []    # walker x,y coord
                  
        self.infect=[]      # walker health status
        self.lifespan=[]            # Time left to live
        self.ts_sick=np.zeros(time_steps)      # time series of sick walkers
        
        #ts_dead=np.zeros(max_iter)
        
        
        
        
        
    
    def place(self):            
        "Place walkers on lattice"
        #print(self.nodes)     
        for j in range(self.W):                   
            x_ , y_  = self.nodes[randrange(len(self.nodes))]
            self.x.append(x_) 
            self.y.append(y_) 
            self.infect.append(0)
            self.lifespan.append(self.L)
            
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
        if(  where==self.cluster_id  and Cluster.n_clusters!= max_clusters):     # Self-loops aren't allowed: 0 cluster is covered
            spawn_cluster(self.t_gen+self.t_p,Cluster.n_clusters)
            G.add_edge( list(G.nodes)[self.cluster_id-1], list(G.nodes)[Cluster.n_clusters-1] )
            where=Cluster.n_clusters
            transfer_infect[ list(G.nodes)[self.cluster_id-1], list(G.nodes)[where-1] ]=0
                
        else:
            if( not(G.has_edge(list(G.nodes)[self.cluster_id-1],list(G.nodes)[where-1]) ) ):
                G.add_edge( list(G.nodes)[self.cluster_id-1], list(G.nodes)[where-1] )
            if (self.infect[j]==1):     # sick!
                #transfer_infect[ list(G.nodes)[self.cluster_id-1], list(G.nodes)[where-1] ]+=1
                pass
        
        node_=list(G.nodes)[where-1]
           
        node_.Lat.nodes[ node_.exit_node ]['infected']+=1       
        # Okay! Give him a new identity!!!
        node_.W+=1
        node_.Lat.nodes[ node_.exit_node ]['walkers'].append(node_.W-1)     
        node_.infect.append(self.infect[j])
        node_.lifespan.append(self.lifespan[j])
        x_,y_=node_.exit_node
        node_.x.append(x_)
        node_.y.append(y_)
        
        if (self.infect[j]==1):     # sick!
            self.sick-=1
            node_.sick+=1
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
                    
        if self.infect[j]<2:     #still alive
            self.walk(j)
        
                        
                        
                        
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
        
        x=np.array(range(0,self.t_p))+self.t_gen
        y=np.array(self.ts_sick[0:self.t_p])
        
        
        #l1=nx.get_node_attributes(self.Lat,'infected')
        #ls1 = [ f'{key} : {l1[key]}' for key in l1 ]
        # write string one by one adding newline
        #with open(r"/home/paul/Documents/COVID/Networks/dump_infected"+str(self.cluster_id)+".txt", 'w') as my_file:
            #[ my_file.write(f'{st}\n') for st in ls1 ]
        
        #l2=nx.get_node_attributes(self.Lat,'walkers')
        #ls2 = [ f'{key} : {l2[key]}' for key in l2 ]
        #with open(r"/home/paul/Documents/COVID/Networks/dump_walkers"+str(self.cluster_id)+".txt", 'w') as my_fil:
            #[ my_fil.write(f'{st}\n') for st in ls2 ]
        
        
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
        
    def rate_clustering():
        
        plt.ylabel('Number of clusters')
        plt.xlabel('Time')
        
        plt.scatter(Cluster.cluster_born[0:Cluster.n_clusters] , Cluster.cluster_n[0:Cluster.n_clusters])
        savefig("/home/paul/Documents/COVID/Networks/rate.png",dpi=400)
        plt.clf()


t=0

start_time=time.time()

spawn_cluster(t,0)    # 1st cluster

while(Cluster.total_sick>0 and t<max_timescale):
    
    for i in range(Cluster.n_clusters):
        list(G.nodes)[i].cluster_controller()

    
    t+=1

#for i in range(Cluster.n_clusters):
    # If the infection gets over, it'll automatically plot!
    # Else plot manually!
    #list(G.nodes)[i].plot()
    
Cluster.global_plot(t) 
Cluster.rate_clustering()
#nx.set_edge_attributes(G,transfer_infect)

#print(transfer_infect)

nx.draw(G)
savefig("/home/paul/Documents/COVID/Networks/Global_network.png",dpi=400)

elapsed_time=time.time()-start_time
print( time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) )

