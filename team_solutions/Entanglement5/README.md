# Game of Finches 

![logo](https://user-images.githubusercontent.com/79099250/215311239-4e778a72-0289-4562-b3a3-e8799e14ea8b.png)

![IonQ_corp_logo](https://user-images.githubusercontent.com/79099250/215311276-dd9675f7-77c7-424b-ad23-4d46bd819845.png)

Game of Finches is a package that uses the IonQ quantum computer to simulate the evolution process of Darwin's finches. Users can choose initial finches and natural selection parameters and watch as their finches evolve into unique specimens using superposition, entanglement, and dephasing as motors of evolution.

The finches are modeled as having 4 characteristics: color, wingspan, beak size, body size. All characteristics can have any value ranging from 0 to 1, given by the resulting probability distribution of the evolution algorithm. The evolution involves multiple finches on separate islands which can interact with each other. The evolution unfolds as follows:

1. Set initial characteristics of finches, interaction strengths, and natural selection pressure
2. Each evolutionary time-step is realised by averaging of 20-50 repeats of a quantum circuit (QC)
3. The output distribution of the QC, as well as natural selection pressure sets a new set initial
characteristics of finches
4. Repeat 2-3 for N generations

Each QC consists of 4 steps: 1) initialization, 2) intra-finch evolution, 3) inter-finch evolution, and 4) a second step of intra-finch evolution.

Initialization consists of single qubit rotations. For the first step, these are set by the user by choosing the initial finch characteristics. For subsequent steps, these rotations are set by a combination of the previous QC outcome distribution and natural selection pressure.

Intra-finch evolution correlates characteristics of a finch within individuals. For example, it might seem reasonable that the fatness of a finch is related to its wingspan or its beak size. We model these correlations as two controlled rotation gates that entangle the characteristic qubits with each other. The strength of the interaction is set buy the controlled rotation angle.

Inter-finch evolution models interactions between finches on different islands. The interaction is modeled as a partial swap given by an angle setting the amount of mixing between finches.

This evolution algorithm tries to model the dynamics of inter- and intra-population evolution while harnessing the full extent of the all-to-all connectivity of the IonQ platform.

We have run most simulations for 2 islands (1 finch per island) with 50 shots per QC. The imperfect gate fidelities are partially an advantage in this evolution algorithm, since it adds another layer of randomness, typical in evolution. 

More detailed explanation of the algorithm can be found in the pdf document iquhack_documentation.pdf.

To run the algorithm run this notebook: main.ipynb. You will be able to set initial finch characteristics, natural selection strength, and interaction rate between the finches and watch the finches evolve.
