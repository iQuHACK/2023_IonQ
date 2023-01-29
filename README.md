# Variations on a Theme of Qaganini

Ever wondered what “quantum music” sounds like? Come, take a listen to Qaganini, the world-renowned quantum composer (qomposer)! And if you like what you hear, you too can create your very own quantum sheet music!

## Functionalities

In our project, the quantum circuits are  musical “qomposers”.  Every time we run the qomposers on the simulator/qgpu, the output is converted into a sequence of musical notes.

There are two main ways to generate music:

- Auto mode: Qaganini will create a piece of quantum sheet music. You can request for Qaganini to play this piece of music multiple times. Due to the quantum nature of his music, each time he plays it, it will exhibit different variations!

- Manual mode: You can create your own quantum sheet music by composing different quantum gates together to form rich quantum circuits. Experiment to see what sort of music you can create, and listen to its multiple variations!

In the application window, you can click on the quantum gates in the top row to select them, and then select a row on the quantum circuit to place the gate down. For the two-qubit gates, you have to select the control row followed by the target row.

## Problem Statement

Our project seeks to make use of quantum randomness and entanglement in order to create pieces of music that sound different every time they are played. In order to do so, we need a method of extracting musical notes from a quantum circuit. We also want to devise a system such that each note depends on the previous notes, so that we do not just get random strings of notes.

## Big Picture Approach

Our main implementation consists of a Python class, `Composer`. The `Composer` class contains as one of its fields a list of Qiskit `QuantumCircuit`’s. Each circuit corresponds to 1 musical note. The main idea is to simulate each circuit on a set of input qubits and measure the circuit to obtain a string of bits. We then apply a mapping function that associates each possible bitstring with a note with a particular pitch and duration. The string of musical notes is then played out loud to the user.

Because quantum states can lie in superposition of the computational basis, the act of measurement collapses the qubits non-deterministically. This means that the string of musical notes derived on each playing can vary.

Furthermore, so that the string of musical notes are correlated, we form the inputs to each circuit in the following manner: The input to the first circuit (corresponding to the first note) is the all $$0$$’s state. The input to all subsequent circuits is then set to be the output of the previous circuit. So, for example, if the measurement of circuit 1 gives the bitstring $’0000001’$, the input to circuit 2 is set to be $|0000001\rangle$. This ensures that the quantum sheet music has musical coherence, rather than being a random sequence of notes.

## Implementation Details

### Graphical User Interface

The graphical user interface was implemented in `pygame`. Through the game engine, users are able to select from a collection of common gates (Pauli gates, Hadamard gates, CNOT, CZ, rotation gates) and place them on a quantum circuit. This circuit will be used to produce the first musical note of the tune. After they are done, the user can click the ‘New Note’  button. On the backend, this causes a new `QuantumCircuit` object to be created and placed at the end of the list. The GUI will refresh by removing all currently placed gates and displaying an empty quantum circuit. This repeats until the user decides to finish writing the sheet music. At that point, the user presses “Play music”, which will submit the jobs to the quantum hardware.

### Generating Music of a Given Genre

Download the GTZAN dataset from https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification.
