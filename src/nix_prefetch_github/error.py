from attr import *
from effect import *


def revision_not_found_errormessage(owner, repo, revision):
    return "Revision {revision} not found for repository {owner}/{repo}".format(
        revision=revision, owner=owner, repo=repo
    )


@attrs
class AbortWithErrorMessage:
    message = attrib()


@sync_performer
def abort_with_error_message_performer(_, intent):
    print(intent.message)
    exit(1)
