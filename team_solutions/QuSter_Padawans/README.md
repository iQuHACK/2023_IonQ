# Qwars Project

> A game based on the concept of Black Mirror: Bandersnatch to see if Grogu's warnings can save Mandalorian 

## Description

<p align="center">
  <img  src="https://github.com/galeinston/hello-word/blob/aca1472b90ff0c6d2c776d916e90b1ef96b7061e/Screenshot%202023-03-18%20at%204.11.14%20AM.png">
</p>

After parting with Mandalorian, Grogu is training under Luke. Right now, he can sense a number of features like size, speed and visibility of an object over a long distance. As his Jedi’s power growing, he can entangle his sense to the movement of his favorite knob, which is now always with Mandalorian. Mandalorian is unaware of an unknown enemy is approaching him with malevolence. Can Grogu save Mandalorian by warning him about the threat? 

Just like in Black Mirror: Bandersnatch movie, the user playing this game select features of the spaceship attacking Mando to test out different scenarios, among which would be the best solution to save Mandalorian.


## Quantum circuit


<p align="center">
  <img width="500" height="300" src="https://github.com/galeinston/hello-word/blob/2e18c8c1aca2af26f0dd27c5fa11d1d620c15ade/Screenshot%202023-03-18%20at%204.11.42%20AM.png">
</p>



Each feature of the spaceship that Grogu can sense is mapped into a quibt on a quantum register called 'greg'. Grogu's favorite knob can oscillate horizontally, vertically and rotate clockwise/counter clockwise. The knob's movements are mapped into qubits on 'knobreg,' another quantum register.

Grogu's Jedi power to sense and move the knob is represented as an entanglement between a qubit on 'greg' to another qubit on 'knobreg'. Because of the engtanglement, what happen to a qubit state on the 'greg' will instantenously change the state of a qubit on the 'knobreg'. Grogu's Jedi power, a.k.a the engtanglement in disguise, will make the knob:
- Vertically oscillate when the size of the enemy's spaceship is bigger than Mando's
- Horizontally oscillate when the speed of the enemy's spaceship is the speed of light
- Rotate the knob counter clockwise if the enemy's spaceship in invisible under a cloak shield

Mando taught Grogu about these movements when they traveling across the universe to find Jedi survivors. So he understand the signal if he sees the knob moves.

Whenever Grogu uses his Jedi's power, an X-gate is apply to a qubit on 'greg', which then reflected on the corresponding qubit on 'knobreg'

## Computation for the game
Javar Script was used to present the scenario to the users, offer options to play under ideal or noisy conditions, aks users to select features for the spaceship, animatedly reflect results of measurements warns Mando about the danger



