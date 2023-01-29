# import packages
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_ionq import IonQProvider
import matplotlib.pyplot as plt

provider = IonQProvider(token='vm05jEWtO7zVGE6laZPtx8jbLM66TaS9')
backend = provider.get_backend("ionq_simulator")
# backend = provider.get_backend("ionq_qpu")

class QuantumPersonalityState:

    NUM_QUBITS = 9

    def __init__(self, personality_traits):
        self.personality_traits = [round(x) for x in personality_traits]
        self.qc = QuantumCircuit(self.NUM_QUBITS, self.NUM_QUBITS)
        self.qc.h(range(3))
        self.apply_personality_gates()

    def apply_personality_gates(self,personality_traits=None, start_index=0):
        if personality_traits is None:
            personality_traits = self.personality_traits
        
        for i in range(len(personality_traits)):
            if personality_traits[i] == 1:
                self.qc.x(i+3+start_index)

        # correlate
        for i in range(len(personality_traits)):
            if personality_traits[i] == 1:
                self.qc.toffoli(0, 1, self.NUM_QUBITS-i-1+start_index)
            else:
                self.qc.cnot(2, self.NUM_QUBITS-i-1+start_index)

    def draw(self):
        print(self.qc.draw())

    def get_pfp_reprn(self):
        self.qc.measure(range(self.NUM_QUBITS), range(self.NUM_QUBITS))
        job = backend.run(self.qc, shots=1)
        result = job.result()
        counts = result.get_counts(self.qc)
        # print(result.get_probabilities())
        # get the most common result
        state = max(counts, key=counts.get)
        return list(map(int, reversed(state)))

class EntangledPersonalityState(QuantumPersonalityState):
    NUM_QUBITS = 9

    def __init__(self, personality_traits, friend_traits):
        self.personality_traits = [round(x) for x in personality_traits]
        self.friend_traits = [round(x) for x in friend_traits]
        self.qc = QuantumCircuit(2*self.NUM_QUBITS, 2*self.NUM_QUBITS)
        self.qc.h(range(3))
        # entangle with friend
        for i in range(3):
            self.qc.cx(i, i+self.NUM_QUBITS)
        self.apply_personality_gates()
        self.apply_personality_gates(friend_traits, start_index=self.NUM_QUBITS)

    def get_pfp_reprn(self):
        self.qc.measure(range(2*self.NUM_QUBITS), range(2*self.NUM_QUBITS))
        job = backend.run(self.qc, shots=1)
        result = job.result()
        counts = result.get_counts(self.qc)
        # print(result.get_probabilities())
        # get the most common result
        state = max(counts, key=counts.get)
        two_pfps = list(map(int, reversed(state)))
        return two_pfps[:self.NUM_QUBITS], two_pfps[self.NUM_QUBITS:]
