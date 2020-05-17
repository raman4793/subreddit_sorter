import luigi

from configuration import Configuration
from scraper import get_scraper
from utils import append_job_id_to_model
from .get_subreddits import GetSubs
from .. import mongo_client
from ..mongo_target import CustomMongoTarget


class GetPosts(luigi.Task):
    job_id = luigi.IntParameter()

    def requires(self):
        return [GetSubs(job_id=self.job_id)]

    def run(self):
        scrapper = get_scraper(scrapper_type=Configuration.scraper_type)
        subreddits = self._get_subreddits()
        for subreddit in subreddits:
            posts = scrapper._get_posts(subreddit=subreddit, limit=Configuration.max_posts_limit)
            posts = [post for post in posts]
            posts = append_job_id_to_model(models=posts, job_id=self.job_id)
            if posts:
                self.output().write(values=posts)
        self.output().mark_done(job_id=self.job_id)

    def output(self):
        return CustomMongoTarget(mongo_client, index="reddit_store",
                                 collection=Configuration.posts_collection_name, task_name="get_posts")

    def _get_subreddits(self):
        if Configuration.use_all:
            return GetSubs(self.job_id).output().all()
        else:
            return GetSubs(self.job_id).output().find({"job_id": self.job_id})
