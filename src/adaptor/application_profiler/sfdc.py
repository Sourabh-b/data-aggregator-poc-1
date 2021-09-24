from src.storage.sqlite import DbOperation
from src.adaptor.application_profiler.salesforceauth import deployed_on, application_life_cycle,application_owner, \
    business_criticality, psa_data_function, es_data_function
from src.utility.beaking_functionality.esp_other_detail import break_responsible_manager, break_psa_details, break_es_details
from src.adaptor.application_profiler.salesforceauth import git_details_sdfc, git_repo_languages_sdfc, git_contributors_sfdc
from src.utility.log.logs import *
import datetime


def read_details(table_name, db_operation):
    records = db_operation.search_with_sys_id(table_name)
    return records


def search_and_push_to_sfdc(table_name, sys_id, sf, search):
    param = 'sys_id'
    result = search.fetch_a_row(table_name, param, sys_id)
    app_name = result[0][1]
    operational_status = result[0][3]
    install_type = result[0][4]
    responsible_manager = result[0][5]
    usr_name, owner_firstname, owner_lastname = break_responsible_manager(responsible_manager)
    business_criticality_value = result[0][6]
    psa_user_name = result[0][9]
    psa_nick_name = result[0][10]
    psa_first_name, psa_last_name = break_psa_details(psa_nick_name)
    es_user_name = result[0][11]
    es_nick_name = result[0][12]
    es_first_name, es_last_name = break_es_details(es_nick_name)
    deployed_on(install_type, sf, app_name)
    application_life_cycle(operational_status, sf, app_name)
    application_owner(sf, usr_name, app_name, owner_firstname, owner_lastname)
    business_criticality(business_criticality_value, sf, app_name)
    psa_data_function(sf, app_name, psa_user_name, psa_first_name, psa_last_name)
    es_data_function(sf, app_name, es_user_name, es_first_name, es_last_name)


def push_to_sfdc(table_name, sf, db):
    db_operation = DbOperation(db)
    records = read_details(table_name, db_operation)
    for record in records:
        search_and_push_to_sfdc(table_name, record[0], sf, db_operation)


def fetch_from_db(db, table_name):
    db_operation = DbOperation(db)
    records = db_operation.search_with_app_id(table_name)
    return records, db_operation


def git_push_to_sfdc(db, table_name, sf):
    records, db_operation = fetch_from_db(db, table_name)
    param = 'app_id'
    for record in records:
        try:
            results = db_operation.fetch_a_row(table_name, param, record[0])
            app_id = results[0][1]
            list_ = eval(results[0][2])
            for result in list_:
                commit_date = result['commit_date']
                commit_date = datetime.datetime.strptime(commit_date, "%Y-%m-%d %H:%M:%S%z")
                url = result['git_url']
                git_repo = result['git_repo']
                pr_date = result['pr_date']
                contributors_count = result['contributors_count']
                git_details_sdfc(commit_date, sf, app_id, url, git_repo, pr_date, contributors_count)
        except Exception as e:
            logs_error(str(e))


def git_language_push_to_sfdc(db, table_name, sf):
    records, db_operation = fetch_from_db(db, table_name)
    param = 'app_id'
    for record in records:
        try:
            results = db_operation.fetch_a_row(table_name, param, record[0])
            list_ = eval(results[0][2])
            for result in list_:
                url = result['git_url']
                languages = result['Languages']
                for language_ in languages:
                    language = language_['language']
                    loc_per_language = language_['loc']
                    percentage = language_['percentage']
                    git_repo_languages_sdfc(sf, url, language, loc_per_language, percentage)
        except Exception as e:
            logs_error(str(e))


def git_contributions_push_to_sfdc(db, table_name, sf):
    records, db_operation = fetch_from_db(db, table_name)
    param = 'app_id'
    for record in records:
        try:
            results = db_operation.fetch_a_row(table_name, param, record[0])
            list_ = eval(results[0][2])
            for result in list_:
                url = result['git_url']
                contributions_ = result['contribution_details']
                for contributors in contributions_:
                    cec_id = contributors['author']
                    contributions = contributors['contributions']
                    commits = contributors['commits']
                    addition = contributors['addition']
                    deletion = contributors['deletion']
                    git_contributors_sfdc(sf, url, cec_id, contributions, commits, addition, deletion)
        except Exception as e:
            logs_error(str(e))
