# An Uncertain Ethics Planner

## Installation

You can calculate ethical policies yourself!

Our solution is tested with Python 3.12.2, using NumPy, Pandas and PyGraphViz (for visualisation, not required.)
You can install our packageswith pip using ```python3 -m pip install -r requirements.txt```.
You may want/need to create a virtual environment if Python is externally managed (for Ubuntu):
```
apt install python3-venv
python3 -m venv ~/UncertainEthicsPlannerEnv
source ~/UncertainEthicsPlannerEnv
pip3 install -r Uncertain-Ethics-Planner/requirements.txt
```
You can also install packages using [anaconda](https://docs.anaconda.com/free/miniconda/)

If you have Graphviz and [PyGraphviz](https://pygraphviz.github.io/) installed, you have the option of creating best partial solution graphs, explicit graphs, and complete state space graphs!

To use the planner, execute the module as a script with ```python3 -m EthicsPlanner```
This will run the autonomous tutor environment with paramaters that may be customised. Use `--help` for details!

You can run our experiments with the `run_tests.sh` script. 
It run each algorithm on the TeacherBot domain 5 times and store results in csv files. You can configure the experiments from inside run_tests.sh. See our results in `Results/TestResults`.

You can also run `pytest` to ensure all the plan configurations are working properly. 

We hope to add more domains soon, as well as more moral theories!
<!-- 
## Environment

An abstract world environment has been made as a template for the below concepts.

### MDP Class
* Environments are specified as a Markov Decision Process containing states, actions and a transition function.
* State objects are instantiated as the environment is explored, triggered by calling `mdp.getActionSuccessors(state, action)`.
* State successors and their probabilities are defined by appending rule methods to the list `mdp.rules`.
* Unlike the traditional MDP formalism, this class has no reward function.

#### Multi-Moral MDP

* Multi-Moral MDPs contain moral theories, `mm_mdp.Theories`. Each theory has a `tag` attribute. Judgments are sorted into lexicographic groups such that lower indexed theories are considered over any judgement from a greater indexed theory, no matter the extremity/probability of the judgement. This is defined as a list of list of tags in `mm_mdp.TheoryClasses`.

#### Moral mdps

* You can randomly generate abstract tree mdps with `AbstractGenerator.py` and store them in json.

### Moral Theories
Abstract moral theories contain most methods. For each environment, a concrete subclass must be made to apply the ethical concepts to the environment.

## Planner
Multi-moral MDPs (MMMDPs) with moral uncertainty are solved with hypothetical retrospection. 
Single-moral MDPs (SMMDPS) are solved with respect to just a single moral theory non-conflicting, with no moral uncertainty. This selection of the theory is made by the solver (passing a theory tag to its `solve` method) 
-->



