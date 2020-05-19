from time import time

from marshmallow import Schema, fields, EXCLUDE, post_load


class CommentSchema(Schema):
    id = fields.String(required=True)
    body = fields.String(required=True)
    parent_id = fields.String(required=True)
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
