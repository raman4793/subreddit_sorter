import abc

import pandas


class BaseCalculator(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    def score(self, *args, **kwargs):
        pass
