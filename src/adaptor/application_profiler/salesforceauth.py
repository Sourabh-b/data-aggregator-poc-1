from src.aop.logs.log_error import LogError
from src.aop.logs.log_msg import LogMsgs
from src.aop.logs.log_warning import LogWarning
from src.adaptor.application_profiler.sf_data_query import SfOperations
import datetime


logerror = LogError()
logmsgs = LogMsgs()
logwarning = LogWarning()


# Get the app_id
def _app_id(sf, app_name):
    try:
        query = "Select Id from App__c where Name = '{0}'".format(app_name)  # SQL Injection removed
        app_id = sf.query(query)
        return app_id
    except Exception as e:
        logmsgs.logs_msg(str(e) + " No app found in Security Dashboard")


def get_git_id(sf, url):
    query = "Select Id from Git_Details__c where Git_URL__c = '{0}'".format(url)
    git_id_query = sf.query(query)
    result_size = git_id_query.get('totalSize')
    if result_size > 0:
        git_id_records = git_id_query.get('records')
        sdfc_app_id = git_id_records[0]['Id']
        return sdfc_app_id
    else:
        return None


def _user_id(sf, usr_name, first_name, last_name):
    usr_id = None
    query = "Select Id from Transient_system_user__c where User_CEC_ID__c = '{0}'".format(usr_name)
    usr_id_query = sf.query(query)
    result_size = usr_id_query.get('totalSize')
    if result_size > 0:
        usr_id_ = usr_id_query.get('records')
        usr_id = usr_id_[0]['Id']
    else:
        data = {'Name': first_name, 'Last_Name__c': last_name, 'User_CEC_ID__c': usr_name}
        try:
            usr_id_ = sf.Transient_system_user__c.create(data)
            usr_id = dict(usr_id_)['Id']
        except Exception as sf_error:
            logerror.logs_error("Salesforce Error" + str(sf_error))

    return usr_id


def check_totalsize(sf, app_name):
    app_id = _app_id(sf, app_name)
    result_size = app_id.get('totalSize')
    if result_size > 0:
        app_id = app_id.get('records')
        app_id = app_id[0]['Id']
        return app_id
    else:
        logerror.logs_error("No app found in security dashboard with name {}".format(app_name))
        return None


def threatmodel_last_updated_date(updated_date, sf, app_name):
    app_id = check_totalsize(sf, app_name)
    if app_id is not None:
        if str(updated_date):
            tm_op = SfOperations()
            result = tm_op.threatmodel(sf=sf, updated_date=updated_date, app_id=app_id)
            if result == 204:
                logmsgs.logs_msg("'Threatmodel details' is updated successfully for {}".format(app_name))
            else:
                logwarning.logs_warning("'Threatmodel details' of {} is NOT updated successfully.".format(app_name))


def deployed_on(install_type, sf, app_name):
    app_id = check_totalsize(sf, app_name)
    if app_id is not None:
        it_op = SfOperations()
        result = it_op.deployed_on(sf, app_id, install_type)
        if result == 204:
            logmsgs.logs_msg("'Deployed_On' details is updated successfully for {}".format(app_name))
        else:
            logwarning.logs_warning("'Deployed_On' details of {} is NOT updated successfully.".format(app_name))


def application_life_cycle(op_status, sf, app_name):
    app_id = check_totalsize(sf, app_name)
    if app_id is not None:
        it_op = SfOperations()
        result = it_op.application_lyf_cycle(sf, app_id, op_status)
        if result == 204:
            logmsgs.logs_msg("'Application_Lifecycle' details is updated successfully for {}".format(app_name))
        else:
            logwarning.logs_warning("'Application_Lifecycle' details of {} is NOT updated successfully.".format(app_name))


def application_owner(sf, usr_name, app_name, first_name, last_name):
    app_id = check_totalsize(sf, app_name)
    if app_id is not None:
        usr_id = _user_id(sf, usr_name, first_name, last_name)
        if usr_id is not None:
            ao_op = SfOperations()
            result = ao_op.application_owner(usr_id, sf, app_id)
            if result == 204:
                logmsgs.logs_msg("'Application_Owner' details is updated successfully for {}".format(app_name))
            else:
                logwarning.logs_warning("'Application_Owner' details of {} is NOT updated successfully.".format(app_name))
        else:
            pass


def business_criticality(business_criticality, sf, app_name):
    app_id = check_totalsize(sf, app_name)
    if app_id is not None:
        bc_op = SfOperations()
        result = bc_op.business_criticality(business_criticality, sf, app_id)
        if result == 204:
            logmsgs.logs_msg("'Business_Criticality' details is updated successfully for {}".format(app_name))
        else:
            logwarning.logs_warning("'Business_Criticality' details of {} is NOT updated successfully.".format(app_name))


def psa_data_function(sf, app_name, psa_data, first_name, last_name):
    app_id = check_totalsize(sf, app_name)
    if app_id is not None:
        usr_id = _user_id(sf, psa_data, first_name, last_name)
        if usr_id is not None:
            psa_op = SfOperations()
            result = psa_op.partner_security_advocate_data(sf, app_id, usr_id)
            if result == 204:
                logmsgs.logs_msg("'PSA' details is updated successfully for {}".format(app_name))
            else:
                logwarning.logs_warning("'PSA' details of {} is NOT updated successfully.".format(app_name))
        else:
            logwarning.logs_warning("PSA User_Id not found for {0}".format(app_name))


