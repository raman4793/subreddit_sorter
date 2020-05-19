import prawcore

from .base_scraper import BaseScraper
from .models.comment_schema import CommentSchema
from .models.post_schema import PostSchema
from .models.subreddit_schema import SubredditSchema


class APIScrapper(BaseScraper):
    """
    Reddit API based scraper
    """

    def __init__(self, *args, **kwargs):
        """
        Reddit scraper initializer
        """
        super().__init__(*args, **kwargs)
        authenticator = prawcore.TrustedAuthenticator(
            prawcore.Requestor("prawcore_read_only_example"),
            'v-X_egMVLaarIQ',
            'jnMSspky0z0OSNJPm5Yq8Ah4SyU')
        self.authorizer = prawcore.ReadOnlyAuthorizer(authenticator)
        self.authorizer.refresh()

    def get_subreddits(self, *, limit=100):
        """
        Overridden get subreddits method inherted from BaseScraper that returns a generator that has validated
        subreddit dictionary
        :param limit: (int)
        :return: subreddit: (generator)
        """
        with prawcore.session(self.authorizer) as session:
            data = session.request("GET", "/best.json?limit={}".format(limit))
            for subreddit in data["data"]["children"]:
                yield SubredditSchema().load(data=subreddit["data"])

    def _get_posts(self, *, subreddit: dict, limit=50):
        """
        Overridden method from BaseScraper that yields posts for a single subreddit dictionary
        :param subreddit: (dict) subreddit dictionary
        :param limit: (int) number of posts to be retrieved
        :return: post: (generator)
        """
        assert type(subreddit) is dict
        try:
            with prawcore.session(self.authorizer) as session:
                data = session.request('GET', "{}.json?limit={}".format(subreddit["subreddit_name_prefixed"], limit))
                for post_data in data["data"]["children"]:
                    yield PostSchema().load(data=post_data["data"])
        except Exception:
            return None

    def _get_comments(self, *, post: dict, limit=25):
        """
        Overridden method from BaseScraper that yields comments for a single post dictionary
        :param post: (dict) post dictionary
        :param limit: (int) number of comments to be retrieved
        :return: comment: (generator)
        """
        assert type(post) is dict
        try:
            with prawcore.session(self.authorizer) as session:
                api_end_point = post["permalink"][:-1]
                data = session.request("GET", "{}?limit={}".format(api_end_point, limit))
                for comment_data in data[1]["data"]["children"]:
                    yield CommentSchema().load(data=comment_data["data"])
        except Exception:
            return None
