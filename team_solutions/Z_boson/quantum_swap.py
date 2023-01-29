import numpy as np
from qiskit import QuantumCircuit, assemble, Aer
from qiskit.visualization import plot_histogram
from qiskit.extensions import UnitaryGate

# generate a unitary transformation between states, using 0 <= x <= 1 to
# denote the proportion of the latter state   
def partial_swap(x = 0):
    U = np.zeros((4, 4))
    U[0, 0] = 1
    U[1, 1] = np.sqrt(1 - x)
    U[1, 2] = np.sqrt(x)
    U[2, 1] = -np.sqrt(x)
    U[2, 2] = np.sqrt(1 - x)
    U[3, 3] = 1
    
    gate = UnitaryGate(U)
    return gate
    
def amplitude_to_angle(p):
    # factor of 0.999 to ensure argument to arcsin < 1
    theta = 2*np.arcsin(np.sqrt(p))
    return theta
    
def loop_matrices(A, B, x):
    (n_durations, n_notes) = A.shape
    
    # make sure that B is the same shape
    if A.shape != B.shape:
        raise ValueError('The matrices are not of the same shape')
        
    C = np.zeros(A.shape)
    
    for i in range(n_durations):
        for j in range(n_notes):
            p_a = A[i, j]
            p_b = B[i, j]
            
            theta_a = amplitude_to_angle(p_a)
            theta_b = amplitude_to_angle(p_b)
            
            C[i, j] = get_cij(theta_a, theta_b, x)
            
    return C
            
            
def get_cij(theta_a, theta_b, x):
    qc = QuantumCircuit(2)
    qc.rx(theta_a, 0) # rotate qbit 0
    qc.rx(theta_b, 1) # rotate qbit 1
    
    U_swap = partial_swap(x) 
    
    qc.append(U_swap, [0, 1]) # apply swap gate
    qc.measure_all()
    
    # simulate the results
    sim = Aer.get_backend('aer_simulator') 
    result = sim.run(qc).result()
    
    counts = result.get_counts()
    
    # estimate the probabilities from the frequency of counts
    counts_arr = np.array(list(counts.values()))
    freq_arr = counts_arr/np.sum(counts_arr)
    
    cij = 0
    for i in range(len(counts)):
        key = list(counts.keys())[i]
        # if qbit 0 is in state 1, add the probability to running total
        if key[1] == '1':
            cij += freq_arr[i]
 
    return cij
    
    
def loop_x(A, B, x_list):
    n = len(x_list) # number of fractions to loop over
    
    C = [None for _ in range(n)]
    
    for i in range(n):
        C[i] = loop_matrices(A, B, x_list[i])
        
    return C
        
def main():
    A = np.loadtxt('csv/A.csv', delimiter=',')
    B = np.loadtxt('csv/B.csv', delimiter=',')
    
    # fractions for which to apply quantum swap
    x_list = np.array([0, 0.2, 0.5, 0.8, 1.0])
    
    AB = loop_x(A, B, x_list)
    
    for i in range(len(AB)):
        np.savetxt("csv/AB" + str(x_list[i]) + ".csv", AB[i], delimiter = ',')
        
        
if __name__ == "__main__":
    main()
    