from functools import wraps

from effect import Effect, sync_perform

from nix_prefetch_github import dispatcher


def performer_test(f):
    @wraps(f)
    def _wrapped(*args, **kwargs):
        generator = f(*args, **kwargs)
        intent = generator.send(None)
        while True:
            intent_result = sync_perform(dispatcher(), Effect(intent))
            try:
                intent = generator.send(intent_result)
            except StopIteration:
                return

    return _wrapped
