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
        self.validate_max_comments_limit()
        self.validate_max_posts_limit()
        self.validate_max_subreddit_limit()

        self.validate_comments_limit()
        self.validate_posts_limit()
        self.validate_subreddit_limit()

    def validate_subreddit_limit(self):
        if self.subreddit_limit > self.max_subreddit_limit:
            raise InvalidConfigurationValue("subreddit_limit has to smaller than max_subreddit_limit")

    def validate_posts_limit(self):
        if self.posts_limit > self.max_posts_limit:
            raise InvalidConfigurationValue("posts_limit has to smaller than max_posts_limit")

    def validate_comments_limit(self):
        if self.comments_limit > self.max_comments_limit:
            raise InvalidConfigurationValue("comments_limit has to smaller than max_comments_limit")

    def validate_max_subreddit_limit(self):
        if self.max_subreddit_limit <= 0 or self.max_subreddit_limit > self.max_limit:
            raise InvalidConfigurationValue(
                "max_subreddit_limit has to be a positive integer smaller than max_limit value {}".format(
                    self.max_limit))

    def validate_max_posts_limit(self):
        if self.max_posts_limit <= 0 or self.max_posts_limit > self.max_limit:
            raise InvalidConfigurationValue(
                "max_posts_limit has to be a positive integer smaller than max_limit value {}".format(
                    self.max_limit))

    def validate_max_comments_limit(self):
        if self.max_comments_limit <= 0 or self.max_comments_limit > self.max_limit:
            raise InvalidConfigurationValue(
                "max_comments_limit has to be a positive integer smaller than max_limit value {}".format(
                    self.max_limit))
