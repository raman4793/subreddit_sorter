from time import time

import luigi

from configuration import Configuration
from .subreddits_score_calculator import SubScore
from .. import mongo_client
from ..mongo_target import CustomMongoTarget


class CalculateScore(luigi.Task):
    job_id = luigi.IntParameter(default=int(time()))
    top_n_subreddits = luigi.IntParameter(default=50)
    top_n_posts = luigi.IntParameter(default=10)
    top_n_comments = luigi.IntParameter(default=5)

    def requires(self):
        return SubScore(job_id=self.job_id, top_n_posts=self.top_n_posts, top_n_comments=self.top_n_comments)

    def run(self):
        session_id = self.job_id
        top_subreddits = SubScore(job_id=self.job_id, top_n_posts=self.top_n_posts,
                                  top_n_comments=self.top_n_comments).output().get_collection().find().sort(
            [("score", -1)]).limit(self.top_n_subreddits)
        values = []
        for index, subreddit in enumerate(top_subreddits):
            subreddit["session_id"] = session_id
            subreddit["_id"] = "{}_{}".format(session_id, index)
            values.append(subreddit)
        self.output().write(values=values)
        self.output().mark_done(job_id=self.job_id)

    def output(self):
        return CustomMongoTarget(mongo_client=mongo_client, index="reddit_store",
                                 collection=Configuration.history_collection_name, task_name="pipeline")
