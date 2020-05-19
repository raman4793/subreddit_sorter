import json

from .base_scraper import BaseScraper
from .models.comment_schema import CommentSchema
from .models.post_schema import PostSchema
from .models.subreddit_schema import SubredditSchema


class FileScrapper(BaseScraper):
    """
    A file based scraper if passed a cache folder path would return json much like the reddit api
    """

    def __init__(self, *args, **kwargs):
        """
        File scraper initializer
        :param cache_folder: Folder location of the cache folder, default value is cache
        """
        super().__init__(*args, **kwargs)
        self.cache_folder = kwargs.get("cache_folder", "cache")

    def get_subreddits(self, *, limit=100):
        """
        Overridden get subreddits method inherted from BaseScraper that returns a generator that has validated
        subreddit dictionary
        :param limit: (int)
        :return: subreddit: (generator)
        """
        self.validate_limit(limit)
        data = json.load(open("{}/subreddit_list.json".format(self.cache_folder), "r"))
        for index, subreddit in enumerate(data["data"]["children"]):
            if index > limit - 1 or index >= 100:
                break
            yield SubredditSchema().loads(json_data=json.dumps(subreddit["data"]))

    def _get_posts(self, *, subreddit: dict, limit=100):
        """
        Overridden method from BaseScraper that yields posts for a single subreddit dictionary
        :param subreddit: (dict) subreddit dictionary
        :param limit: (int) number of posts to be retrieved
        :return: post: (generator)
        """
        self.validate_limit(limit)
        assert type(subreddit) is dict
        try:
            data = json.load(open("{}/posts/{}.json".format(self.cache_folder, subreddit["subreddit"]), "r"))
            for index, post_data in enumerate(data["data"]["children"]):
                if index > limit - 1 or index >= 100:
                    break
                yield PostSchema().loads(json_data=json.dumps(post_data["data"]))
        except Exception:
            return None

    def _get_comments(self, *, post: dict, limit=100):
        """
        Overridden method from BaseScraper that yields comments for a single post dictionary
        :param post: (dict) post dictionary
        :param limit: (int) number of comments to be retrieved
        :return: comment: (generator)
        """
        self.validate_limit(limit)
        assert type(post) is dict
        try:
            cache_file_name = post["permalink"].split("/")[-2]
            data = json.load(
                open("{}/comments/{}/{}.json".format(self.cache_folder, post["subreddit"], cache_file_name), "r"))
            for index, comment_data in enumerate(data[1]["data"]["children"]):
                if index > limit - 1 or index >= 100:
                    break
                yield CommentSchema().loads(json_data=json.dumps(comment_data["data"]))
        except Exception as ex:
            return None
