import datetime

import luigi
from luigi.contrib.simulate import RunAnywayTarget

from .get_comments import GetComments


class GetData(luigi.Task):
    job_id = luigi.IntParameter()

    def requires(self):
        return [GetComments(job_id=self.job_id)]

    def run(self):
        self.output().done()

    def output(self):
        return RunAnywayTarget(self)
