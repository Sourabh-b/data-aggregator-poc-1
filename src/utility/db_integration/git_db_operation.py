from src.storage.sqlite import DbOperation
from src.utility.log.logs import *
from src.adaptor.application_profiler.salesforceauth import check_totalsize
from src.utility.git_base.git_data_fetch import data_fetch_for_each_repo
from src.authentications.git_auth import *
import yaml
import json


def common_updater(git_splitted_url, session, git_details, git_contribution_details, git_language_details):
    commit_date, url, contributors_count, pr_date, languages, git_repo, lang_list, total_loc, contribution_details = data_fetch_for_each_repo(
        git_splitted_url, session)
    git_contribution_details['git_url'] = url
    git_contribution_details['contribution_details'] = contribution_details
    session_owner_ = session.me().as_dict()
    session_owner = session_owner_['login']
    git_language_details['git_url'] = url
    git_language_details['Languages'] = lang_list
    git_details['git_url'] = url
    git_details['git_repo'] = git_repo
    git_details['commit_date'] = str(commit_date)
    git_details['pr_date'] = str(pr_date)
    git_details['contributors_count'] = contributors_count
    return languages, total_loc, session_owner, git_details, git_contribution_details, git_language_details


def www_auth(git_splitted_url):
    file = open("settings/config_secrets.yml")
    parsed_file = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    token = parsed_file['www_git_token']
    git_base_url = git_splitted_url[0] + '//' + git_splitted_url[2]
    www_session = authentication_session(url=git_base_url, token=token)
    return www_session


def wwwin_auth(git_splitted_url):
    file = open("settings/config_secrets.yml")
    parsed_file = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    token = parsed_file['wwwin_git_token']
    git_base_url = git_splitted_url[0] + '//' + git_splitted_url[2]
    wwwin_session = authentication_session(url=git_base_url, token=token)
    return wwwin_session


def store_into_db(apps, db, sf):
    session_owner = None
    total_loc = None
    store = DbOperation(db)
    www_session = None
    wwwin_session = None
    for app in apps:
        git_base_list = []
        git_language_list = []
        git_contribution_list = []
        app_name = app['appName']
        git_urls_ = app['gitUrls']
        app_id = check_totalsize(sf, app_name)
        if len(git_urls_) > 0:
            for git_url in git_urls_:
                git_details = {}
                git_contribution_details = {}
                git_language_details ={}
                try:
                    git_splitted_url = git_url.split('/')
                    if 'www-github.cisco.com' in git_splitted_url:
                        if www_session is None:
                            www_session = www_auth(git_splitted_url)
                            languages, total_loc, session_owner, git_details, git_contribution_details, git_language_details = common_updater(
                                git_splitted_url, www_session, git_details, git_contribution_details, git_language_details)
                        else:
                            languages, total_loc, session_owner, git_details, git_contribution_details, git_language_details = common_updater(
                                git_splitted_url, www_session, git_details, git_contribution_details, git_language_details)

                    elif 'wwwin-github.cisco.com' in git_splitted_url:
                        if wwwin_session is None:
                            wwwin_session = wwwin_auth(git_splitted_url)
                            languages, total_loc, session_owner, git_details, git_contribution_details, git_language_details = common_updater(
                                git_splitted_url, wwwin_session, git_details, git_contribution_details, git_language_details)

                        else:
                            languages, total_loc, session_owner, git_details, git_contribution_details, git_language_details = common_updater(git_splitted_url,
                                wwwin_session, git_details, git_contribution_details, git_language_details)
                    else:
                        continue

                    git_base_list.append(git_details)
                    git_language_list.append(git_language_details)
                    git_contribution_list.append(git_contribution_details)
                except Exception as e:
                    logs_warning("Github error " + str(e))
                    continue
        git_base_list = json.dumps(git_base_list)
        git_language_list = json.dumps(git_language_list)
        git_contribution_list = json.dumps(git_contribution_list)
        store.git_base_data_table(app_name=app_name, app_id=app_id, git_details=git_base_list, session_owner=session_owner)
        store.git_language_details(application_name=app_name, app_id=app_id, git_language_details=git_language_list, loc=total_loc)
        store.git_contributor_details(app_name=app_name, app_id=app_id, contributions_details=git_contribution_list)

    if store.sqliteConnection:
        store.sqliteConnection.close()
