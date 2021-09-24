from github3.github import GitHubEnterprise


def authentication_session(url: str = None, token: str = None):
    """
        Create a github3.py session for a GitHub Enterprise instance
        If token is not provided, will attempt to use the GH_TOKEN
        environment variable if present.
        """

    session = GitHubEnterprise(url=url, token=token)
    if session is None:
        msg = "Unable to connect to GitHub Enterprise (%s) with provided token."
        raise RuntimeError(msg, url)
    return session