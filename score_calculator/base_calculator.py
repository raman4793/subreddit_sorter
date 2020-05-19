import abc


class BaseCalculator(abc.ABC):
    """
    A abstract base class for entity calculators
    """

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def score(self, *args, **kwargs):
        """
        A abstract method for calculating score of an entity
        :param args:
        :param kwargs:
        :return:
        """
        pass
