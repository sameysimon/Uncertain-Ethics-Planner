# Singleton Moral Markov Decision Process 
from Raspberry.Environment.GeneralMDP import MDP
from abc import ABC, abstractmethod 
from enum import Enum
import numpy as np

class SM_MDP(MDP, ABC):
    def __init__(self):
        super().__init__()
        self.Theory = None
