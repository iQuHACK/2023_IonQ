# import packages
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit import Aer

import numpy as np


from qiskit_ionq import IonQProvider
token = 'Ezy7otlqBB8KVRm5qES55UI9EXOPUfdd'
provider = IonQProvider(token)

simop=0
size=1
speed=0
visible=0

def Jedi_entangle(simop,size, speed, visible):
    # Initiate the circuit
    greg = QuantumRegister(3,'Grogu')
    kbreg = QuantumRegister(3,'knob')
    cr = ClassicalRegister(3, 'Classical Register')
    rmcirq = QuantumCircuit(greg,kbreg, cr)

    # Engtangle Grogu's sense power with the knob's movements
    rmcirq.h(greg[0])
    rmcirq.h(greg[1])
    rmcirq.h(greg[2])
    rmcirq.cx(greg[:], kbreg[:])
    rmcirq.barrier()
    
    # Conditionally applying the X gate to qubits. 
    #If the attacking spaceship size > Mandalorian's spaceship, apply X-gate to greg[0]
    #If the attacking spaceship speed = lightspeed, apply X-gate to greg[1]
    #If the attacking spaceship is invisible, apply X-gate to greg[3]
    if size == 1:
        rmcirq.x(greg[0])
    if speed == 1:
        rmcirq.x(greg[1])
    if visible == 1:
        rmcirq.x(greg[2])
    rmcirq.barrier()
    
    # Applying CX gates and H gates in reverse order to try to return qubits back to its original states
    
    rmcirq.cx(greg[:], kbreg[:])
    rmcirq.h(greg[:])
    rmcirq.barrier()
    
    # Take measurements
    rmcirq.measure(kbreg[:],cr[:])
    
    # Setup backend
    if simop == 0:
        backend = provider.get_backend("ionq_simulator")
    elif simop == 1:
        backend = provider.get_backend("ionq_qpu")

    # Run the program   
    job = backend.run(rmcirq, shots=64)
    result = job.result()
    counts = result.get_counts(rmcirq)
    
    # Map results to knob's movements
    features = np.array(list(counts.keys()))[0]
    rotation = features[0]
    horizontal = features[1]
    vertical = features[2]
    
    return rotation, horizontal, vertical

with open("py2jvs.html", "w") as f:
    f.write("<script>var x = {}; var horizontal = {}; vertical = {} ;</script>".format(x, horizontal, vertical))