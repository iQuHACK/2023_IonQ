## Quantum Canvas

Quantum computing, a rapidly advancing technology, is likely to have a significant impact on the art industry. With their unique properties, quantum computers open up new possibilities for digital art, leading to advancements in animation, generative art, and interactive installations. As the technology continues to develop, we can expect to see quantum art become an increasingly important aspect of the art world. The goal of this project is to identify and visualize noise in quantum circuits in an artistic form.
Problem: In the field of quantum computing, the design and implementation of circuits that can effectively perform quantum operations is crucial for the development of quantum algorithms and the advancement of quantum technologies. However, one of the major challenges facing the development of quantum systems is the presence of noise in the circuits. Noise can manifest in various forms, such as thermal noise, crosstalk, or electromagnetic interference, and can greatly impact the performance and accuracy of quantum operations. By using various techniques, such as simulation, measurement, and visualization, we aim to capture and represent the sources and effects of noise in quantum circuits.
The project will involve the following steps:
Simulation and Measurement of noise in quantum circuits to identify its effects on circuit performance.
Visualization of the noise in an artistic form through the use of generative art.
Approach
We have conducted a thorough review of literature on image art generation and developed a novel concept for utilizing quantum noise in the creation of visually engaging artwork. Our approach is to quantify and utilize the unique noise present in quantum computing systems to generate new forms of digital art. We have examined various techniques for representing color in qubits and implemented various algorithms to achieve this goal.
Implementation
The goal of this project is to develop a comprehensive approach for identifying and visualizing noise in quantum circuits in an artistic form. In order to achieve this goal, the following implementation steps have been undertaken:
Develop a simulation of many noisy operations (50+/qubit) to explore the noise’s effects on the performance of quantum operations.
Apply a set of quantum gates to an initial state which encodes the binary representation of the hexadecimal color code for white (#FFFFFF) and measure the resulting state. The gates all return the qubit to its initial state, but because these operations are noisy some bits are flipped. 
Repeat this process to generate bands of color encodings which deviate further from the initial white as errors accumulate. Use the measurement results to determine the new colors of the visualization.
Use the measurement results to update the visualization and showcase the impact of noise on the quantum circuit.
Repeat the process for a set of gates and measurements with different amounts of noise.
This project is aimed at developing an approach that is based on a combination of simulation, measurement, and visualization techniques to capture and represent the sources and effects of noise in quantum circuits, and to communicate this understanding to a wider audience in an accessible and engaging manner. It will also provide a new perspective and medium to explore the complex and abstract nature of quantum mechanics, which can facilitate the public engagement and education in the field of quantum technology.
One challenge we encountered with this implementation on IonQ’s trapped ion computers is that their single-qubit gate fidelity is 99.96% as of March 2022. Available today on Microsoft Azure for public use on Aria, their highest qubit computer, has the following fidelity. 

When looking to accumulate error—in general, the opposite of what most users of quantum computing technology intend—we found IonQ’s computers to be too good. Because error accumulates In order to have precise control over the noise, therefore, we used Qiskit’s Aer Simulator. In this way, we were able to capture noise at a scale that is visible for us to observe with color differences.

Total number of shots used : 105
100 (random walk) + 5 (color generation) experiments with one shot 
Backends used :  Ionq, Qiskit Aer Simulation, IBM
Challenge Repository: https://github.com/iQuHACK/2023_IonQ
