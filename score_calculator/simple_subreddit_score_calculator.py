import pandas as pd

from .base_calculator import BaseCalculator


class SimpleSubredditScoreCalculator(BaseCalculator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, *, subreddit, posts_data_frame: pd.DataFrame):
        subreddit["score"] = sum(posts_data_frame["score"] / posts_data_frame["score"].count())
        return subreddit
