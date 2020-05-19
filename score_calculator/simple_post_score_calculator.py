import numpy
import pandas as pd

from exceptions.exceptions import InvalidArgumentValue
from .base_calculator import BaseCalculator


class SimplePostScoreCalculator(BaseCalculator):
    """
    A point score calculator implementation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, *, post, comments_data_frame: pd.DataFrame):
        """
        Overriding score to calculate score of the subreddit dictionary passed in with the formula specified in the requirement doc
        :param post: The post dictionary whose score is to be calculated
        :param comments_data_frame: A data frame with the comment of that post
        :return: post: post dictionary after adding score
        """
        if type(post) is not dict:
            raise InvalidArgumentValue("post should be a dictionary")
        if type(comments_data_frame) is not pd.DataFrame:
            raise InvalidArgumentValue("comments data frame needs a pandas data frame")
        if comments_data_frame.dtypes["ups"] != numpy.int:
            raise InvalidArgumentValue("comments data frame contains invalid data")
        post["score"] = sum(comments_data_frame["score"] / comments_data_frame["score"].count())
        return post
