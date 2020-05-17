import pandas as pd

from .base_calculator import BaseCalculator


class SimpleCommentScoreCalculator(BaseCalculator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, *, comments_data_frame: pd.DataFrame):
        comments_data_frame["score"] = (comments_data_frame["ups"] - comments_data_frame["ups"].mean()) / \
                                       comments_data_frame["ups"].std()
        comments_data_frame = comments_data_frame.sort_values(by=["score"], ascending=False)
        return comments_data_frame