def es_data_function(sf, app_name, es_data, first_name, last_name):
    app_id = check_totalsize(sf, app_name)
    if app_id is not None:
        usr_id = _user_id(sf, es_data, first_name, last_name)
        if usr_id is not None:
            es_op = SfOperations()
            result = es_op.executive_sponsor_data(sf, app_id, usr_id)
            if result == 204:
                logmsgs.logs_msg("'ES' details is updated successfully for {}".format(app_name))
            else:
                logwarning.logs_warning("'ES' details of {} is NOT updated successfully.".format(app_name))
        else:
            logwarning.logs_warning("ES User_Id not found for {0}".format(app_name))


def git_details_sdfc(commit_date, sf, app_id, url, git_repo, pr_date, contributors_count=0):
    if contributors_count is None:
        contributors_count = 0
    data = {
        "Name": git_repo,
        "CX_Application_Name__c": app_id,
        "CX_Commit_Date__c": commit_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Git_URL__c": url,
        "CX_Contributor_Count__c": int(contributors_count)
    }
    if pr_date != "None":
        pr_date = datetime.datetime.strptime(pr_date, "%Y-%m-%d %H:%M:%S")
        data["CX_last_PR_Date__c"] = pr_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        data["CX_last_PR_Date__c"] = ''

    query = "Select Id from Git_Details__c where Git_URL__c = '{0}'".format(url)
    git_id_query = sf.query(query)
    result_size = git_id_query.get('totalSize')
    if result_size > 0:
        git_id_records = git_id_query.get('records')
        sdfc_app_id = git_id_records[0]['Id']
        result = sf.Git_Details__c.update(sdfc_app_id, data)
        if result != 204:
            logmsgs.logs_msg("App is NOT updated successfully.")
    else:
        try:
            result = sf.Git_Details__c.create(data)
            if result != 200:
                raise ConnectionError("App is updated successfully.")
        except Exception as sf_error:
            logerror.logs_error("Salesforce Error " + str(sf_error))


def git_repo_languages_sdfc(sf, url, language, loc_per_language=0, percentage=0):
    # Git Id from Git_Details__c based on git application name
    git_id = get_git_id(sf, url)
    if git_id is not None:
        data = {
            "Name": language,
            "CX_Lines_of_Code__c": int(loc_per_language),
            "CX_Technology_Percentage__c": float(percentage),
            "CX_Git_Repository__c": git_id
        }
        query = "Select Id from CX_Git_Languages__c where CX_Git_Repository__c = '{0}' and Name = '{1}'".format(git_id,
                                                                                                                language)

        git_id_query = sf.query(query)
        result_size = git_id_query.get('totalSize')
        if result_size > 0:
            git_id_records = git_id_query.get('records')
            git_lang_id = git_id_records[0]['Id']
            result = sf.CX_Git_Languages__c.update(git_lang_id, data)
            if result == 204:
                logmsgs.logs_msg("App updated Successfully")
        else:
            result = sf.CX_Git_Languages__c.create(data)
            if result.get('records')[0]['success']:
                logmsgs.logs_msg("App is created successfully..")


def get_total_loc(languages):
    total_loc = 0
    for language in languages:
        total_loc += language[1]
    return total_loc


def git_contributors_sfdc(sf, url, cec_id, contributions, commits, addition, deletion):
    git_id = get_git_id(sf, url)
    if git_id is not None:
        data = {
            "Name": cec_id,
            "CX_Git_Repository__c": git_id,
            "CX_Contributions__c": contributions,
            "CX_Commits__c": commits,
            "CX_Additions__c": addition,
            "CX_Deletions__c": deletion,
        }
        # Get the repository id based on the url
        query = "Select Id from CX_Git_Contributors__c where Name = '{0}' and CX_Git_Repository__c = '{1}'".format(
            cec_id, git_id)
        git_id_query = sf.query(query)
        result_size = git_id_query.get('totalSize')
        if result_size > 0:
            git_id_records = git_id_query.get('records')
            contributor_id = git_id_records[0]['Id']
            result = sf.CX_Git_Contributors__c.update(contributor_id, data)
            if result == 204:
                logmsgs.logs_msg("App updated Successfully")
        else:
            result = sf.CX_Git_Contributors__c.create(data)
            if result.get('records')[0]['success']:
                logmsgs.logs_msg("App Created")


def git_repositories_sdfc(sf, app_name, git_repo, url):
    app_id = check_totalsize(sf, app_name)
    '''Calculate Total language of code'''
    data = {
        "Name": git_repo,
        "CX_Application_Name__c": app_id,
        "Git_URL__c": url
    }
    query = "Select Id from Git_Details__c where Git_URL__c = '{0}'".format(url)
    git_id_query = sf.query(query)
    result_size = git_id_query.get('totalSize')
    if result_size > 0:
        git_id_records = git_id_query.get('records')
        sdfc_app_id = git_id_records[0]['Id']
        result = sf.Git_Details__c.update(sdfc_app_id, data)
        if result != 204:
            raise ConnectionError("App is NOT updated successfully.")
    else:
        result = sf.Git_Details__c.create(data)
        if result != 200:
            raise ConnectionError("App is NOT updated successfully.")
