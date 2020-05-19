import numpy
import pandas as pd

from exceptions.exceptions import InvalidArgumentValue
from .base_calculator import BaseCalculator


class SimpleSubredditScoreCalculator(BaseCalculator):
    """
    A subreddit score calculator implementation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, *, subreddit, posts_data_frame: pd.DataFrame):
        """
        Overriding score to calculate score of the subreddit dictionary passed in with the formula specified in the requirement doc
        :param subreddit: The subreddit dictionary whose score is to be calculated
        :param posts_data_frame: A data frame with the posts of that subreddit
        :return: subreddit: Subreddit dictionary after adding score
        """
        if type(subreddit) is not dict:
            raise InvalidArgumentValue("post should be a dictionary")
        if type(posts_data_frame) is not pd.DataFrame:
            raise InvalidArgumentValue("comments data frame needs a pandas data frame")
        if posts_data_frame.dtypes["ups"] != numpy.int:
            raise InvalidArgumentValue("comments data frame contains invalid data")
        subreddit["score"] = sum(posts_data_frame["score"] / posts_data_frame["score"].count())
        return subreddit
