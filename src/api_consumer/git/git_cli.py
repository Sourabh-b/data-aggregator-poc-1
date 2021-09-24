from src.adaptor.application_profiler.salesforceauth import git_repositories_sdfc, git_details_sdfc
from src.api_consumer.git.git_automation import *
from src.utility.apps.read import read_apps


def git_automation(sf, git_url, git_token, file, db):
    apps = read_apps('resources/' + file)
    session = authentication_session(url=git_url, token=git_token)
    session_owner_ = session.me().as_dict()
    session_owner = session_owner_['login']
    for app in apps:
        app_name = app['appName']
        git_urls = app['gitUrls']
        if len(git_urls) > 0:
            for git_url in git_urls:
                git_repo = git_url.split('/')[-1]
                git_org = git_url.split('/')[-2]
                git_repositories_sdfc(sf, app_name, git_repo, git_url)
                repos = repo(session, git_org, git_repo)
                for repository in repos:
                    contributor_details = get_contributor_details(repository)
                    languages = repository.repository.languages()
                    commit_date, url, contributors_count, pr_date = git_details(repository)
                    git_details_sdfc(commit_date, sf, app_name, git_url, git_repo, languages, pr_date, db,
                                     contributors_count, contributor_details, session_owner)
