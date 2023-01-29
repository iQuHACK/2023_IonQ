
from qiskit import QuantumCircuit, execute
import numpy as np
from math import pi
from qiskit import QuantumCircuit, quantum_info as qi
import matplotlib.pyplot as plt
import random


def local_simulator():
    from qiskit import Aer
    provider = simulator = Aer
    backend = simulator.get_backend('aer_simulator')


def make_line ( length ):
    n = int(np.ceil(np.log(length)/np.log(2)))
    line = ['0','1']
    for j in range(n-1):
        cp0 = []
        for string in line:
            cp0.append (string+'0')
        cp1 = []
        for string in line[::-1]:
            cp1.append (string+'1')
        line = cp0+cp1
    return line


def make_grid(X, Y):
    line_X = make_line(X)
    line_Y = make_line(Y)
    grid = {}
    for x in range(X):
        for y in range(Y):
            grid[ line_X[x]+line_Y[y] ] = (x,y)
    return grid


def random_height(X, Y):
    height = {}
    for x in range(X):
        for y in range(Y):
            if random.random() < 0.05:
                height[(x, y)] = 1.
    return height

def plot_2d(height, X, Y, log=False):
    
    H = [[0] * X for _ in range(Y)]
    for x in range(X):
        for y in range(Y):
            if log:
                H[Y-1-y][x] = np.log(height.get((x, y), 0))
            else:    
                H[Y-1-y][x] = height.get((x, y), 0)
    plt.imshow(H)
    plt.show()
    plt.clf()
        
        
def height2circuit(height, X, Y):
    # determine grid size
    # make grid
    grid = make_grid(X, Y)
    # determine required qubit number
    n_x = int(np.ceil(np.log(X)/np.log(2))) # create empty state
    n_y = int(np.ceil(np.log(Y)/np.log(2)))
    n = n_x + n_y
    
    state = [0]*(2**(n_x + n_y))
    # fill state with required amplitudes H=0
    H = 0
    for bit_string in grid:
        (x,y) = grid[bit_string]
        if (x,y) in height:
            h = height[x,y]
            state[ int(bit_string,2) ] = np.sqrt( h )
            H += h
    
    # normalize state
    for j,amp in enumerate(state):
        state[ j ] = amp/np.sqrt(H)
        
    # define and initialize quantum circuit
    qc = QuantumCircuit(n,n)
    qc.initialize(state, range(n))
    
    return qc, grid        

        
def circuit2height(qc, grid, theta=np.pi/10):
    # get the number of qubits from the circuit
    n = qc.num_qubits
    
    ######################################
    qc.ry(theta, [i for i in range(n)])
    
    
    ######################################
    
    ket = qi.Statevector(qc.data[0][0].params)
    qc.data.pop(0)
    # evolve this by the rest of the circuit
    ket = ket.evolve(qc)
    
    # extract the output probabilities
    p = ket.probabilities_dict()
    
    # determine maximum probs value for rescaling
    max_h = max( p.values() )
    
    # set height to rescaled probs value
    height = {}
    for bit_string in p:
        if bit_string in grid:
            height[grid[bit_string]] = p[bit_string]/max_h
    return height

def blur(height, X, Y, theta):
    qc, grid = height2circuit(height, X, Y)
    height = circuit2height(qc, grid, theta=theta)
    return height
        
if __name__ == "__main__":

    X, Y = 12, 5
    from copy import deepcopy
    height = random_height(X, Y)
    height_ = deepcopy(height)
    plot_2d(height_, X, Y)

    for i in range(1,6):
        height_ = deepcopy(height)
        height_ = blur(height_, X, Y, theta=np.pi*i/10)
        plot_2d(height_, X, Y)
