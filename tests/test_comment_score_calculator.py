import unittest

import pandas

from exceptions.exceptions import InvalidArgumentValue
from score_calculator import get_comment_score_calculator
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
            {"ups": 15.0, "score": -0.605920},
            {"ups": 10.0, "score": 0.572258},
            {"ups": 5.0, "score": 1.413813},
            {"ups": 3.0, "score": -1.110853},
            {"ups": 0.0, "score": -0.269298}
        ]
        data_frame = model_to_data_frame(values)
        score = self.score_calculator.score(comments_data_frame=data_frame)
        pandas.testing.assert_series_equal(left=data_frame["score"], right=score["score"])
