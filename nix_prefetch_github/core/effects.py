"""This module contains data structures that describe all the side
effects that the core module expects to be performed
"""

from attr import attrib, attrs


@attrs
class GetListRemote:
    owner = attrib()
    repo = attrib()


@attrs
class CheckGitRepoIsDirty:
    directory = attrib()


@attrs
class ShowWarning:
    message = attrib()


@attrs
class TryPrefetch:
    owner = attrib()
    repo = attrib()
    sha256 = attrib()
    rev = attrib()
    fetch_submodules = attrib(default=False)


@attrs
class CalculateSha256Sum:
    owner = attrib()
    repo = attrib()
    revision = attrib()
    fetch_submodules = attrib(default=False)


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
