import abc


class BaseScraper(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_subreddits(self, *, limit=100):
        pass

    def get_posts(self, *, subreddits: list, limit=100):
        for subreddit in subreddits:
            yield self._get_posts(subreddit=subreddit)

    def get_comments(self, *, posts: list, limit=100):
        for post in posts:
            yield self._get_comments(post=post)

    @abc.abstractmethod
    def _get_posts(self, *, subreddit: dict, limit=100):
        pass

    @abc.abstractmethod
    def _get_comments(self, *, post: dict, limit=100):
        pass
