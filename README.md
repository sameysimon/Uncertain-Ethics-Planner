# An Uncertain Ethics Planner

## Environment

An abstract world environment has been made as a template for the below concepts.

### MDP Class
* Environments are specified as a Markov Decision Process containing states, actions and a transition function.
* State objects are instantiated as the enviroment is explored, triggered by calling `mdp.getActionSuccessors(state, action)`.
* State successors and their probabilties are defined by appending rule methods to the list `mdp.rules`.
* Unlike the traditional MDP formalism, this class has no reward function.

#### Singleton-Moral MDP

* A subclass of MDP, `SM_MDPs` contain a single moral theory, `sm_mpd.Theory`.
* Concrete in `AbstractSMMDP`.

#### Multi-Moral MDP

* Multi-Moral MDPs contain moral theories in a lexicographic order, `mm_mdp.Theories`. Judgements from lower indexed theories are considered over any judgement from a greater indexed theory, no matter the extremity/probability of the judgement.
* * Concrete in `AbstractMMMDP`.

#### Moral SSPs

* Moral SSPs contain moral theor(y/ies) plus a cost function with a discount. Defined in `MoralSSP.py`, they 

* You can randomly generate abstract tree SSPs with `AbstractGenerator.py` and store them in json.

### Moral Theories
Abstract moral theories contain most methods. For each environment, a concrete subclass is must be made to apply the ethical concepts to the environment.

## Planner

Currently:
* MMMDP hypothetical retrospection heursitic Find-and-Revise
* An exhaustive multi moral theory hypothetical retrospection. (compares every policy) (incomplete)
* Singleton moral theory Value Iteration (untested)



