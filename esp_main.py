from src.authentications.esp_auth import authentication
from src.authentications.sf import sf_auth
from src.utility.read_config import *
from src.api_consumer.esp_data.esp_apps_list import get_apps
from src.adaptor.application_profiler.sfdc import push_to_sfdc
from src.utility.db_integration.esp_db_operation import insert_into_db

_, username, password, sts_uri, instance, db, username_salesforce, password_salesforce, security_token, client_id, \
domain, esp_url, esp_app_detail, business_criticality = read_config_secret()
app_table_name, _, _, _ = read_config_data()

auth = authentication(username, password, sts_uri, instance)
sf = sf_auth(username_salesforce, password_salesforce, security_token, client_id, domain)

if __name__ == '__main__':
    app_data = get_apps(esp_url, auth)
    insert_into_db(app_data, esp_app_detail, business_criticality, db, auth)
    #push_to_sfdc(app_table_name, sf, db)
