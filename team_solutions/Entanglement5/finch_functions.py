from qiskit import QuantumCircuit
from qiskit_ionq import IonQProvider
from qiskit import transpile
from math import pi

import numpy as np
import matplotlib.pyplot as plt
from qiskit_ionq import IonQProvider

class finchEvolver:
    """ class containing all the functions relating to the quantum circuit side of the evolution of finches """
    
    def __init__(self, token='eHMFfV9o1gffeXCQLlpzKdh1nvoGUT1A', N_finches=2, characteristics_per_finch=4):
        self.provider = IonQProvider(token=token)
        
        self.N_finches = N_finches
        self.characteristics_per_finch = characteristics_per_finch
        
        self.qcircuit = None
        
    def finch_init(self, finch_N, theta_i):
        
        """ 
        initializes finches with rotations given by:
        finch_N (int): which finch you are addressing
        theta_i (array or list): vector of angles specifying the rotation amount for each characteristic
        """
        
        # single qubit rotations
        for ii in range(self.characteristics_per_finch):
            qubit_N = ii+self.characteristics_per_finch*finch_N
            self.qcircuit.rx(theta_i[qubit_N],qubit_N)
        
    
    def intra_finch_evolution(self, finch_N, theta_intra):
        
        """ 
        builds gates for interactions fo the characteristics within a single finch, given by:
        finch_N (int): which finch you are addressing
        theta_intra (array or list): vector of angles specifying the interaction amount for each characteristic pair
        """
        
        # correlation between wingspan and body size
        self.qcircuit.crx(theta_intra[finch_N][0],
                          0+self.characteristics_per_finch*finch_N,
                          2+self.characteristics_per_finch*finch_N)
        self.qcircuit.crx(theta_intra[finch_N][0],
                          2+self.characteristics_per_finch*finch_N,
                          0+self.characteristics_per_finch*finch_N)
        
        # correlation between beak size and body size
        self.qcircuit.crx(theta_intra[finch_N][1],
                          1+self.characteristics_per_finch*finch_N,
                          2+self.characteristics_per_finch*finch_N)
        self.qcircuit.crx(theta_intra[finch_N][1],
                          2+self.characteristics_per_finch*finch_N,
                          1+self.characteristics_per_finch*finch_N)
        

    def inter_finch_evolution(self, finch_Ns, characteristic, theta_inter):
        
        """ 
        builds gates for interactions fo the characteristics between finches, given by:
        finch_Ns (list): which finches are interacting (length 2)
        characteristic (array or list): which characteristics of the finches are getting mixed
        theta_inter (array or list): vector of angles specifying the mixing amount betwene the finches for each characteristic
        """

        for ii in range(len(characteristic)):
            self.partial_swap(finch_Ns, characteristic[ii], theta_inter[ii])

    def create_quantum_circuit(self, theta_i, theta_intra, theta_inter):
        
        """ 
        builds quantum circuit for evolution simulation, with:
        theta_i (array or list): angles for initialization
        theta_intra (array or list): angles for intra-finch interactions
        theta_inter (array or list): angles for inter-finch interactions
        """

        self.qcircuit = QuantumCircuit(self.N_finches*self.characteristics_per_finch,self.N_finches*self.characteristics_per_finch)
        
        
        # initialization and primary evolution of characteristics of individual finches
        for ii in range(self.N_finches):
            self.finch_init(ii, theta_i)
            self.intra_finch_evolution(ii, theta_intra)
        self.qcircuit.barrier()

        # interactions in between finches
        self.inter_finch_evolution([0,1], [0,3], theta_inter)
        
        # secondary evolution of characteristics of individual finches
        for ii in range(self.N_finches):
            self.intra_finch_evolution(ii, theta_intra)
        self.qcircuit.barrier()

        self.qcircuit.measure(range(self.characteristics_per_finch*self.N_finches), range(self.characteristics_per_finch*self.N_finches))  


    def partial_swap(self, finch_Ns, characteristic, theta_inter):
        
        """ 
        implements partial swap, which is essentially a gradual swap given by angle theta_inter.
        For example, if theta_inter=0, this results in identity, if if theta_inter=pi, this
        results in a SWAP gate, and if theta_inter=pi/2, this results in a sqrt(SWAP) gate
        finch_Ns (array or list): which finches the partial swap is applied on
        characteristic (int): which characteristic the partial swap is applied on
        theta_inter (float): "amount" of swapping, as explained above
        """

        self.qcircuit.crx(pi, characteristic+finch_Ns[0]*self.characteristics_per_finch, 
                          characteristic+finch_Ns[1]*self.characteristics_per_finch)

        self.qcircuit.crx(theta_inter, characteristic+finch_Ns[1]*self.characteristics_per_finch, 
                          characteristic+finch_Ns[0]*self.characteristics_per_finch)

        self.qcircuit.crx(pi, characteristic+finch_Ns[0]*self.characteristics_per_finch, 
                          characteristic+finch_Ns[1]*self.characteristics_per_finch)
        self.qcircuit.barrier()


    def characteristic_results_from_outcome(self,counts,shots):
        
        """ 
        based on the outcome of an experiment, this function returns the distribution of
        each characteristic for each finch.
        counts (dict): outcome of experiment/simulation
        shots (int): number of repeats of the experiment/simulation
        """

        characteristic_results = np.zeros(self.N_finches*self.characteristics_per_finch)

        for kk in range(len(characteristic_results)):
            for ii in range(2**(len(characteristic_results)-1)):
                string = np.binary_repr(ii,width=(len(characteristic_results)-1))[:kk]+str(1)+np.binary_repr(ii,width=(len(characteristic_results)-1))[kk:]
                if string in counts:
                    characteristic_results[kk] += counts[string]

        return characteristic_results/shots

    def theta_is_from_outcome(self,characteristic_results):
        
        """ 
        based on the characteristic distribution of finches, this function returns the initial 
        rotations to prepare the quantum state with same distributions.
        characteristic_results (array): distribution of characteristics
        """
        
        theta_i = np.arccos(np.sqrt(characteristic_results))
        return 2*theta_i

    def natural_selection_modifier(self,theta_i, preferred_characteristics, multiplier):
        """ 
        based on the initial rotations and which characteristics are "preferred" (due to natural
        selection), returns a new set rotations for initialization.
        theta_i (array): initial array of rotations
        preferred_characteristics (array): which characteristics are more likely, towards which
        the distribution will be pushed
        multiplier (array): defines how strong a natural selection process is for different 
        characteristics from 0 to 1, with 1 --> complete forcing of characteristic, and 
        0 --> no natural selection at all
        """
        return multiplier*(pi*preferred_characteristics-theta_i) + theta_i

    def multi_generation_evolution_plotting(self, N_gen, theta_i, theta_intra, theta_inter, preferred_characteristics, multiplier, shots, noise_model=None):
        """ 
        this function simulates a full, multi-generational evolution of finch characteristics and plots the
        distributions for each generation, with:
        N_gen (int): number of generations
        theta_i (array or list): angles for first round initialization
        theta_intra (array or list): angles for intra-finch interactions
        theta_inter (array or list): angles for inter-finch interactions
        preferred_characteristics (array): which characteristics are more likely, towards which
        the distribution will be pushed
        multiplier (array): defines how strong a natural selection process is for different 
        characteristics from 0 to 1, with 1 --> complete forcing of characteristic, and 
        0 --> no natural selection at all
        shots (int): number of repeats for a given generation (can be thought of as population size)
        noise_model (str): which noise model to use: 'aria-1' or 'harmony'. If None is set, will not use noise_model
        """
        
        fig, ax = plt.subplots(figsize=(13,6))
        label_locs = np.arange(len(theta_i))
        width = 0.7/(N_gen+1)
        
        labels = []
        for ii in range(self.N_finches):
            labels.append('color finch ' + str(ii+1))
            labels.append('beak size finch ' + str(ii+1))
            labels.append('wingspan finch ' + str(ii+1))
            labels.append('fatness finch ' + str(ii+1))
            
        colors = plt.cm.Blues(np.linspace(0.2,1,N_gen + 1))
        ax.set_xticks(label_locs, labels, rotation = 45)
        ax.bar(label_locs - N_gen * width/2, np.sin(theta_i[::-1]/2)**2, width, label = 'Gen 0', color = colors[0])
        ax.set_ylim([0,1])
        
        backend = self.provider.get_backend("ionq_simulator")

        for generation in range(N_gen):

            self.create_quantum_circuit(theta_i, theta_intra, theta_inter)

            job = backend.run(self.qcircuit, shots=shots)
            result = job.result()
            counts = result.get_counts()

            characteristic_results = self.characteristic_results_from_outcome(counts,shots)

            theta_i = self.theta_is_from_outcome(characteristic_results)

            theta_i = self.natural_selection_modifier(theta_i, preferred_characteristics, multiplier)

            ax.bar(label_locs - (N_gen - 2 - 2*generation)*width/2, characteristic_results, width, label = 'Gen %s'%(generation + 1), color = colors[generation + 1])
        
        ax.legend()
        
        
    def multi_generation_evolution_just_data(self, N_gen, theta_i, theta_intra, theta_inter, preferred_characteristics, multiplier, shots, noise_model=None):
        """ 
        this function simulates a full, multi-generational evolution of finch characteristics and returns
        data containing the distributions for each generation and a dictionary containing all raw data 
        for each generation, with:
        N_gen (int): number of generations
        theta_i (array or list): angles for first round initialization
        theta_intra (array or list): angles for intra-finch interactions
        theta_inter (array or list): angles for inter-finch interactions
        preferred_characteristics (array): which characteristics are more likely, towards which
        the distribution will be pushed
        multiplier (array): defines how strong a natural selection process is for different 
        characteristics from 0 to 1, with 1 --> complete forcing of characteristic, and 
        0 --> no natural selection at all
        shots (int): number of repeats for a given generation (can be thought of as population size)
        noise_model (str): which noise model to use: 'aria-1' or 'harmony'. If None is set, will not use noise_model
        """
        
        data = np.zeros([N_gen+1, self.N_finches*self.characteristics_per_finch])

        data[0,:] = np.sin(theta_i[::-1]/2)**2
        
        backend = self.provider.get_backend("ionq_simulator")
            
        raw_data = dict()

        for generation in range(N_gen):

            self.create_quantum_circuit(theta_i, theta_intra, theta_inter)
            
            if noise_model is not None:
                job = backend.run(self.qcircuit, shots=shots, noise_model=noise_model)
            else:
                job = backend.run(self.qcircuit, shots=shots)
                
            result = job.result()
            counts = result.get_counts()
            
            raw_data['gen'+str(generation+1)] = counts

            characteristic_results = self.characteristic_results_from_outcome(counts,shots)

            theta_i = self.theta_is_from_outcome(characteristic_results)

            theta_i = self.natural_selection_modifier(theta_i, preferred_characteristics, multiplier)

            data[generation+1,:] = characteristic_results

        return data, raw_data
        
    def multi_generation_evolution_just_data_harmony(self, N_gen, theta_i, theta_intra, theta_inter, preferred_characteristics, multiplier, shots):
        
        """ 
        this function runs a full, multi-generational evolution of finch characteristics  on the 
        harmony qpu and returns data containing the distributions for each generation and a dictionary 
        containing all raw data for each generation, with:
        N_gen (int): number of generations
        theta_i (array or list): angles for first round initialization
        theta_intra (array or list): angles for intra-finch interactions
        theta_inter (array or list): angles for inter-finch interactions
        preferred_characteristics (array): which characteristics are more likely, towards which
        the distribution will be pushed
        multiplier (array): defines how strong a natural selection process is for different 
        characteristics from 0 to 1, with 1 --> complete forcing of characteristic, and 
        0 --> no natural selection at all
        shots (int): number of repeats for a given generation (can be thought of as population size)
        """
        
        data = np.zeros([N_gen+1, self.N_finches*self.characteristics_per_finch])

        data[0,:] = np.sin(theta_i[::-1]/2)**2
        
        backend = self.provider.get_backend("ionq_qpu")
        
        raw_data = dict()

        for generation in range(N_gen):

            self.create_quantum_circuit(theta_i, theta_intra, theta_inter)

            job = backend.run(self.qcircuit, shots=shots)
            result = job.result()
            counts = result.get_counts()
            
            raw_data['gen'+str(generation+1)] = counts

            characteristic_results = self.characteristic_results_from_outcome(counts,shots)

            theta_i = self.theta_is_from_outcome(characteristic_results)

            theta_i = self.natural_selection_modifier(theta_i, preferred_characteristics, multiplier)

            data[generation+1,:] = characteristic_results
            
        return data, raw_data
    
    def multi_generation_evolution_just_data_aria(self, N_gen, theta_i, theta_intra, theta_inter, preferred_characteristics, multiplier, shots):
        
        """ 
        this function runs a full, multi-generational evolution of finch characteristics  on the 
        aria qpu and returns data containing the distributions for each generation and a dictionary 
        containing all raw data for each generation, with:
        N_gen (int): number of generations
        theta_i (array or list): angles for first round initialization
        theta_intra (array or list): angles for intra-finch interactions
        theta_inter (array or list): angles for inter-finch interactions
        preferred_characteristics (array): which characteristics are more likely, towards which
        the distribution will be pushed
        multiplier (array): defines how strong a natural selection process is for different 
        characteristics from 0 to 1, with 1 --> complete forcing of characteristic, and 
        0 --> no natural selection at all
        shots (int): number of repeats for a given generation (can be thought of as population size)
        """
        
        data = np.zeros([N_gen+1, self.N_finches*self.characteristics_per_finch])

        data[0,:] = np.sin(theta_i[::-1]/2)**2
        
        backend = self.provider.get_backend("ionq_qpu.aria-1")
        
        raw_data = dict()

        for generation in range(N_gen):

            self.create_quantum_circuit(theta_i, theta_intra, theta_inter)

            job = backend.run(self.qcircuit, shots=shots)
            result = job.result()
            counts = result.get_counts()
            
            raw_data['gen'+str(generation+1)] = counts

            characteristic_results = self.characteristic_results_from_outcome(counts,shots)

            theta_i = self.theta_is_from_outcome(characteristic_results)

            theta_i = self.natural_selection_modifier(theta_i, preferred_characteristics, multiplier)

            data[generation+1,:] = characteristic_results
            
        return data, raw_data
        
        
    def draw_q_circuit(self, theta_i, theta_intra, theta_inter):
        
        """ 
        this function shows a drawing of the implemented quantum circuit for given input angle values:
        theta_i (array or list): angles for first initialization
        theta_intra (array or list): angles for intra-finch interactions
        theta_inter (array or list): angles for inter-finch interactions
        """
        
        self.create_quantum_circuit(theta_i, theta_intra, theta_inter)
        
        backend = self.provider.get_backend("ionq_simulator")
        
        transpiled = transpile(self.qcircuit, backend)
        print(transpiled)
