"""This module contains data structures that describe all the side
effects that the core module expects to be performed
"""

from attr import attrib, attrs


@attrs
class CheckGitRepoIsDirty:
    directory = attrib()


@attrs
class ShowWarning:
    message = attrib()


@attrs
class DetectGithubRepository:
    directory = attrib()
    remote = attrib()


class GetCurrentDirectory:
    pass


@attrs
class DetectRevision:
    directory = attrib()


@attrs
class AbortWithErrorMessage:
    message = attrib()


@attrs
class GetRevisionForLatestRelease:
    repository = attrib()
