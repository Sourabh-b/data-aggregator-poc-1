import yaml


def read_config_secret():
    file = open("settings/config_secrets.yml")
    parsed_file = yaml.load(file, Loader=yaml.FullLoader)
    file_name = parsed_file['apps']
    username = parsed_file['usr_id']
    password = parsed_file['pasword']
    sts_uri = parsed_file['sts_uri']
    instance = parsed_file['instance']
    db = parsed_file['db_name'] + ".db"
    sf_user = parsed_file['username']
    sf_password = parsed_file['password']
    security_token = parsed_file['security_token']
    client_id = parsed_file['client_id']
    domain = parsed_file['domain']
    esp_url = parsed_file['esp_api']
    esp_app_detail = parsed_file['esp_app_details']
    business_criticality = parsed_file['business_criticality']
    file.close()
    return file_name, username, password, sts_uri, instance, db, sf_user, sf_password, \
           security_token, client_id, domain, esp_url, esp_app_detail, business_criticality


def read_config_data():
    file = open("settings/config_data.yml")
    parsed_file = yaml.load(file, Loader=yaml.FullLoader)
    application_table_name = parsed_file['application_table_name']
    git_base_table = parsed_file['git_base_data_table_name']
    git_language_table = parsed_file['git_language_table_name']
    git_contribution_table = parsed_file['git_contributions_table_name']
    file.close()

    return application_table_name, git_base_table, git_language_table, git_contribution_table
