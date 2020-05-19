#!/usr/bin/env bash
set -e
python3 -m unittest tests.test_configuration
PYTHONPATH=$(pwd) luigi --module tasks.score_calculators.score_calculator CalculateScore --top-n-subreddits $subreddit_limit --top-n-posts $posts_limit --top-n-comments $comments_limit --local-scheduler
