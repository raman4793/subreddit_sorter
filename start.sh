#!/usr/bin/env bash
set -e
python3 -m unittest tests.test_configuration
PYTHONPATH=$(pwd) luigi --module tasks.score_calculators.score_calculator RangeDaily --of CalculateScore --start 2020-01-01 --of-params '{"top_n_subreddits": "$subreddit_limit", "top_n_comments": "$comments_limit", "top_n_posts": "$posts_limit"}'
