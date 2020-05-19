from time import time

from marshmallow import Schema, fields, EXCLUDE, post_load


class PostSchema(Schema):
    title = fields.String(required=True)
    id = fields.String(required=True)
    subreddit = fields.String(required=True)
    name = fields.String(required=True)
    permalink = fields.String(required=True)
    ups = fields.Integer(required=True)
    downs = fields.Integer(required=True)
    score = fields.Integer(required=False)

    @post_load
    def clean_data(self, data, **kwargs):
        if not data.get("_id"):
            data["_id"] = "{}_{}".format(time(), data["id"])
        data["score"] = 0.0
        return data

    class Meta:
        unknown = EXCLUDE
