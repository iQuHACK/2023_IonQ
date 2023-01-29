import pennylane as qml
from pennylane import numpy as np
from matplotlib import pyplot as plt
from playsound import write_to_midi
from qiskit import Aer, QuantumCircuit, transpile
from random import randint, random
from classifygenre import trainModel, compute_acc
import warnings
warnings.filterwarnings("ignore")
import sys
class DevNull:
    def write(self, msg):
        pass
sys.stderr = DevNull()

# set the random seed
np.random.seed(42)
num_notes = 10
# create a device to execute the circuit on
dev = qml.device("default.qubit", wires=8)
simulator = Aer.get_backend('aer_simulator')

@qml.qnode(dev, diff_method="parameter-shift")
def circuit(params):
    final_meas = []
    for i in range(num_notes):
        circui = QuantumCircuit(8, 8)
        init_state = randint(0, pow(2, 8)-1)
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
    try:
        shifted = params.copy()
        shifted[i] += np.pi/2
        forward = qnode(shifted)  # forward evaluation
    except:
        forward = 0
    
    try:
        shifted[i] -= np.pi/2
        backward = qnode(shifted) # backward evaluation
    except:
        backward = 0

    return 0.5 * (forward - backward)

params = np.random.random([num_notes*3], requires_grad=True)
# gradient with respect to the first parameter
print(parameter_shift_term(circuit, params, 0))


def parameter_shift(qnode, params):
    gradients = np.zeros([len(params)])

    for i in range(len(params)):
        gradients[i] = parameter_shift_term(qnode, params, i)

    return gradients

print('param 0s', params)
for _ in range(1):
    grads = parameter_shift(circuit, params)
    print(grads)
    params = params + np.array(grads)*np.pi/2
    print('params', params, type(params))
    params = np.array(params, requires_grad=True)
    print(type(params))


# grad_function = qml.grad(circuit)
# print(grad_function(params)[0])