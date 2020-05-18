import numpy
import pandas as pd

from exceptions.exceptions import InvalidArgumentValue
from .base_calculator import BaseCalculator


class SimplePostScoreCalculator(BaseCalculator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, *, post, comments_data_frame: pd.DataFrame):
        if type(post) is not dict:
            raise InvalidArgumentValue("post should be a dictionary")
        if type(comments_data_frame) is not pd.DataFrame:
            raise InvalidArgumentValue("comments data frame needs a pandas data frame")
        if comments_data_frame.dtypes["ups"] != numpy.float:
            raise InvalidArgumentValue("comments data frame contains invalid data")
        post["score"] = sum(comments_data_frame["score"] / comments_data_frame["score"].count())
        return post
