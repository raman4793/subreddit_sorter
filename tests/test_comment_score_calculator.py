import unittest

import pandas

from exceptions.exceptions import InvalidArgumentValue
from score_calculator import get_comment_score_calculator, get_post_score_calculator, get_sub_score_calculator
from scraper import FileScrapper
from utils import model_to_data_frame


class TestCommentScoreCalculator(unittest.TestCase):
    def setUp(self):
        self.file_scraper = FileScrapper(cache_folder="cache")
        self.score_calculator = get_comment_score_calculator()

    def test_invalid_data(self):
        values = ["asdf", b"asdfasdf", 5, {"a": "asdf"}, [1, "asdf"]]
        for value in values:
            arguments = {"comments_data_frame": value}
            self.assertRaises(InvalidArgumentValue, self.score_calculator.score, **arguments)

    def test_invalid_data_frame(self):
        values = [{"ups": "abc"}]
        data_frame = model_to_data_frame(values)
        arguments = {"comments_data_frame": data_frame}
        self.assertRaises(InvalidArgumentValue, self.score_calculator.score, **arguments)

    def test_valid_data_frame(self):
        values = [
            {"ups": 10.0, "score": 0.47494783668349555},
            {"ups": 10.0, "score": 0.47494783668349555},
            {"ups": 10.0, "score": 0.47494783668349555},
            {"ups": 9.9, "score": 0.3618650184255208},
            {"ups": 8, "score": -1.7867085284760074}
        ]
        data_frame = model_to_data_frame(values)
        score = self.score_calculator.score(comments_data_frame=data_frame)
        pandas.testing.assert_frame_equal(left=model_to_data_frame(values), right=score)


class TestPostScoreCalculator(unittest.TestCase):
    def setUp(self):
        self.file_scraper = FileScrapper(cache_folder="cache")
        self.score_calculator = get_post_score_calculator()

    def test_invalid_data(self):
        values = ["asdf", b"asdfasdf", 5, {"a": "asdf"}, [1, "asdf"]]
        for value in values:
            arguments = {"comments_data_frame": value, "post": "abc"}
            self.assertRaises(InvalidArgumentValue, self.score_calculator.score, **arguments)

    def test_invalid_data_frame(self):
        values = [{"ups": "abc"}]
        data_frame = model_to_data_frame(values)
        arguments = {"comments_data_frame": data_frame, "post": "ac"}
        self.assertRaises(InvalidArgumentValue, self.score_calculator.score, **arguments)

    def test_valid_data_frame(self):
        comments = [
            {"ups": 10.0, "score": 0.47494783668349555},
            {"ups": 10.0, "score": 0.47494783668349555},
            {"ups": 10.0, "score": 0.47494783668349555},
            {"ups": 9.9, "score": 0.3618650184255208}
        ]
        data_frame = model_to_data_frame(comments)
        score = self.score_calculator.score(post={}, comments_data_frame=data_frame)
        self.assertDictEqual(score, {'score': 0.44667713211900184})


class TestSubredditScoreCalculator(unittest.TestCase):
    def setUp(self):
        self.file_scraper = FileScrapper(cache_folder="cache")
        self.score_calculator = get_sub_score_calculator()

    def test_invalid_data(self):
        values = ["asdf", b"asdfasdf", 5, {"a": "asdf"}, [1, "asdf"]]
        for value in values:
            arguments = {"posts_data_frame": value, "subreddit": "abc"}
            self.assertRaises(InvalidArgumentValue, self.score_calculator.score, **arguments)

    def test_invalid_data_frame(self):
        values = [{"ups": "abc"}]
        data_frame = model_to_data_frame(values)
        arguments = {"posts_data_frame": data_frame, "subreddit": "ac"}
        self.assertRaises(InvalidArgumentValue, self.score_calculator.score, **arguments)

    def test_valid_data_frame(self):
        subreddits = [
            {"ups": 10.0, "score": 0.47494783668349555},
            {"ups": 10.0, "score": 0.47494783668349555},
            {"ups": 10.0, "score": 0.47494783668349555},
            {"ups": 9.9, "score": 0.3618650184255208}
        ]
        data_frame = model_to_data_frame(subreddits)
        score = self.score_calculator.score(subreddit={}, posts_data_frame=data_frame)
        self.assertDictEqual(score, {'score': 0.44667713211900184})
