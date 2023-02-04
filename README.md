# IonQ iQuHACK 2023 In-Person Challenge 
1st Place IonQ Challenge, [MIT iQuHACK 2023](https://www.iquise.mit.edu/iQuHACK/2023-01-27)

Team: Entanglement5

Members: Pieter-Jan Stas, Zixiao Xu, Aniruddha Sen, Sophie Li, Sasha Geim
# Game of Finches 

![logo](https://user-images.githubusercontent.com/87408590/215841612-e995b442-ef59-4a7c-abf5-6ec0005ddee8.png)


![IonQ_corp_logo](https://user-images.githubusercontent.com/79099250/215311276-dd9675f7-77c7-424b-ad23-4d46bd819845.png)

Game of Finches is a package that uses the IonQ quantum computer to simulate the evolution process of Darwin's finches. Users can choose initial finches and natural selection parameters and watch as their finches evolve into unique specimens using superposition, entanglement, and dephasing as motors of evolution.

The finches are modeled as having 4 characteristics: color, wingspan, beak size, body size. All characteristics can have any value ranging from 0 to 1, given by the resulting probability distribution of the evolution algorithm. The evolution involves multiple finches on separate islands which can interact with each other. The evolution unfolds as follows:

1. Set initial characteristics of finches, interaction strengths, and natural selection pressure
2. Each evolutionary time-step is realised by averaging of 20-50 repeats of a quantum circuit (QC)
3. The output distribution of the QC, as well as natural selection pressure sets a new set initial
characteristics of finches
4. Repeat 2-3 for N generations

Each QC consists of 4 steps: 1) initialization, 2) intra-finch evolution, 3) inter-finch evolution, and 4) a second step of intra-finch evolution.
<img width="853" alt="circuit" src="https://user-images.githubusercontent.com/87408590/215841260-57071ed3-1fd1-4b58-823e-625e60aa2865.png">

Initialization consists of single qubit rotations. For the first step, these are set by the user by choosing the initial finch characteristics. For subsequent steps, these rotations are set by a combination of the previous QC outcome distribution and natural selection pressure.

Intra-finch evolution correlates characteristics of a finch within individuals. For example, it might seem reasonable that the fatness of a finch is related to its wingspan or its beak size. We model these correlations as two controlled rotation gates that entangle the characteristic qubits with each other. The strength of the interaction is set buy the controlled rotation angle.

Inter-finch evolution models interactions between finches on different islands. The interaction is modeled as a partial swap given by an angle setting the amount of mixing between finches.

This evolution algorithm tries to model the dynamics of inter- and intra-population evolution while harnessing the full extent of the all-to-all connectivity of the IonQ platform.

We have run most simulations for 2 islands (1 finch per island) with 50 shots per QC. The imperfect gate fidelities are partially an advantage in this evolution algorithm, since it adds another layer of randomness, typical in evolution.

Below is an example of a 2-finch evolution run on the IonQ Harmony QPU, with the two finches starting with the same characteristics.

<img width="880" alt="Screenshot 2023-01-29 at 03 08 37" src="https://user-images.githubusercontent.com/79099250/215851614-070be3ae-718b-4da1-b854-836d0ea919d2.png">

More detailed explanation of the algorithm can be found in the pdf document: team_solutions/Entanglement5/iquhack_documentation.pdf.

To run the algorithm yourself, run this notebook: team_solutions/Entanglement5/main.ipynb. You will be able to set initial finch characteristics, natural selection strength, and interaction rate between the finches and watch the finches evolve.

team_solutions/Entanglement5/finch_functions.py contains the functions building and running the quantum circuits. 
team_solutions/Entanglement5/visualization.py contains the functions creating images and visualizing the finches.
