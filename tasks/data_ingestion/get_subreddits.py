import luigi

from configuration import Configuration
from scraper import get_scraper
from utils import append_job_id_to_model
from .. import mongo_client
from ..mongo_target import CustomMongoTarget


class GetSubs(luigi.Task):
    job_id = luigi.IntParameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        scrapper = get_scraper(scrapper_type=Configuration.scraper_type)
        subreddits = scrapper.get_subreddits(limit=Configuration.max_subreddit_limit)
        subreddits = [subreddit for subreddit in subreddits]
        subreddits = append_job_id_to_model(models=subreddits, job_id=self.job_id)
        if subreddits:
            self.output().write(values=subreddits)
        self.output().mark_done(job_id=self.job_id)

    def output(self):
        return CustomMongoTarget(mongo_client, index="reddit_store",
                                 collection=Configuration.subreddits_collection_name, task_name="get_subs")
