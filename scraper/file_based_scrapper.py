import json

from .base_scraper import BaseScraper
from .models.comment_schema import CommentSchema
from .models.post_schema import PostSchema
from .models.subreddit_schema import SubredditSchema


class FileScrapper(BaseScraper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_subreddits(self, *, limit=100):
        data = json.load(open("cache/subreddit_list.json", "r"))
        for index, subreddit in enumerate(data["data"]["children"]):
            if index > limit - 1 or index >= 100:
                break
            yield SubredditSchema().loads(json_data=json.dumps(subreddit["data"]))

    def _get_posts(self, *, subreddit: dict, limit=100):
        assert type(subreddit) is dict
        try:
            data = json.load(open("cache/posts/{}.json".format(subreddit["subreddit"]), "r"))
            for index, post_data in enumerate(data["data"]["children"]):
                if index > limit - 1 or index >= 100:
                    break
                yield PostSchema().loads(json_data=json.dumps(post_data["data"]))
        except Exception:
            return None

    def _get_comments(self, *, post: dict, limit=100):
        assert type(post) is dict
        try:
            cache_file_name = post["permalink"].split("/")[-2]
            data = json.load(open("cache/comments/{}/{}.json".format(post["subreddit"], cache_file_name), "r"))
            for index, comment_data in enumerate(data[1]["data"]["children"]):
                if index > limit - 1 or index >= 100:
                    break
                yield CommentSchema().loads(json_data=json.dumps(comment_data["data"]))
        except Exception as ex:
            return None
