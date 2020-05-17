import luigi

from configuration import Configuration
from tasks.score_calculators.score_calculator import CalculateScore
from utils import timed


@timed
def pipeline():
    luigi.build([CalculateScore(top_n_subreddits=Configuration.subreddit_limit, top_n_posts=Configuration.posts_limit,
                                top_n_comments=Configuration.comments_limit)], local_scheduler=True, workers=5)
    # luigi.build([CalculateScore(job_id=1589708292)], local_scheduler=True, workers=5)


if __name__ == '__main__':
    pipeline()
