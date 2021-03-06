import numpy
import pandas as pd

from exceptions.exceptions import InvalidArgumentValue
from .base_calculator import BaseCalculator


class SimpleCommentScoreCalculator(BaseCalculator):
    """
    A comment score calculator implementation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, *, comments_data_frame: pd.DataFrame):
        """
        Overriding score method to take a comments data frame mean normalizing ups to act as score
        :param comments_data_frame: A data frame of comments for which score is to be calculated
        :return: comment_data_frame: A data frame of comments which has the score calculated
        """
        if type(comments_data_frame) is not pd.DataFrame:
            raise InvalidArgumentValue("comments data frame needs a pandas data frame")
        if comments_data_frame.dtypes["ups"] != numpy.int:
            raise InvalidArgumentValue("comments data frame contains invalid data")
        comments_data_frame["score"] = (comments_data_frame["ups"] - comments_data_frame["ups"].mean()) / \
                                       comments_data_frame["ups"].std()
        comments_data_frame = comments_data_frame.sort_values(by=["score"], ascending=False)
        return comments_data_frame
