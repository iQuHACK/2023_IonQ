# import packages
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ionq import IonQProvider
from playsound import *
import random
from numpy import pi
from numpy.random import choice
provider = IonQProvider(token='1oyMIFGGrziz9w5PtiTVeqPEtOKUGYoe')

class Composer:
    SGL_GATES = ('X','Y','Z','H')
    SGL_GATES_PARAM = ('RX', 'RY', 'RZ')
    TWO_GATES = ('CX', 'CZ')
    
    def __init__(self, n, name):
        self.notes_circuits = []
        self.circ = None
        self.num_qubits = n
        self.name = name
        self.new_note()
        self.final_meas = []
        
    """ Circuit creation """    
    
    def new_note(self):
        self.notes_circuits.append(
            QuantumCircuit(self.num_qubits,self.num_qubits)
        )
        self.circ = self.notes_circuits[-1]
        
        
    # gates = ['X','Y','Z','H']
    def add_single_qubit_gate(self, gate, idx):
        gate = gate.upper()
        if gate not in self.SGL_GATES:
            raise Exception('invalid gate')
        if gate == 'X':
            self.circ.x(idx)
        elif gate == 'Y':
            self.circ.y(idx)
        elif gate == 'Z':
            self.circ.z(idx)
        elif gate == 'H':
            self.circ.h(idx)
        return
    
    # gates = ['RX', 'RY', 'RZ']
    def add_single_qubit_gate_wparam(self, gate, idx, param):
        gate = gate.upper()
        if gate not in self.SGL_GATES_PARAM:
            raise Exception('invalid gate')
        if gate == 'RX':
            self.circ.rx(param, idx)
        elif gate == 'RY':
            self.circ.ry(param, idx)
        elif gate == 'RZ':
            self.circ.rz(param, idx)

    # gate == ['CX', 'CZ']
    def add_two_qubit_gate(self, gate, idx_src, idx_dst):
        gate = gate.upper()
        if gate not in self.TWO_GATES:
            raise Exception('invalid gate')
        if gate == 'CX':
            self.circ.cx(idx_src, idx_dst)
        elif gate == 'CZ':
            self.circ.cz(idx_src, idx_dst)
            
    
    """ Generating the music """
    
    def run_job(self):
        # sends the circuits to hardware/simulator, waits and retrieves results
        # returns a formatted-results file

        final_meas = []
        init_state = random.randint(48, 48+32-1)
        for cir in self.notes_circuits:
            print(cir.draw())

            print('initial', init_state)
            circuit = QuantumCircuit(self.num_qubits, self.num_qubits)

            circuit.prepare_state(init_state, circuit.qubits)
            circuit = circuit.compose(cir)

            circuit.measure(range(self.num_qubits), range(self.num_qubits))
            backend = provider.get_backend("ionq_simulator")#("ionq_simulator")
            transpiled = transpile(circuit, backend)

            job = backend.run(transpiled, shots=1)
            result = job.result()

            counts = result.get_counts()
            print('counts', counts)

            init_state = list(counts.keys())[list(counts.values()).index(1)]
            final_meas.append(init_state)
        self.final_meas = final_meas
    
    def generate_audio(self):
        # creates audio file from note sequence
        print('self.final_meas', self.final_meas)
        play_notes(write_to_midi(self.final_meas))

    
    
    
    """ Display """
    
    def dump(self):
        print("BEGIN COMPOSER")        
        for i, circ in enumerate(self.notes_circuits):
            print ("="*50)
            print(f"\t\tNote {i+1}")
            print(circ.draw())
        print("="*50)
        print("END COMPOSER")