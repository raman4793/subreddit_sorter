import pandas as pd

from .base_calculator import BaseCalculator


class SimplePostScoreCalculator(BaseCalculator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, *, post, comments_data_frame: pd.DataFrame):
        post["score"] = sum(comments_data_frame["score"] / comments_data_frame["score"].count())
        return post
