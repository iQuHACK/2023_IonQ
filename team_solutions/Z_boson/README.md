# Z_boson
iQuHACK 2023 project for ionQ

https://firaollemu.github.io/index.html

This project uses quantum procedural generation (https://arxiv.org/pdf/2007.11510.pdf) to generate a sound library from a few basic, random tunes generated from a limited number of sound elements (located in the ./sound_elements directory).

The method is to construct an n_duration\*n_notes matrix for each sound element. Each column of the matrix corresponds to set frequencies (A3 to G4 in whole notes), and each row represents the notes being played simultaneously. One of the sound elements is transformed gradually to another using a partial swap operator, mixing the identity with the full swap operator.

The code to generate the sound matrices and convert them to audio files is in generate_sound_matrices.m. The analysis code, including the partial swap operators is in quantum_swap.py.

Data files resulting from the partial quantum swap are stored in the directory ./procedural_generation/.

## blur
We apply quantum blur effect to the 2D matrix representing the duration and pitch by applying $R_y$ to all qubits by a given angle $\theta = \pi / 10$. For input file 'sound_elements/csv/A.csv', the output file is 'sound_elements/csv/A_blur.csv'.
