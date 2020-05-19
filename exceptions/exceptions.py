class BaseRedditAnalyzerException(Exception):
    def __init__(self, *args, **kwargs):
        try:
            self.message = kwargs["message"]
        except KeyError as ke:
            Exception("Please provide the keyword argument ", str(ke))


class KeywordArgumentException(BaseRedditAnalyzerException):
    pass


class InvalidArgumentValue(BaseRedditAnalyzerException):
    pass


class InvalidConfigurationValue(BaseRedditAnalyzerException):
    pass
