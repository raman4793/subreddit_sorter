import flask
from flask import jsonify
from pymongo import MongoClient

app = flask.Flask(__name__)

mongo_client = MongoClient(host="localhost")


@app.route("/v1/subreddits")
def get():
    history_collection = mongo_client["reddit_store"]["history"]
    top_n_subreddits_from_past_two_runs = history_collection.aggregate([
        {"$sort": {"job_id": -1}},
        {"$group": {"_id": "$session_id", "count": {"$sum": 1},
                    "entry": {"$push": {"score": "$score", "subreddit": "$subreddit"}}}},
        {"$limit": 2}
    ])
    top_n_subreddits_from_past_two_runs = list(top_n_subreddits_from_past_two_runs)
    print(top_n_subreddits_from_past_two_runs)
    if len(top_n_subreddits_from_past_two_runs) == 2:
        latest_run = top_n_subreddits_from_past_two_runs[0]["entry"]
        last_run = top_n_subreddits_from_past_two_runs[1]["entry"]
        for latest_run_data in latest_run:
            previous_score = None
            for last_run_data in last_run:
                if latest_run_data["subreddit"] == last_run_data["subreddit"]:
                    previous_score = last_run_data["score"]
            if previous_score:
                latest_run_data["score_change"] = (latest_run_data["score"] - previous_score) / abs(previous_score)
            else:
                latest_run_data["score_change"] = None
        return jsonify(latest_run)
    return jsonify(top_n_subreddits_from_past_two_runs[0]["entry"])


if __name__ == '__main__':
    app.run(host="0.0.0.0")
