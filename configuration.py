import os

from exceptions.exceptions import InvalidConfigurationValue


class Configuration:
    max_limit = int(os.environ.get("max_limit", 100))
    scraper_type = int(os.environ.get("scraper_type", 2))

    subreddit_limit = int(os.environ.get("subreddit_limit", 10))
    posts_limit = int(os.environ.get("posts_limit", 5))
    comments_limit = int(os.environ.get("comments_limit", 3))

    max_subreddit_limit = int(os.environ.get("max_subreddit_limit", 20))
    max_posts_limit = int(os.environ.get("max_posts_limit", 10))
    max_comments_limit = int(os.environ.get("max_comments_limit", 5))

    mongo_host = os.environ.get("mongo_host", "localhost")
    subreddits_collection_name = os.environ.get("subreddit_collection_name", "subreddits")
    posts_collection_name = os.environ.get("posts_collection_name", "posts")
    comments_collection_name = os.environ.get("comments_collection_name", "comments")
    history_collection_name = os.environ.get("history_collection_name", "history")

    pipeline_run_frequency_in_hours = int(os.environ.get("pipeline_run_frequency_in_hours", 1))

    use_all = bool(os.environ.get("use_all", 0))
    ignore_negative_scores = bool(os.environ.get("ignore_negative_scores", 1))

    def validate(self):
        self.validate_max_limit()

        self.validate_max_comments_limit()
        self.validate_max_posts_limit()
        self.validate_max_subreddit_limit()

        self.validate_comments_limit()
        self.validate_posts_limit()
        self.validate_subreddit_limit()

        self.validate_scraper_type()
        self.validate_mongo_host()

        self.validate_collection_names()

    def validate_subreddit_limit(self):
        if type(
                self.subreddit_limit) is not int or self.subreddit_limit > self.max_subreddit_limit or self.subreddit_limit <= 0:
            raise InvalidConfigurationValue("subreddit_limit has to smaller than max_subreddit_limit")

    def validate_posts_limit(self):
        if type(self.posts_limit) is not int or self.posts_limit > self.max_posts_limit or self.posts_limit <= 0:
            raise InvalidConfigurationValue("posts_limit has to smaller than max_posts_limit")

    def validate_comments_limit(self):
        if type(
                self.comments_limit) is not int or self.comments_limit > self.max_comments_limit or self.comments_limit <= 0:
            raise InvalidConfigurationValue("comments_limit has to smaller than max_comments_limit")

    def validate_max_subreddit_limit(self):
        if type(
                self.max_subreddit_limit) is not int or self.max_subreddit_limit <= 0 or \
                self.max_subreddit_limit > self.max_limit:
            raise InvalidConfigurationValue(
                "max_subreddit_limit has to be a positive integer smaller than max_limit value {}".format(
                    self.max_limit))

    def validate_max_posts_limit(self):
        if type(self.max_posts_limit) is not int or self.max_posts_limit <= 0 or self.max_posts_limit > self.max_limit:
            raise InvalidConfigurationValue(
                "max_posts_limit has to be a positive integer smaller than max_limit value {}".format(
                    self.max_limit))

    def validate_max_comments_limit(self):
        if type(
                self.max_comments_limit) is not int or self.max_comments_limit <= 0 or \
                self.max_comments_limit > self.max_limit:
            raise InvalidConfigurationValue(
                "max_comments_limit has to be a positive integer smaller than max_limit value {}".format(
                    self.max_limit))

    def validate_max_limit(self):
        if type(self.max_limit) is not int or self.max_limit <= 0:
            raise InvalidConfigurationValue(
                "max_comments_limit has to be a positive integer smaller than max_limit value {}".format(
                    self.max_limit))

    def validate_scraper_type(self):
        if type(self.scraper_type) is not int or self.scraper_type > 2 or self.scraper_type <= 0:
            raise InvalidConfigurationValue("scraper_type value can only be 1 or 2")

    def validate_mongo_host(self):
        import re
        if type(self.mongo_host) is not str or (not re.findall(
                r'\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
                self.mongo_host) and self.mongo_host != "localhost"):
            raise InvalidConfigurationValue("Invalid configuration value for mongo_host")

    def validate_collection_names(self):
        if type(self.subreddits_collection_name) is not str:
            raise InvalidConfigurationValue("subreddits_collection_name has to be a string")
        elif len(self.subreddits_collection_name.split(" ")) > 1:
            raise InvalidConfigurationValue("subreddits_collection_name have spaces")
        if type(self.posts_collection_name) is not str:
            raise InvalidConfigurationValue("posts_collection_name has to be a string")
        elif len(self.posts_collection_name.split(" ")) > 1:
            raise InvalidConfigurationValue("posts_collection_name have spaces")
        if type(self.comments_collection_name) is not str:
            raise InvalidConfigurationValue("comments_collection_name has to be a string")
        elif len(self.comments_collection_name.split(" ")) > 1:
            raise InvalidConfigurationValue("comments_collection_name have spaces")
        if type(self.history_collection_name) is not str:
            raise InvalidConfigurationValue("history_collection_name has to be a string")
        elif len(self.history_collection_name.split(" ")) > 1:
            raise InvalidConfigurationValue("history_collection_name have spaces")

    def validate_pipeline_run_frequency(self):
        if type(self.pipeline_run_frequency_in_hours) is not int or self.pipeline_run_frequency_in_hours <= 0:
            raise InvalidConfigurationValue("pipeline_run_frequency_in_hours can only be a positive integer")

    def validate_use_all(self):
        if type(self.use_all) is int:
            # if 0 > self.use_all > 1:
            if not (self.ignore_negative_scores == 0 or self.ignore_negative_scores == 1):
                raise InvalidConfigurationValue(
                    "use_all can only be boolean so either use True/False or 1/0")
        elif type(self.use_all) is not bool:
            raise InvalidConfigurationValue("use_all can only be boolean so either use True/False or 1/0")

    def validate_ignore_negative_scores(self):
        if type(self.ignore_negative_scores) is int:
            if not (self.ignore_negative_scores == 0 or self.ignore_negative_scores == 1):
                raise InvalidConfigurationValue(
                    "ignore_negative_scores can only be boolean so either use True/False or 1/0")
        elif type(self.ignore_negative_scores) is not bool:
            raise InvalidConfigurationValue(
                "ignore_negative_scores can only be boolean so either use True/False or 1/0")
