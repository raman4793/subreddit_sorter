import datetime

from luigi.contrib.mongodb import MongoTarget


class CustomMongoTarget(MongoTarget):

    def __init__(self, mongo_client, index, collection, task_name):
        super().__init__(mongo_client, index, collection)
        self.task_name = task_name

    def all(self):
        return self.get_collection().find()

    def find(self, mongo_filters):
        return self.get_collection().find(mongo_filters)

    def bulk_operations(self, operations: list):
        return self.get_collection().bulk_write(operations)

    def mark_done(self, *, job_id, operation_count=None):
        data = {"last_run_at": job_id, "_id": self.task_name}
        if operation_count:
            data["operation_count"] = operation_count
        self.get_index()["meta_store"].update({"_id": self.task_name}, {"$set": data}, upsert=True)

    def upsert(self, value, query):
        value = {"$set": value}
        return self.get_collection().update(query, value, upsert=True)

    def exists(self):
        expected_previous_run_date_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        expected_previous_run_time_stamp = datetime.datetime.timestamp(expected_previous_run_date_time)
        result = self.get_index()["meta_store"].find(
            {"last_run_at": {"$gt": expected_previous_run_time_stamp}, "_id": self.task_name})
        return result.count() > 0

    def write(self, values):
        self.get_collection().insert(values)
