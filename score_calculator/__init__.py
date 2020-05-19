from collections import namedtuple

from .simple_post_score_calculator import SimplePostScoreCalculator
from .simple_comment_score_calculator import SimpleCommentScoreCalculator
from .simple_subreddit_score_calculator import SimpleSubredditScoreCalculator


def get_calculators():
    calculator = namedtuple('calculator', 'subreddit_point_calculator post_point_calculator comment_point_calculator')
    return calculator(SimpleSubredditScoreCalculator(),
                      SimplePostScoreCalculator(),
                      SimpleCommentScoreCalculator())


def get_comment_score_calculator(*args, **kwargs):
    return SimpleCommentScoreCalculator(*args, **kwargs)


def get_post_score_calculator(*args, **kwargs):
    return SimplePostScoreCalculator(*args, **kwargs)


def get_sub_score_calculator(*args, **kwargs):
    return SimpleSubredditScoreCalculator(*args, **kwargs)
