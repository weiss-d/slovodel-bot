"""
Generating words with Markov Chain and checking its existence in DB dictionary.
"""

import json

import redis
from rusyll import rusyll
import markovify

from enum import Enum
from typing import List, Any

wordTypes = Enum("wordTypes", "NOUN VERB ADJECTIVE")
