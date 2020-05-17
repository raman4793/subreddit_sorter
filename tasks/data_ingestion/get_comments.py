import luigi

from configuration import Configuration
from scraper import get_scraper
from utils import append_job_id_to_model
from .get_posts import GetPosts
from .. import mongo_client
from ..mongo_target import CustomMongoTarget


class GetComments(luigi.Task):
    job_id = luigi.IntParameter()

    def requires(self):
        return [GetPosts(job_id=self.job_id)]

    def run(self):
        scrapper = get_scraper(scrapper_type=Configuration.scraper_type)
        posts = self._get_posts()
        for post in posts:
            comments = scrapper._get_comments(post=post, limit=Configuration.max_comments_limit)
            comments = [comment for comment in comments]
            comments = append_job_id_to_model(models=comments, job_id=self.job_id)
            if comments:
                self.output().write(values=comments)
        self.output().mark_done(job_id=self.job_id)

    def output(self):
        return CustomMongoTarget(mongo_client=mongo_client, index="reddit_store",
                                 collection=Configuration.comments_collection_name, task_name="get_comments")

    def _get_posts(self):
        if Configuration.use_all:
            return GetPosts(self.job_id).output().all()
        else:
            return GetPosts(self.job_id).output().find({"job_id": self.job_id})
