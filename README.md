# Project-LEI

## Contributors

[Ângela Barros](https://github.com/angelabarros)

[Manuel Monteiro](https://github.com/mamonteiro-brg)


## Goal
This is a Project where we want to predict the safety of drug combinations.

## Datasets
In this project we will analyse the following datasets:

  - SIDER
  - OFFSIDES

## Development
To analyse SIDER we will use Deedpchem (https://deepchem.io/)

The Featurizations that will be used in the project:

### Graph Convolutions

 Molecule is represented by a neighbout list and a set of initial feature vectors , each corresponding to a single atom,. Feature vector summarizes the atom's local chemical environment,  including atom-types, hybridization types and valence structures.
 
### Weave

  With the same feature vectors for atoms as Graph convolutions featurizer, Weave featurizer elaborates the neighbour list as a matrix of pair feature vectors, each representing the connectivity and distance between a pair of atoms.


## Models
The first models used in the project will be
  - Multitask Network
  - Single Task
  - Graph convolution Model


## Resources
Sites:
  - https://deepchem.io/

  - http://moleculenet.ai/
  
  - http://data.bioontology.org/


## Notes
In order to match the side effects to the same categories we used an API in order to accomplish that: http://data.bioontology.org/
The first step in the processing phase was to map out the categories in order to use the OFFSIDES dataset in the same way that SIDER was used.
