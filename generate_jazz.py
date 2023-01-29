from qiskit import QuantumCircuit, transpile, Aer
from random import randint, choice
from playsound import write_to_midi, play_notes, note_to_midinum

def play_generated_jazz():
    # result from training 
    params = [0.37454012, 0.95071431, 0.73199394, 0.59865848, 0.15601864, 0.15599452,
    0.05808361, 0.86617615, 0.60111501, 0.70807258, 0.02058449, 0.96990985,
    0.83244264, 0.21233911, 0.18182497, 0.18340451, 0.30424224, 0.52475643,
    0.43194502, 0.29122914, 0.61185289, 0.13949386, 0.29214465, 0.36636184,
    0.45606998, 0.78517596, 0.19967378, 0.51423444, 0.59241457, 0.04645041]

    final_meas = []
    num_notes = 10

    for j in range(3):
        for i in range(num_notes):
            try:
                circui = QuantumCircuit(8, 8)
                notes_choice = ['C3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Bb3']
                print(choice(notes_choice), type(bin(note_to_midinum[choice(notes_choice)] - 48)))
                bits_arr = '100' + str(bin(note_to_midinum[choice(notes_choice)] - 48).replace('0b','') )
                print(bits_arr)
                init_state = bits_arr
                print('initial', init_state)
                circui.prepare_state(init_state, circui.qubits)
                # print('params first', type(params[0+3*i].numpy()))
                circui.rx(params[0+3*i]*3, 5) 
                circui.rx(params[1+3*i]*3, 6)
                circui.rx(params[2+3*i]*3, 7)

                circui.measure(range(8), range(8))

                backend = Aer.get_backend('aer_simulator')

                transpiled = transpile(circui, backend)

                job = backend.run(transpiled, shots=1)
                result = job.result()

                counts = result.get_counts()
                print('counts', counts)

                init_state = list(counts.keys())[list(counts.values()).index(1)]
                final_meas.append(init_state)
            except:
                print('f')
    print('final meas!!', final_meas)
    # circuit results -> midi

    play_notes(write_to_midi(final_meas))