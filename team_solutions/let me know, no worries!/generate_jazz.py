from qiskit import QuantumCircuit, transpile, Aer
from random import randint, choice
from playsound import write_to_midi, play_notes, note_to_midinum

def play_generated_jazz():
    # result from training 
    params = [ 1.26989403,  0.8250506,   3.42590964,  2.4286362,  -1.32838389,  0.26595026,
  0.70996409,  1.59659644,  2.4860706,   2.04324946, -1.14180479, -0.70298824,
  1.83775229,  1.06056913,  0.15040904, -1.70155108,  0.63410947,  1.27088469,
  1.71214402, -0.72978847, -3.45650959,  1.27046722,  2.31061793,  1.04965825,
 -0.21151845,  2.45022007,  0.13684193, -0.42038938,  1.32283486, -0.13419116,
  1.44006691,  0.0527144 ,  1.36095856,  2.7160314,  0.93421611,  2.22211404,
  1.3177774 ,  0.50607916,  1.69739666,  0.21238703,  1.44150715,  1.35911489,
 -1.1986866 , -0.60649805,  0.91066046]

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
    
play_generated_jazz()