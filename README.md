# ALC Subsumption Algorithm

## Description
This project implements a subsumption algorithm for the ALC description logic. In description logics, a concept **C** subsumes a concept **D** if every model of **D** is also a model of **C**. The algorithm is applied to the classification of a set of concepts in the form of a taxonomy.

## Features
- Implementation of a subsumption algorithm for ALC
- Application to taxonomy-based concept classification

## Keywords
- Description Logics
- Subsumption
- Classification

## Project Structure
- **src/**: Contains the Python implementation of the algorithm.
- **tests/**: Sample test cases for verifying the implementation.

## Setup
### Prerequisites
- Python 3.x (no additional dependencies required)

### Installation
```bash
# Clone the repository
git clone https://github.com/lina-yasmine/ALC-Subsumption-Algorithm
cd ALC-Subsumption-Algorithm
```

## Usage
Run the script to test subsumption and classification:
```bash
python src/main.py
```

## Example
```python
from src.alc import TBox, ABox, Not, And, Or, Exists, ForAll

tbox = TBox()
tbox.add_relation("Animal", "Mammifère")
tbox.add_relation("Mammifère", "Humain")

abox = ABox()
abox.add_assertion("Pierre", "Humain")

print(abox.is_instance_of("Pierre", And("Animal", "Humain"), tbox))  # True
```

## References
Baader, F., Calvanese, D., McGuinness, D., Nardi, D., & Patel-Schneider, P. (2003). *The Description Logic Handbook: Theory, Implementation, and Applications*. Cambridge University Press.

## License
[MIT License]
