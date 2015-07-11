#Example of 2D Ising model with Lattice state output

from webplot import p
p.use_doc('ising_model')
import numpy as np

L=10 #define square lattice size

T = 1.5 #temperature Tc = 2.269
I = 2*np.random.randint(2, size=(L,L))-1 #initalize random matrix (LxL) with [-1,1]

#define transition probabilites
w  = np.zeros(5) 
for i in range(5):
    dE = i*4 - 8;   #It makes mapping into -8,-4,0,4,8 from 0,1,2,3,4 
    w[i] = np.exp(-float(dE)/T);


#function to plot lattice
def plotLattice():
    p.figure()
    p.hold('on')
    sd = np.where(I==-1) #spin down
    su = np.where(I==1) #spin up
    l = str(L)
    p.scatter(sd[0],sd[1],color='black',title='2D Ising Model Size: '+l+'x'+l)
    p.scatter(su[0],su[1],color='blue')

#metropolis algorithm
def iterate():
    L = I.shape[0]
    rate = 0
    for x in range(L):
        for y in range(L):
            i = np.random.randint(L) #pick random lattice site
            j = np.random.randint(L)

            S = I[i,j]
            N = I[(i+1)%L, j] + I[i,(j+1)%L] + I[(i-1)%L,j] + I[i,(j-1)%L] #sum nearnest neighbors
            dE = 2*S*N
            dEi = (dE+8)/4 #dEi should be one member of 0 ~ 4 
            
            if w[dEi] >  np.random.random_sample(): #accept spin flip with decaying probabilty
                rate += 1
                I[i,j]= -S
                
                
                
                

plotLattice()
for i in range(5):
    iterate()
plotLattice()
for i in range(5):
    iterate()
plotLattice()
for i in range(5):
    iterate()
plotLattice()
for i in range(5):
    iterate()
plotLattice()
