import abc

import utils
from score_calculator.base_calculator import BaseCalculator
from scraper.base_scraper import BaseScraper


class BaseRunner(abc.ABC):

    def __init__(self, *, n_subreddit: int, n_posts: int, n_comments: int):
        self.n_subreddit = n_subreddit
        self.n_posts = n_posts
        self.n_comments = n_comments
        self.scrapper = None
        self.subreddit_score_calculator = None
        self.post_score_calculator = None
        self.comment_score_calculator = None

    def initialize_runner(self, *, scrapper: BaseScraper, subreddit_score_calculator: BaseCalculator,
                          post_score_calculator: BaseCalculator,
                          comment_score_calculator: BaseCalculator):
        self.scrapper = scrapper
        self.subreddit_score_calculator = subreddit_score_calculator
        self.post_score_calculator = post_score_calculator
        self.comment_score_calculator = comment_score_calculator

    def run(self):
        subreddits = self._get_subreddits_data_frame()
        for subreddit_index, subreddit in subreddits.iterrows():
            posts = self._get_posts_data_frame(subreddit=subreddit)
            if posts is None:
                break
            for post_index, post in posts.iterrows():
                comments = self._get_comments_data_frame(post)
                if comments is None:
                    break
                comments = self.comment_score_calculator.score(comments_data_frame=comments)
                updated_post = self.post_score_calculator.score(post=post, comments_data_frame=comments[0:self.n_comments])
                posts.at[post_index, "score"] = updated_post["score"]
            posts = posts.sort_values(by="score", ascending=False)
            updated_subreddit = self.subreddit_score_calculator.score(subreddit=subreddit, posts_data_frame=posts[0:self.n_posts])
            subreddits.at[subreddit_index, "score"] = updated_subreddit["score"]
            subreddits.sort_values(by="score", ascending=False)
        return subreddits

    def _get_subreddits_data_frame(self):
        return utils.model_to_data_frame(self.scrapper.get_subreddits())

    def _get_posts_data_frame(self, subreddit):
        posts = self.scrapper._get_posts(subreddit=subreddit.to_dict())
        return utils.model_to_data_frame(posts) if posts else None

    def _get_comments_data_frame(self, post):
        comments = self.scrapper._get_comments(post=post.to_dict())
        return utils.model_to_data_frame(comments) if comments else None
