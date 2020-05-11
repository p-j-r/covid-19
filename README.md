# Models

The following epidemiological models for the spread of SARS-CoV-2 (novel coronavirus) have been implemented:  

Agent based network random walks  
-------------

PDF: [pjr.pdf](https://github.com/p-j-r/covid-19/blob/master/pjr.pdf)

![Network-G](https://github.com/p-j-r/covid-19/blob/master/results/Run-8:%20Success!/Global_network.png)
![Network-G_](https://github.com/p-j-r/covid-19/blob/master/results/Run-9:%20Success!/Global_network.png)

Rate of adding of clusters:(It's random!) _Looks like a linear fit though!_
![Rate](https://github.com/p-j-r/covid-19/blob/master/results/Run-9:%20Success!/rate.png)

    
SIR- Stochastic
------

Using Gillespie algorithm a basic SIR model is generated.  
Differential equation solution: [corona_diff](https://github.com/p-j-r/covid-19/blob/master/corona_diff.py)  
Stochastic simulation: [corona_stochastic](https://github.com/p-j-r/covid-19/blob/master/corona_stochastic.py)  
![stochastic](https://github.com/p-j-r/covid-19/blob/master/results/sim_b0.6671291_g0.332871.png)


SIR- Age Structure & Social contact based
---------------
I- Both symptomatic & asymptomatic   
The age and social contact data for India that is needed to construct structured compartment models can be found at the following source:

Age Structure & Contact Matrices: [data](https://github.com/p-j-r/pyross/tree/master/examples/data)   
Research Paper: https://arxiv.org/pdf/2003.12055.pdf
   
[Source-code](https://github.com/p-j-r/covid-19/blob/master/SIR_model_India.py)

![SIaIsR](https://github.com/p-j-r/covid-19/blob/master/results/Analytic_b0.1646692_g0.14285714285714285.png)

[Hotspots & Contact Tracing model](https://github.com/p-j-r/covid-19/blob/master/corona_walk)
----------------

Uses [networkX](https://networkx.github.io/documentation/networkx-1.10/overview.html) package and modelling the disease spread as a [lattice](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.generators.classic.grid_2d_graph.html#networkx.generators.classic.grid_2d_graph), providing a way to identify and isolate the Hotspots.

![Sick people](https://github.com/p-j-r/covid-19/blob/master/results/Lattice_model.png)
![Averaged](https://github.com/p-j-r/covid-19/blob/master/results/Lattice_model__Averaged.png)
