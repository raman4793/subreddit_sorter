
# Trending Subreddit Finder

### Build
```sh
$ docker-compose build
```

or alternatively

```sh
$ docker-compose pull
```

### Run
```sh
$ docker-compose up -d
```
##### Click [localhost:5000/v1/subreddits](http://localhost:5000/v1/subreddits) to see the result of the run
##### Click [localhost](http://localhost) to see the dashboard

### Test
```sh
$ bash test.sh
```
### To generate docs
```sh
$ cd docs
$ sphinx-apidoc -o rst ..
$ make html
```
# Configuration
### max_limit 
Max limit is the maximum limit that can be passed to the scraper, reddit apis seems to have 100 as their max limit in one api call.
```default: 100```
### scraper_type
Sets the scraper to be used for data ingestion.
Set as 1 for file based scraper
Set as 2 for api based scraper
```default: 2```
### subreddit_limit
This sets the top n subreddits to be selected after the score calculation is done. (TODO: refactor this to mirror task arguments)
```default: 10```
### posts_limit
This sets the top n posts to be selected for subreddit score calculation. (TODO: refactor this to mirror task arguments)
```default: 5```
### comments_limit
This sets the top n comments to be selected for post score calculation. (TODO: refactor this to mirror task arguments)
```default: 3```
### max_subreddit_limit
This sets the limit variable for the get subreddit method. (NOTE: This value cannot be more than **max_limit**)
```default: 20```
### max_posts_limit
This sets the limit variable for the get posts method. (NOTE: This value cannot be more than **max_limit**)
```default: 10```
### max_comments_limit
This sets the limit variable for the get comments method. (NOTE: This value cannot be more than **max_limit**)
```default: 5```
### mongo_host = os.environ.get("mongo_host", "localhost")  
This sets the host of the mongo db instance for data dumps.
```default: localhost```
### subreddits_collection_name
This sets the name of the collection for the subreddit data to be dumped(NOTE: has to be a valid identifier)
```default: subreddits```
### posts_collection_name
This sets the name of the collection for the post data to be dumped(NOTE: has to be a valid identifier)
```default: posts```
### comments_collection_name
This sets the name of the collection for the comment data to be dumped(NOTE: has to be a valid identifier)
```default: comments```
### history_collection_name
This sets the name of the collection for the top n subreddit data to be dumped(NOTE: has to be a valid identifier)
```default: history```
### pipeline_run_frequency_in_hours
This sets the frequency at which the pipeline has to be run in hours.
```default: 1```
### use_all = bool(os.environ.get("use_all", 0))  
The mongodb will have data from multiple runs, this variable can be set to get data from all executions of the pipeline or just the data ingested in the current run.
```default: 0```
### ignore_negative_scores = bool(os.environ.get("ignore_negative_scores", 1))
When working with massive amounts of data updating score after calculation can be a lengthy process, so this variable can be set to ignore any update operation if the score is negative.
```default: 1```
# Tasks
### GetData
```input: job_id```
This is a wrapper task that abstracts the other data ingestion tasks
```Depends on GetComments```
### GetSubreddits
```input: job_id```
This task is responsible for getting all the validated subreddit dictionary from api or file scraper and dumping it into subreddits collection in mongdb
### GetPosts
```input: job_id```
Once the GetSubreddits is completed this task gets the list of all subreddits and gets posts for each subreddit and dumps it into posts collection
```Depends on GetSubreddits```
### GetComments
```input: job_id```
Once the GetPosts is completed this task gets the list of all posts and gets comments for each post and dumps it into comments collection.
```Depends on GetPosts```
### CommentScore
```input: job_id```
Once the GetComments is completed this task groups all comments based on parent_id and a data frame object is created and the comment score calculator object is called to calculate score. The scores are then updated to the comments collection in the mongodb.
```Depends on GetComments```
### PostScore
```input: job_id, top_n_comments(select top n comments to calculate post score)```
Once the CommentScore is completed this task groups all posts based on their subreddit and iterate over each group and gets the comments score to calculate the post score, then the post score are updated to the posts collection.
```Depends on CommentScore```
### SubredditScore
```
job_id,
top_n_comments(select top n comments to calculate post score)
top_n_posts(select top n posts to calculate subreddit score)
```
Once the PostScore is completed this task groups iterates over all subreddits then gets posts of each subreddit and calculates subreddit score. Finally the scores are updated back to subreddits collection.
```Depends on PostScore```
### CalculateScore
```
job_id,
top_n_comments(select top n comments to calculate post score)
top_n_posts(select top n posts to calculate subreddit score)
top_n_subreddits(select top n subreddits)
```
This is the entry point of the pipeline, once the pipeline is complete this task takes top n subreddits from subreddit collection and inserts it into another collection to drive an api.
```Depends on SubredditScore```
# Components

