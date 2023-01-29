import csv
import pennylane as qml
from pennylane import numpy as np
from matplotlib import pyplot as plt
from playsound import write_to_midi
from qiskit import Aer, QuantumCircuit, transpile
from random import randint, random
from classifygenre import trainModel, compute_acc

# set the random seed
np.random.seed(42)
num_notes = 15
# create a device to execute the circuit on
dev = qml.device("default.qubit", wires=8)
simulator = Aer.get_backend('aer_simulator')


def circuit(params):
    final_meas = []
    for i in range(num_notes):
        circui = QuantumCircuit(8, 8)
        init_state = 0
        print('initial', init_state)
        circui.prepare_state(init_state, circui.qubits)
        # print('params first', type(params[0+3*i].numpy()))
        circui.rx(params[0+3*i].numpy(), 5) 
        circui.rx(params[1+3*i].numpy(), 6)
        circui.rx(params[2+3*i].numpy(), 7)

        circui.measure(range(8), range(8))

        backend = Aer.get_backend('aer_simulator')

        transpiled = transpile(circui, backend)

        job = backend.run(transpiled, shots=1)
        result = job.result()

        counts = result.get_counts()
        print('counts', counts)

        init_state = list(counts.keys())[list(counts.values()).index(1)]
        final_meas.append(init_state)
    print('final meas!!', final_meas)
    # circuit results -> midi
    midi_file = write_to_midi(final_meas)
    loss = compute_acc(midi_file)
    print('comp', loss)
    return loss

def parameter_shift_term(qnode, params, i):
    shifted = params.copy()
    shifted[i] += np.pi/2
    forward = circuit(shifted)  # forward evaluation

    shifted[i] -= np.pi/2
    backward = circuit(shifted) # backward evaluation

    return 0.5 * (forward - backward)

params = np.random.random([num_notes*3], requires_grad=True)


def parameter_shift(qnode, params):
    gradients = np.zeros([len(params)])

    for i in range(len(params)):
        gradients[i] = parameter_shift_term(qnode, params, i)

    return gradients

print('param 0s', params)
for i in range(1):
    grads = parameter_shift(circuit, params)
    print(grads)
    params = params + np.array(grads)*np.pi/2
    print('params after ',i, ' runs: ', params)
    

with open("final_params.csv","w") as f:
    wr = csv.writer(f,delimiter="\n")
    for ele in params:
        wr.writerow([ele+","])

