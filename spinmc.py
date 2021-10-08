'''
Monte carlo simulation for a 2D ising model.
Assuming ferromagnetic Ising model for J>0.
B>0 corresponds to field in the +z direction.
'''

import matplotlib as mpl
import numpy as np


class system():
    '''
    Define spin system
    '''
    
    def __init__(self,J,B,T,Lx,Ly,thermalize,num_sweeps):
        '''
        J: Exchange coupling
        B: Magnetic field
        T: Dimensionless temperature
        Lx, Ly: Extent of lattice in the x and y directions
        '''
        
        'Initialize in random configuaration'
        
        self.system = np.random.rand(Lx,Ly)
        self.system = 1*(self.system < 0.5) - 1*(self.system >= 0.5)
        self.J, self.B = J, B
        self.Lx = Lx
        self.Ly = Ly
        self.N = Lx*Ly
        self.temp = T
        self.thermalize = thermalize
        self.num_sweeps = num_sweeps
        self.magnetization_measurements = []
    

    def nearest_neighbours(self,i,j):
        
        return [((i-1)%self.Lx,j), ((i+1)%self.Lx,j), (i,(j+1)%self.Ly), (i,(j-1)%self.Ly)]

    
    def make_measurements(self):
       
       
        self.magnetization_measurements.append(np.sum(self.system)/self.N)
        
        
    def random_update(self):

        
        #Propose update at random position     
        position = (np.random.randint(self.Lx),np.random.randint(self.Ly))
        NN = self.nearest_neighbours(*position)
        dE = 0

        #Loop through and compute energy difference due to update
        for site in NN:
            
            
            dE += 2*self.J*self.system[site]*self.system[position] + 2*self.B*self.system[position]
            
        #Accept with probability p
        p = np.min([1,np.exp(-dE/self.temp)])
        if np.random.binomial(1,p) == 1:
            self.system[position] *= -1
           

    
    
    def sweep(self,measure = True):
        
        for j in range(2*self.N):

            self.random_update()
            
        if measure:
    
            self.make_measurements()
            
    def init_sweep(self):
        
        print('THERMALIZING')
        for j in range(self.thermalize):
            print('Thermalizing {}/{}'.format(j,self.thermalize))
            self.sweep(measure = False) 
            
    def run(self, init = True):
        
        if init:
        
            self.init_sweep()
        
        print('RUNNING T = {}'.format(self.temp))
        [self.sweep(measure = True) for j in range(self.num_sweeps)]
        
        return self.system, self.magnetization_measurements
    
J, B = 1.0, 0.0
Lx, Ly = 25, 25
T = 1
thermalize = 300
num_sweeps = 500

ising = system(J,B,T,Lx,Ly,thermalize,num_sweeps)
state, measurements = ising.run()
print(state)
print(np.average(measurements))
    




        
        
        
        
        
        
 
 