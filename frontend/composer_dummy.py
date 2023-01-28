from qiskit import QuantumCircuit

class Composer:
    def __init__(self, n):
        self.notes_circuits = []
        self.num_qubits = n
        
    """ Circuit creation """    
    
    def new_note(self):
        self.notes_circuits.append(
            QuantumCircuit(self.num_qubits,self.num_qubits)
        )
        pass

    def add_single_qubit_gate(self, gate, idx):

        pass

    def add_single_qubit_gate_wparam(self, gate, idx, param):

        pass

    def add_two_qubit_gate(self, gate, idx_src, idx_dst):

        pass
    
    """ Generating the music """
    
    def run_job():
        # sends the circuits to hardware/simulator, waits and retrieves results
        
        # returns a formatted-results file
        return None
    
    def map_to_notes(results):
        # applies mapping to results to generate a sequence of notes
        
        return None
    
    def generate_audio(notes):
        # creates audio file from note sequence
        
        return None
    
    def compose():
        results = run_job()
        notes = map_to_notes(results)
        return generate_audio(notes)