import os


class Configuration:
    scraper_type = int(os.environ.get("scraper_type", 2))

    subreddit_limit = int(os.environ.get("subreddit_limit", 10))
    posts_limit = int(os.environ.get("posts_limit", 5))
    comments_limit = int(os.environ.get("comments_limit", 3))

    max_subreddit_limit = int(os.environ.get("max_subreddit_limit", 20))
    max_posts_limit = int(os.environ.get("max_posts_limit", 10))
    max_comments_limit = int(os.environ.get("max_comments_limit", 5))

    mongo_host = os.environ.get("mongo_host", "localhost")
    subreddits_collection_name = os.environ.get("subreddit_collection_name", "subreddits")
    posts_collection_name = os.environ.get("posts_collection_name", "posts")
    comments_collection_name = os.environ.get("comments_collection_name", "comments")
    history_collection_name = os.environ.get("history_collection_name", "history")

    pipeline_run_frequency_in_hours = os.environ.get("pipeline_run_frequency_in_hours", 1)

    use_all = bool(os.environ.get("use_all", 0))
    ignore_negative_scores = bool(os.environ.get("ignore_negative_scores", 1))
