import pennylane as qml
from pennylane import numpy as np
from matplotlib import pyplot as plt
# from playsound import write_to_midi
from qiskit import Aer, QuantumCircuit, transpile

# set the random seed
np.random.seed(42)
num_notes = 10
# create a device to execute the circuit on
dev = qml.device("default.qubit", wires=8)
simulator = Aer.get_backend('aer_simulator')


@qml.qnode(dev, diff_method="parameter-shift")
def circuit(params):
    final_meas = []
    for _ in range(num_notes):
        qml.RX(params[0], wires=0)
        qml.RX(params[1], wires=1)
        qml.RX(params[2], wires=2)
        res = qml.measure(0)
        print('res!!', res)
        # circuit = QuantumCircuit(8, 8)

        # # circuit.measure(range(8), range(8))
        # backend = Aer.get_backend('aer_simulator')

        # transpiled = transpile(circuit, backend)

        # job = backend.run(transpiled, shots=1)
        # result = job.result()

        # counts = result.get_counts()
        # print('counts', counts)

        # init_state = list(counts.keys())[list(counts.values()).index(1)]
        # final_meas.append(init_state)
    # qml.broadcast(qml.CNOT, wires=[0, 1, 2], pattern="ring")

    # qml.RX(params[3], wires=0)
    # qml.RY(params[4], wires=1)
    # qml.RZ(params[5], wires=2)

    # qml.broadcast(qml.CNOT, wires=[0, 1, 2], pattern="ring")
    
    # # circuit results -> midi
    # # midi_file = write_to_midi(bits_arr)
    return qml.expval(qml.PauliY(1) @ qml.PauliZ(2))#laurens_func(midi_file)

def parameter_shift_term(qnode, params, i):
    shifted = params.copy()
    shifted[i] += np.pi/2
    forward = qnode(shifted)  # forward evaluation

    shifted[i] -= np.pi
    backward = qnode(shifted) # backward evaluation

    return 0.5 * (forward - backward)

params = np.random.random([num_notes*3], requires_grad=True)
# gradient with respect to the first parameter
print(parameter_shift_term(circuit, params, 0))


def parameter_shift(qnode, params):
    gradients = np.zeros([len(params)])

    for i in range(len(params)):
        gradients[i] = parameter_shift_term(qnode, params, i)

    return gradients


print(parameter_shift(circuit, params))

grad_function = qml.grad(circuit)
print(grad_function(params)[0])