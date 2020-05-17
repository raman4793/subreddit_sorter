import json

import prawcore

from .base_scraper import BaseScraper
from .models.comment_schema import CommentSchema
from .models.post_schema import PostSchema
from .models.subreddit_schema import SubredditSchema


class APIScrapper(BaseScraper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        authenticator = prawcore.TrustedAuthenticator(
            prawcore.Requestor("prawcore_read_only_example"),
            'v-X_egMVLaarIQ',
            'jnMSspky0z0OSNJPm5Yq8Ah4SyU')
        self.authorizer = prawcore.ReadOnlyAuthorizer(authenticator)
        self.authorizer.refresh()

    def get_subreddits(self, *, limit=100):
        with prawcore.session(self.authorizer) as session:
            data = session.request("GET", "/best.json?limit={}".format(limit))
            for subreddit in data["data"]["children"]:
                yield SubredditSchema().loads(json_data=json.dumps(subreddit["data"]))

    def _get_posts(self, *, subreddit: dict, limit=50):
        assert type(subreddit) is dict
        try:
            with prawcore.session(self.authorizer) as session:
                data = session.request('GET', "{}.json?limit={}".format(subreddit["subreddit_name_prefixed"], limit))
                for post_data in data["data"]["children"]:
                    yield PostSchema().loads(json_data=json.dumps(post_data["data"]))
        except Exception:
            return None

    def _get_comments(self, *, post: dict, limit=25):
        assert type(post) is dict
        try:
            with prawcore.session(self.authorizer) as session:
                api_end_point = post["permalink"][:-1]
                data = session.request("GET", "{}?limit={}".format(api_end_point, limit))
                for comment_data in data[1]["data"]["children"]:
                    yield CommentSchema().loads(json_data=json.dumps(comment_data["data"]))
        except Exception:
            return None
