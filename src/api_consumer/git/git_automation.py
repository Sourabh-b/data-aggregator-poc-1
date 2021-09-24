import github3
from datetime import datetime
from dateutil import tz
from src.utility.log.logs import *


def authentication_session(url: str = None, token: str = None):
    """
        Create a github3.py session for a GitHub Enterprise instance
        If token is not provided, will attempt to use the GH_TOKEN
        environment variable if present.
        """

    session = github3.github.GitHubEnterprise(url=url, token=token)
    if session is None:
        msg = "Unable to connect to GitHub Enterprise (%s) with provided token."
        raise RuntimeError(msg, url)
    return session


def repo(session, org_name, repo_name):
    search_string = org_name + '/' + repo_name
    repos = session.search_repositories(search_string)
    return repos


def git_details(repo):
    try:
        if repo is not None:
            full_repository = repo.repository.refresh()
            repo_profile = full_repository.as_dict()
            commit_date = datetime.fromisoformat(repo_profile['pushed_at'][:-1])
            repo_url = repo_profile['svn_url']
            contributors_count = get_contributors_count(repo)
            last_pr_date = latest_pull_req(repo)
            # Auto time-zone detection
            from_zone = tz.tzutc()
            # Convert to Local timezone
            utc = commit_date.replace(tzinfo=from_zone)
            return utc, repo_url, contributors_count, last_pr_date
    except Exception as e:
        logs_error("Couldn't find the value "+ str(e))


def latest_pull_req(repo):
    try:
        pull_reqs = repo.repository.pull_request(1)
        pull_req = pull_reqs.as_dict()
        pr_date = pull_req['created_at']
        last_pr_date = datetime.strptime(pr_date, "%Y-%m-%dT%H:%M:%SZ")
        return last_pr_date
    except Exception as e:
        logs_warning("Error in retriving PR Date - latest_pull_req" + str(e))


def get_contributors_count(repo):
    cont_count = []
    try:
        contributors = repo.repository.contributors()
        for contributor in contributors:
            cont_count.append(contributor)
        return len(cont_count)
    except Exception as e:
        logs_warning('Error in contributors..'+str(e))


def get_total_loc(languages):
    total_loc = 0
    for language in languages:
        total_loc += language[1]
    return total_loc


def get_loc_per_language(languages):
    for language_ in languages:
        language = language_[0]
        loc_per_language = language_[1]
        yield loc_per_language, language


def get_percentage(languages):
    lang_list = []
    total_loc = get_total_loc(languages)
    for loc_per_language, language in get_loc_per_language(languages):
        language_details = {}
        percentage = (loc_per_language / total_loc) * 100
        language_details['language'] = language
        language_details['loc'] = loc_per_language
        language_details['percentage'] = percentage
        lang_list.append(language_details)
    return lang_list, total_loc


def get_contributor_details(repo):
    # Contributor details = [{author.login, additions, deletions, commits}]
    addition = 0
    deletion = 0
    commits = 0
    author = ''
    contributor_list = []
    if repo is not None:
        contributors_stats = repo.repository.contributor_statistics()
        try:
            for contributor_stat in contributors_stats:
                contributor_stat = contributor_stat.as_dict()
                contributor_dict = {}
                for week in contributor_stat['weeks']:
                    addition += week['a']
                    deletion += week['d']
                    commits += week['c']
                author = contributor_stat['author']['login']
                contributions = contributor_stat['total']
                contributor_dict['author'] = author
                contributor_dict['addition'] = addition
                contributor_dict['deletion'] = deletion
                contributor_dict['commits'] = commits
                contributor_dict['contributions'] = contributions
                contributor_list.append(contributor_dict)
        except Exception as e:
            logs_error(e)
        finally:
            return contributor_list
