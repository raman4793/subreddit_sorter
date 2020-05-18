import luigi
from pymongo import UpdateOne

from configuration import Configuration
from score_calculator import get_post_score_calculator
from utils import model_to_data_frame
from .comments_score_calculator import CommentScore
from .. import mongo_client
from ..mongo_target import CustomMongoTarget


class PostScore(luigi.Task):
    job_id = luigi.IntParameter()
    top_n_comments = luigi.IntParameter(default=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_score_calculator = get_post_score_calculator()

    def requires(self):
        return [CommentScore(job_id=self.job_id)]

    def run(self):
        operations = []
        result = mongo_client["reddit_store"][Configuration.posts_collection_name].aggregate(self._get_posts_filter())
        for subreddit_posts in result:
            for post in subreddit_posts["entry"]:
                top_comments = CommentScore(self.job_id).output().get_collection().find(
                    {"parent_id": post["name"]}).sort(
                    [("score", -1)]).limit(self.top_n_comments)
                if top_comments.count() > 0:
                    top_comments = model_to_data_frame(top_comments)
                    post = self.post_score_calculator.score(post=post, comments_data_frame=top_comments)
                    if Configuration.ignore_negative_scores and post["score"] < 0:
                        continue
                    operation = UpdateOne({"name": post["name"]}, {'$set': {'score': post["score"]}})
                    operations.append(operation)
        operation_count = len(operations)
        self.output().bulk_operations(operations=operations)
        self.output().mark_done(job_id=self.job_id, operation_count=operation_count)

    def output(self):
        return CustomMongoTarget(mongo_client=mongo_client, index="reddit_store",
                                 collection=Configuration.posts_collection_name, task_name="score_posts")

    def _get_posts_filter(self):
        mongo_filter = [
            {
                "$group": {
                    "_id": "$subreddit",
                    "count": {"$sum": 1},
                    "entry": {
                        "$push": {
                            "name": "$name"
                        }
                    }
                }
            }
        ]
        if not Configuration.use_all:
            mongo_filter.insert(0, {"$match": {"job_id": self.job_id}})
        return mongo_filter
