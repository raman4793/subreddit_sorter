import unittest

from configuration import Configuration
from exceptions.exceptions import InvalidConfigurationValue


class TestConfiguration(unittest.TestCase):

    def test_invalid_max_limits(self):
        limits = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0]
        for limit_value in limits:
            Configuration.max_limit = limit_value
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_max_limit)

    def test_invalid_subreddit_limits(self):
        Configuration.max_subreddit_limit = 10
        limits = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20]
        for limit_value in limits:
            Configuration.subreddit_limit = limit_value
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_subreddit_limit)

    def test_invalid_comment_limits(self):
        Configuration.max_comments_limit = 10
        limits = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20]
        for limit_value in limits:
            Configuration.comments_limit = limit_value
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_comments_limit)

    def test_invalid_post_limits(self):
        Configuration.max_posts_limit = 10
        limits = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20]
        for limit_value in limits:
            Configuration.posts_limit = limit_value
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_posts_limit)

    def test_invalid_max_subreddit_limits(self):
        Configuration.max_limit = 10
        limits = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20]
        for limit_value in limits:
            Configuration.max_subreddit_limit = limit_value
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_max_subreddit_limit)

    def test_invalid_max_comment_limits(self):
        Configuration.max_limit = 10
        limits = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20]
        for limit_value in limits:
            Configuration.max_comments_limit = limit_value
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_max_comments_limit)

    def test_invalid_max_post_limits(self):
        Configuration.max_limit = 10
        limits = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20]
        for limit_value in limits:
            Configuration.max_posts_limit = limit_value
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_max_posts_limit)

    def test_invalid_scraper_type(self):
        scraper_types = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20]
        for scraper_type in scraper_types:
            Configuration.scraper_type = scraper_type
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_scraper_type)

    def test_invalid_mongo_host(self):
        mongo_hosts = ["asdf", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20]
        for mongo_host in mongo_hosts:
            Configuration.mongo_host = mongo_host
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_mongo_host)

    def test_invalid_subreddits_collection_name(self):
        collection_names = [b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20, "test this"]
        for collection_name in collection_names:
            Configuration.subreddits_collection_name = collection_name
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_collection_names)

    def test_invalid_posts_collection_name(self):
        collection_names = [b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20, "test this"]
        for collection_name in collection_names:
            Configuration.posts_collection_name = collection_name
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_collection_names)

    def test_invalid_comments_collection_name(self):
        collection_names = [b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20, "test this"]
        for collection_name in collection_names:
            Configuration.comments_collection_name = collection_name
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_collection_names)

    def test_invalid_history_collection_name(self):
        collection_names = [b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 0, 20, "test this"]
        for collection_name in collection_names:
            Configuration.history_collection_name = collection_name
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_collection_names)

    def test_invalid_pipeline_run_frequency(self):
        run_frequencies = ["hello world", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1]
        for run_frequencie in run_frequencies:
            Configuration.pipeline_run_frequency_in_hours = run_frequencie
            self.assertRaises(InvalidConfigurationValue, Configuration().validate_pipeline_run_frequency)

    def test_invalid_use_all(self):
        use_all = ["hello world", b"asdfs", 0.56, ["ad", 45], {"a": "hello"}, -1, 3]
        for run_frequencie in use_all:
            Configuration.use_all = run_frequencie
            self.assertRaises(InvalidConfigurationValue, Configuration().validate)

    def test_valid_max_limits(self):
        limits = range(1, 100)
        for limit_value in limits:
            Configuration.max_limit = limit_value
            Configuration().validate_max_limit()

    def test_valid_subreddit_limits(self):
        limits = range(1, Configuration.max_subreddit_limit)
        for limit_value in limits:
            Configuration.subreddit_limit = limit_value
            Configuration().validate_subreddit_limit()

    def test_valid_comment_limits(self):
        Configuration.max_limit = 100
        Configuration.max_comments_limit = 10
        limits = range(1, Configuration.max_comments_limit)
        for limit_value in limits:
            Configuration.comments_limit = limit_value
            Configuration().validate_comments_limit()

    def test_valid_post_limits(self):
        Configuration.max_limit = 100
        Configuration.max_posts_limit = 10
        limits = range(1, Configuration.max_posts_limit)
        for limit_value in limits:
            Configuration.posts_limit = limit_value
            Configuration().validate_posts_limit()

    def test_valid_max_subreddit_limits(self):
        Configuration.max_limit = 10
        limits = range(1, Configuration.max_limit)
        for limit_value in limits:
            Configuration.max_subreddit_limit = limit_value
            Configuration().validate_max_subreddit_limit()

    def test_valid_max_comment_limits(self):
        Configuration.max_limit = 10
        limits = range(1, Configuration.max_limit)
        for limit_value in limits:
            Configuration.max_comments_limit = limit_value
            Configuration().validate_max_comments_limit()

    def test_valid_max_post_limits(self):
        Configuration.max_limit = 10
        limits = range(1, Configuration.max_limit)
        for limit_value in limits:
            Configuration.max_posts_limit = limit_value
            Configuration().validate_max_posts_limit()

    def test_valid_scraper_type(self):
        scraper_types = [1, 2]
        for scraper_type in scraper_types:
            Configuration.scraper_type = scraper_type
            Configuration().validate_scraper_type()

    def test_valid_mongo_host(self):
        mongo_hosts = ["192.168.1.5", "localhost"]
        for mongo_host in mongo_hosts:
            Configuration.mongo_host = mongo_host
            Configuration().validate_mongo_host()

    def test_valid_collection_name(self):
        collection_names = ["abc", "subredits"]
        for collection_name in collection_names:
            Configuration.subreddits_collection_name = collection_name
            Configuration.comments_collection_name = collection_name
            Configuration.posts_collection_name = collection_name
            Configuration.history_collection_name = collection_name
            Configuration().validate_collection_names()

    def test_valid_pipeline_run_frequency(self):
        run_frequencies = range(1, 24)
        for run_frequencie in run_frequencies:
            Configuration.pipeline_run_frequency_in_hours = run_frequencie
            Configuration().validate_pipeline_run_frequency()

    def test_valid_use_all(self):
        run_frequencies = [0, 1, False, True]
        for run_frequencie in run_frequencies:
            Configuration.pipeline_run_frequency_in_hours = run_frequencie
            Configuration().validate_use_all()

    def test_valid_ignore_negative_scores(self):
        run_frequencies = [False, True, 0, 1]
        for run_frequency in run_frequencies:
            Configuration.ignore_negative_scores = run_frequency
            Configuration().validate_ignore_negative_scores()
