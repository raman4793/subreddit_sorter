import logging
import os
import unittest

from exceptions.exceptions import InvalidArgumentValue
from scraper import FileScrapper


class TestFileScraperGetSubreddit(unittest.TestCase):

    def setUp(self):
        logging.info(os.getcwd())
        self.file_scraper = FileScrapper(cache_folder="cache")
        self.logger = logging

    def test_invalid_limits(self):
        limit_values = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 101, 0]
        for limit_value in limit_values:
            arguments = {"limit": limit_value}
            with self.assertRaises(InvalidArgumentValue):
                subreddits = self.file_scraper.get_subreddits(**arguments)
                next(subreddits)

    def test_valid_limits(self):
        limit_values = range(1, 10)
        for limit_value in limit_values:
            arguments = {"limit": limit_value}
            subreddits = self.file_scraper.get_subreddits(**arguments)
            index = 0
            for _ in subreddits:
                index = index + 1
            logging.info(index)
            self.assertEqual(index, limit_value)


class TestFileScraperGetPost(unittest.TestCase):

    def setUp(self):
        logging.info(os.getcwd())
        self.file_scraper = FileScrapper(cache_folder="cache")
        self.logger = logging
        self.sub_reddit = {
            "subreddit": "PrequelMemes",
            "subreddit_name_prefixed": "r/PrequelMemes",
            "id": "giumpn",
            "ups": 16976,
            "name": "t3_giumpn",
            "score": 0.0,
            "downs": 0,
            "title": "The voice actor for Obi-wan in The Clone Wars wants a part in the upcoming Kenobi series. "
                     "R/prequelmemes, I think we all know what we need to do."
        }

    def test_invalid_limits(self):
        limit_values = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 101]
        for limit_value in limit_values:
            arguments = {"subreddit": self.sub_reddit, "limit": limit_value}
            with self.assertRaises(InvalidArgumentValue):
                posts = self.file_scraper._get_posts(**arguments)
                next(posts)

    def test_valid_limits(self):
        limit_values = range(1, 10)
        for limit_value in limit_values:
            arguments = {"subreddit": self.sub_reddit, "limit": limit_value}
            posts = self.file_scraper._get_posts(**arguments)
            index = 0
            for _ in posts:
                index = index + 1
            logging.info(index)
            self.assertEqual(limit_value, index)


class TestFileScraperGetComment(unittest.TestCase):

    def setUp(self):
        logging.info(os.getcwd())
        self.file_scraper = FileScrapper(cache_folder="cache")
        self.logger = logging
        self.post = {
            'ups': 2556, 'title': 'The Clone Wars : S7E12 - Discussion Thread', 'id': 'gbkvgn', 'score': 0.0,
            'permalink': '/r/PrequelMemes/comments/gbkvgn/the_clone_wars_s7e12_discussion_thread/',
            'subreddit': 'PrequelMemes', 'downs': 0, 'name': 't3_gbkvgn'
        }

    def test_invalid_limits(self):
        limit_values = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 101]
        for limit_value in limit_values:
            arguments = {"post": self.post, "limit": limit_value}
            with self.assertRaises(InvalidArgumentValue):
                comments = self.file_scraper._get_comments(**arguments)
                next(comments)

    def test_valid_limits(self):
        limit_values = range(1, 10)
        for limit_value in limit_values:
            arguments = {"post": self.post, "limit": limit_value}
            comments = self.file_scraper._get_comments(**arguments)
            index = 0
            for _ in comments:
                index = index + 1
            logging.info(index)
            self.assertEqual(limit_value, index)
