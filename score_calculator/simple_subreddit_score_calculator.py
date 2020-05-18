import numpy
import pandas as pd

from exceptions.exceptions import InvalidArgumentValue
from .base_calculator import BaseCalculator


class SimpleSubredditScoreCalculator(BaseCalculator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, *, subreddit, posts_data_frame: pd.DataFrame):
        if type(subreddit) is not dict:
            raise InvalidArgumentValue("post should be a dictionary")
        if type(posts_data_frame) is not pd.DataFrame:
            raise InvalidArgumentValue("comments data frame needs a pandas data frame")
        if posts_data_frame.dtypes["ups"] != numpy.float:
            raise InvalidArgumentValue("comments data frame contains invalid data")
        subreddit["score"] = sum(posts_data_frame["score"] / posts_data_frame["score"].count())
        return subreddit
