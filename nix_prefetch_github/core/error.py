class AbortWithError(Exception):
    """This is exception should only be risen after the
    AbortWithErrorMessageEffect was triggered.  Also you should never
    catch this exception since its only purpose is for testing.
    """
