from src.utility.read_config import *
from src.utility.apps.read import read_apps
from src.utility.db_integration.git_db_operation import *
from src.authentications.sf import *
from src.adaptor.application_profiler.sfdc import git_push_to_sfdc, git_language_push_to_sfdc, git_contributions_push_to_sfdc

# Read secret config file
file, _, _, _, _, db, sf_user, sf_password, security_token, client_id, domain, _, _, _ = read_config_secret()

# Read data config file
_, git_base_table, git_language_table, git_contribution_table = read_config_data()

# Check sf authentication
sf = sf_auth(sf_user, sf_password, security_token, client_id, domain)

# Read repo mappings for apps
apps = read_apps('resources/' + file)
store_into_db(apps, db, sf)
git_push_to_sfdc(db, git_base_table, sf)
git_language_push_to_sfdc(db, git_language_table, sf)
git_contributions_push_to_sfdc(db, git_contribution_table, sf)

