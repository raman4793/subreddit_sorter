import time
from functools import wraps

import pandas as pd


def model_to_data_frame(models: list):
    if type(models) is list:
        model_data_frame = pd.DataFrame(columns=models[0].keys(), data=models)
    else:
        try:
            records = [model for model in models]
            model_data_frame = None
            if records:
                model_data_frame = pd.DataFrame(columns=records[0].keys(), data=records)
        except Exception:
            raise ValueError("Please pass generator or a list")
    return model_data_frame


def timed(func):
    @wraps(func)
    def timed_function(*args, **kwargs):
        start_time = time.time()
        return_value = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print("{} took {} seconds".format(func.__name__, elapsed_time))
        return return_value

    return timed_function


def append_job_id_to_model(models, job_id):
    def append_job_id(model):
        model["job_id"] = job_id
        return model

    models = list(map(append_job_id, models))
    return models
