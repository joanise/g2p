"""
This file is for constants that can be initialized without any (expensive) dependencies.
"""
import os
from abc import ABC, abstractmethod

DISTANCE_METRICS = [
    "weighted_feature_edit_distance",
    "hamming_feature_edit_distance",
    "feature_edit_distance",
    "dolgo_prime_distance",
    "fast_levenshtein_distance",
    "levenshtein_distance",
]

LANGS_DIR = os.path.join(os.path.dirname(__file__), "mappings", "langs")
LANGS_FILE_NAME = "langs.json.gz"
NETWORK_FILE_NAME = "network.json.gz"


class BaseTransducer(ABC):
    """Base class to typecheck transducers without having to import them."""

    @abstractmethod
    def __call__(self, to_convert: str):
        pass


class BaseTransductionGraph(ABC):
    """Base class to typecheck transduction graphs without having to import them."""

    @property
    @abstractmethod
    def tiers(self):
        pass


class BaseTokenizer(ABC):
    """Base class to typecheck tokenizers without having to import them."""

    @abstractmethod
    def tokenize_text(self, text):
        pass