### Scrapers

Scrapers are objects that brings the data into the pipeline, we have 2 types of scraper.

* File based scraper that uses a special folder as input which has json files for subreddit list, and posts for each subreddit and comments for each posts in a special folder structure
* API based scraper uses the reddit API to get data. The json files for the file based scraper was created by dumping API responses to json files.

The file based scraper was developed to accelerate testing as it was seen that APIs took close to 3 hours and 30 mins to ingest 100 subreddits, 50 posts for  each subreddit and 50 comments for each posts.

##### Subreddit Schema
```json
{
    "_id" : "1589862837.9016228_gm0bz9",
    "ups" : 51797,
    "title" : "What is the worst thing you have done because you got confused between items in different hands?",
    "subreddit_name_prefixed" : "r/AskReddit",
    "score" : 0.0,
    "downs" : 0,
    "subreddit" : "AskReddit",
    "id" : "gm0bz9",
    "name" : "t3_gm0bz9",
    "job_id" : 1589862834
}
```

* \_id is generated by {time_stamp}_{id}
* ups is the up vote count
* title is the title pinned post of the subreddit
* subreddit_name_prefixed is the endpoint on which posts can be queried
* score is by default set at 0.0.
* downs is the down vote count
* subreddit is the name of the subreddit
* id is the id recieved from the api
* name is a combination of entity type and entity id
* job_id is attached to the schema that is the timestamp at which the pipeline was started

##### Post Schema
```json
{
    "_id" : "1589862840.510622_gm0bz9",
    "ups" : 51817,
    "title" : "What is the worst thing you have done because you got confused between items in different hands?",
    "score" : 0.648524499847494,
    "downs" : 0,
    "permalink" : "/r/AskReddit/comments/gm0bz9/what_is_the_worst_thing_you_have_done_because_you/",
    "subreddit" : "AskReddit",
    "id" : "gm0bz9",
    "name" : "t3_gm0bz9",
    "job_id" : 1589862834
}
```

* \_id is generated by {time_stamp}_{id}
* ups is the up vote count
* title is the title of the post
* permalink is the endpoint on which comments can be queried
* score is by default set at 0.0.
* downs is the down vote count
* subreddit is the name of the subreddit
* id is the id recieved from the api
* name is a combination of entity type and entity id
* job_id is attached to the schema that is the timestamp at which the pipeline was started

##### Comment Schema
```json
{
    "_id" : "1589862871.0522447_fr14kfn",
    "ups" : 4597,
    "parent_id" : "t3_gm0bz9",
    "body" : "I went to go and put a scoop of catfood in the washing machine drawer once.",
    "score" : 0.0,
    "downs" : 0,
    "id" : "fr14kfn",
    "job_id" : 1589862834
}
```

* \_id is generated by {time_stamp}_{id}
* ups is the up vote count
* parent_id is the id of the post it belongs to
* body is the content of the comment
* score is by default set at 0.0.
* downs is the down vote count
* id is the id recieved from the api
* job_id is attached to the schema that is the timestamp at which the pipeline was started
### Score Calculators

##### Comment Score Calculator

Comment Score calculator takes in a pandas data frame with data validated by the comment schema
and comment score is calculated as
```
comments_data_frame["score"] = (comments_data_frame["ups"] - comments_data_frame["ups"].mean()) / \  
                               comments_data_frame["ups"].std()
```
This gives a mean normalised score for the comments.
The return of the  comment score calculator is a score sorted data frame
##### Post Score Calculator
Post Score Calculator takes in post dictionary validated by post schema and comments data frame that holds all the comments for that particular post.
The score is then calculated as 
```
post["score"] = sum(comments_data_frame["score"] / comments_data_frame["score"].count())
```
The post dictionary is then returned
##### Subreddit Score Calculator
Subreddit Score Calculator takes in subreddit dictionary validated by subreddit schema and posts data frame that holds all the posts for that subreddit.
Then the score is calculated as 
```
subreddit["score"] = sum(posts_data_frame["score"] / posts_data_frame["score"].count())
```
The subreddit dictionary is then returned.