# An Uncertain Ethics Planner



Run tests with `run_tests.sh`. It run each algorithm on the TeacherBot domain 5 times and store results in csv files. You can configure the experiments from inside run_tests.sh. See our results in `Results/TestResults`.
We used Python 3.12.2, with numpy, Pandas to store results, and pygraphviz to draw state space graphs (disabled by default, the code should run without it). 
We hope to add more domains soon, as well as more moral theories

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


