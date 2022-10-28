This repository contains some of the content of my end-of-studies research project on consensus algorithms.

## Bibliographical Survey
biblio contains the bibliographical survey which is the basis of the project.

## Scripts
scripts contains scripts to compute the probabilities of evolution of the markov processes representing the sampling in avalanche-style consensus in the case of building a state-machine. These probabilities are used to know the probability ε that consensus is not reached in the avalanche version of the decentralized state machine. β = 1 in markov.py and β = 2 in markovBeta.py. At the moment, β > 2 not available, I have not found a way to compute probabilities for all β.

## References
- [Decentralized calculator](https://github.com/Nicolascrd/decentralized-calculator)
- [Distributed state-machine](https://github.com/Nicolascrd/distributed-state-machine)