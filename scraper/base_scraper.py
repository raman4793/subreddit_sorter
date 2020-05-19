import abc

from configuration import Configuration
from exceptions.exceptions import InvalidArgumentValue


class BaseScraper(abc.ABC):
    """
    A base class for all scrapers
    """

    def __init__(self, *args, **kwargs):
        """
        Scraper initializer
        :param args:
        :param kwargs:
        """
        pass

    @abc.abstractmethod
    def get_subreddits(self, *, limit=100):
        """
        Abstract get subreddits method that returns a generator that has validated subreddit dictionary
        :param limit: (int)
        :return: subreddit: (generator)
        """
        pass

    def get_posts(self, *, subreddits: list, limit=100):
        """
        Takes a list of subreddits dictionary and yields posts for each subreddit
        :param subreddits: (list)
        :param limit: (int)
        :return: post: (generator)
        """
        for subreddit in subreddits:
            yield self._get_posts(subreddit=subreddit, limit=limit)

    def get_comments(self, *, posts: list, limit=100):
        """
        Takes a list of posts dictionary and yields comments for each post
        :param posts:
        :param limit:
        :return: comments: (generator)
        """
        for post in posts:
            yield self._get_comments(post=post, limit=limit)

    @abc.abstractmethod
    def _get_posts(self, *, subreddit: dict, limit=100):
        """
        Abstract method that yields posts for a single subreddit dictionary
        :param subreddit: (dict) subreddit dictionary
        :param limit: (int) number of posts to be retrieved
        :return: post: (generator)
        """
        pass

    @abc.abstractmethod
    def _get_comments(self, *, post: dict, limit=100):
        """
        Abstract method that yields comments for a single post dictionary
        :param post: (dict) post dictionary
        :param limit: (int) number of comments to be retrieved
        :return: comment: (generator)
        """
        pass

    @staticmethod
    def validate_limit(limit):
        """
        A static method to validate the limit values, raises InvalidArgumentValue in case limit is not a positive
        integer below Configuraiton.max_limit
        :param limit: (int)
        :return: None
        """
        if type(limit) is not int or limit <= 0 or limit > Configuration.max_limit:
            raise InvalidArgumentValue("Limit has to be a positive integer below {}".format(Configuration.max_limit))
