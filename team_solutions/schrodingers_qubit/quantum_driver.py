import numpy as np
import qiskit
from qiskit import QuantumCircuit, Aer
from qiskit.tools.visualization import plot_histogram, plot_state_city
from qiskit.circuit import Parameter
from qiskit_ionq import IonQProvider


# global params
no_qubits = 8

provider = IonQProvider("CW8P78VEqL4NFcMKkXMq5tFu193Hzazs")
backend = provider.get_backend("ionq_simulator")

def bind(circ, vals_dict):
    return circ.bind_parameters(vals_dict)

def compute_scores(probabilities):
    vid_counts = {i: 0 for i in range(len(list(probabilities.keys())[0]))}
    #print(vid_counts)
    for key, val in probabilities.items():
        #print(key, val)
        for i in range(len(key)):
            vid_counts[i] += float(key[i])*val
    #print(vid_counts)
    #vid_counts = {key:val/sum(vid_counts.values()) for key,val in vid_counts.items()}
    return vid_counts

def get_quantum_parameters(no_outputs, inputs):
    # setup
    no_qubits = np.int(np.ceil(np.log(no_outputs)/np.log(2)))
    print(no_qubits, np.log(no_outputs)/np.log(2))
    params = {}
    for i in range(no_qubits):
        params[f"video_{i}"] = Parameter(f"v_{i}")
    
    # prepare circuit
    qfm = qiskit.QuantumCircuit(no_qubits)
    #qfm.prepare_state([1/np.sqrt(2**no_qubits)+0j]*2**no_qubits)
    for i in range(no_qubits):    
        qfm.rx(params[f"video_{i}"], i)
    qfm.measure_all()
    qfm_bound = bind(qfm, inputs)

    job = backend.run(qiskit.compiler.transpile(qfm_bound, backend), shots=10000)
    probabilities = job.get_probabilities() 
    return compute_scores(probabilities)

def get_quantum_parameters_one_step(no_vids, inputs_var1, inputs_var2):
    """ inputs_var1, inputs_var2: no_videos """
    # setup
    no_qubits = no_vids * 2
    print("no_qubits", no_qubits, "len(inputs_var1)", len(inputs_var1))
    params = {}
    for i in range(no_vids):
        for j in [0,1]: # different features
            params[f"v{i}_f{j}"] = Parameter(f"v{i}_f{j}")
    print(params)
    
    # prepare circuit
    qfm = qiskit.QuantumCircuit(no_qubits)
    #coupling = [list(range(i,i+2)) for i in [0,2]]
    my_list = list(range(no_qubits))
    coupling = []
    for i in range(0, no_qubits, 2):
        x = i
        coupling.append((my_list[x:x+2]))
    print("COUPLING", coupling)
    for pair in coupling:
        print(pair, pair[0], pair[1])
        qfm.cx(pair[0], pair[1])
    #qfm.prepare_state([1/np.sqrt(2**no_qubits)+0j]*2**no_qubits)
    counter = 0
    for i in range(no_vids):
        for j in [0,1]: # different features
            params[f"v{i}_f{j}"] = Parameter(f"v{i}_f{j}")
            qfm.rx(params[f"v{i}_f{j}"], counter)
            counter += 1
    qfm.measure_all()
    inputs_var1_dict, inputs_var2_dict = {}, {}
    for i in range(no_vids):
        print(i, inputs_var1, inputs_var2)
        inputs_var1_dict[params[f"v{i}_f{0}"]]= inputs_var1[i]
        inputs_var2_dict[params[f"v{i}_f{1}"]]= inputs_var2[i]
    print("dicts", inputs_var1_dict, inputs_var2_dict)
    qfm_bound = bind(qfm, inputs_var1_dict)
    qfm_bound = bind(qfm_bound, inputs_var2_dict)

    job = backend.run(qiskit.compiler.transpile(qfm_bound, backend), shots=10000)
    probabilities = job.get_probabilities() 
    return probabilities

def get_quantum_parameters(no_vids, inputs_var1, inputs_var2):
    """ inputs_var1, inputs_var2: no_time_steps X no_videos """
    no_qubits = no_vids * len(inputs_var1[0])
    print(no_qubits, inputs_var1)
    probs = []
    opacities = []
    for t in range(len(inputs_var1)):
        probs.append(get_quantum_parameters_one_step(no_vids, inputs_var1[t], inputs_var2[t]))
    print("probs", probs)
    probs_post = [post_process(prob_dist, no_vids) for prob_dist in probs] 
    print("probs_post", probs_post)
    probs_post_post = [compute_scores(prob_post_dist) for prob_post_dist in probs_post]
    #probs_post_post = [{key:val/sum(prob_post_dist.values()) for key,val in prob_post_dist.items()} for prob_post_dist in probs_post]
    print("probs_post_post", probs_post_post)
    return probs_post_post

def post_process(dict, no_vids):
    out = {}
    for key, val in dict.items():
        my_list = list(range(len(key)))
        coupling = []
        for i in range(0, len(key), 2):
            x = i
            coupling.append((my_list[x:x+2]))
        target_key = [0]*no_vids
        for li_index, li in enumerate(coupling):
            relevant_indices = [int(i) for i in li]
            #print("li_index, li", li_index, li)
            #print(key[relevant_indices[0]:relevant_indices[-1]])
            if "1" in key[relevant_indices[0]:relevant_indices[-1]]:
                target_key[li_index] = 1
        target_key = ''.join([f"{target_key_item}" for target_key_item in target_key])
        if target_key not in out.keys():
            out[target_key] = val
        else:
            out[target_key] += val
    return out