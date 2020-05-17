import luigi
from pymongo import UpdateOne

from configuration import Configuration
from score_calculator import get_comment_score_calculator
from tasks import mongo_client
from tasks.mongo_target import CustomMongoTarget
from utils import model_to_data_frame
from ..data_ingestion.get_data import GetData


class CommentScore(luigi.Task):
    job_id = luigi.IntParameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comment_score_calculator = get_comment_score_calculator()

    def requires(self):
        return [GetData(job_id=self.job_id)]

    def run(self):
        operations = []
        comment_filter = self._get_comment_filter()
        result = mongo_client["reddit_store"][Configuration.comments_collection_name].aggregate(
            comment_filter)
        for index, post_comments in enumerate(result):
            comments_data_frame = model_to_data_frame(models=post_comments["entry"])
            comments_data_frame = self.comment_score_calculator.score(comments_data_frame=comments_data_frame)
            for _, comment_data_frame in comments_data_frame.iterrows():
                if Configuration.ignore_negative_scores and comment_data_frame.score < 0:
                    continue
                operation = UpdateOne({"id": comment_data_frame.id}, {'$set': {'score': comment_data_frame.score}})
                operations.append(operation)
        operation_count = len(operations)
        self.output().bulk_operations(operations)
        self.output().mark_done(job_id=self.job_id, operation_count=operation_count)

    def output(self):
        return CustomMongoTarget(mongo_client=mongo_client, index="reddit_store",
                                 collection=Configuration.comments_collection_name, task_name="score_comments")

    def _get_comment_filter(self):
        mongo_filter = [
            {
                "$group": {
                    "_id": "$parent_id",
                    "count": {"$sum": 1},
                    "entry": {
                        "$push": {
                            "ups": "$ups",
                            "id": "$id",
                            "job_id": "$job_id"
                        }
                    }
                }
            }
        ]
        if not Configuration.use_all:
            mongo_filter.insert(0, {"$match": {"job_id": self.job_id}})
        return mongo_filter
