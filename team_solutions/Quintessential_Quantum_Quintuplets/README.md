# Quantum Image Processing Visualization

Project for IQuHack 2023 IonQ Challenge at https://github.com/iQuHACK/2023_IonQ.

Image processing is in growing needs with the development of applications like facial recognition and autonomous vehicles. Due to the large volume and complexity of data, image processing is computationally expensive. More and more often, specialized hardwares such as GPUs are used to accelerate image processing. Quantum computing promises speed ups in a number of image processing algorithms, such as edge extraction [1]. 

We demonstrate Quantum Image Processing on the trapped ion quantum computers provided by IonQ. We first transform the image into a qubit representation named Flexible Representation of Quantum Images (FRQI). Next, we perform Quantum Fourier Transform on the input image as a demonstration of practical image processing on quantum computers. We visualize this process by repeatedly measuring the output qubits and feed the output into a fractal generation routine.

## Documentation

The link to our documentation and process can be found here: https://docs.google.com/document/d/1rIbXHpgPaqvQ9ja3OycBM_sBB9STySyqZ8Fe9A27SLs/edit

To generate the fractals, you can upload an image (preferably 8 x 8 or smaller) and then follow the steps in fractal_generation.ipynb. We support larger image sizes but are constrained by simulation speed/hardware limitations.

## Credit

Credit to https://www.linkedin.com/pulse/space-fractal-art-qiskit-wiktor-mazin-phd-mmt/ for fractal generation method.

