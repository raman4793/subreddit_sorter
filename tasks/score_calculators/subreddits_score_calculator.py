import luigi
from pymongo import UpdateOne

from configuration import Configuration
from score_calculator import get_sub_score_calculator
from utils import model_to_data_frame
from .posts_score_calculator import PostScore
from .. import mongo_client
from ..mongo_target import CustomMongoTarget


class SubScore(luigi.Task):
    job_id = luigi.IntParameter()
    top_n_posts = luigi.IntParameter(default=10)
    top_n_comments = luigi.IntParameter(default=5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subreddit_score_calculator = get_sub_score_calculator()

    def requires(self):
        return [PostScore(job_id=self.job_id, top_n_comments=self.top_n_comments)]

    def run(self):
        operations = []
        subreddits = self._get_subreddits()
        for subreddit in subreddits:
            top_posts = PostScore(self.job_id).output().get_collection().find(
                {"subreddit": subreddit["subreddit"]}).sort(
                [("score", -1)]).limit(self.top_n_posts)
            if top_posts.count() > 0:
                top_posts = model_to_data_frame(models=top_posts)
                subreddit = self.subreddit_score_calculator.score(subreddit=subreddit, posts_data_frame=top_posts)
                if Configuration.ignore_negative_scores and subreddit["score"] < 0:
                    continue
                operation = UpdateOne({"name": subreddit["name"]}, {'$set': {'score': subreddit["score"]}})
                operations.append(operation)
        operation_count = len(operations)
        self.output().bulk_operations(operations=operations)
        self.output().mark_done(job_id=self.job_id, operation_count=operation_count)

    def output(self):
        return CustomMongoTarget(mongo_client, index="reddit_store",
                                 collection=Configuration.subreddits_collection_name, task_name="score_subs")

    def _get_subreddits(self):
        if Configuration.use_all:
            subreddits = mongo_client["reddit_store"][Configuration.subreddits_collection_name].find()
        else:
            subreddits = mongo_client["reddit_store"][Configuration.subreddits_collection_name].find(
                {"job_id": self.job_id})
        return subreddits
