from src.utility.log.logs import *
from src.api_consumer.git.git_automation import repo, git_details, get_contributor_details, get_percentage


def data_fetch_for_each_repo(git_url, session):
    git_repo = git_url[-1]
    git_org = git_url[-2]
    repos = repo(session, git_org, git_repo)
    for repository in repos:
        try:
            contribution_details = fetch_contributor_details(repository)
            languages = repository.repository.languages()
            commit_date, url, contributors_count, pr_date = git_details(repository)
            lang_list, total_loc = get_percentage(languages)
            return commit_date, url, contributors_count, pr_date, languages, git_repo, lang_list, total_loc, \
                   contribution_details
        except Exception as e:
            logs_error(str(e) + " Repository not found for " + git_repo)


def fetch_contributor_details(repository):
    contributor_details = get_contributor_details(repository)
    contribution_detail = []
    for contributor in contributor_details:
        contributor_details = {'author': contributor['author'], 'contributions': contributor['contributions'],
                               'commits': contributor['commits'], 'addition': contributor['addition'],
                               'deletion': contributor['deletion']}
        contribution_detail.append(contributor_details)
    return contribution_detail
