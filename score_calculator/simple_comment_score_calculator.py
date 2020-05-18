import numpy
import pandas as pd

from exceptions.exceptions import InvalidArgumentValue
from .base_calculator import BaseCalculator


class SimpleCommentScoreCalculator(BaseCalculator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, *, comments_data_frame: pd.DataFrame):
        if type(comments_data_frame) is not pd.DataFrame:
            raise InvalidArgumentValue("comments data frame needs a pandas data frame")
        if comments_data_frame.dtypes["ups"] != numpy.float:
            raise InvalidArgumentValue("comments data frame contains invalid data")
        comments_data_frame["score"] = (comments_data_frame["ups"] - comments_data_frame["ups"].mean()) / \
                                       comments_data_frame["ups"].std()
        comments_data_frame = comments_data_frame.sort_values(by=["score"], ascending=False)
        return comments_data_frame
