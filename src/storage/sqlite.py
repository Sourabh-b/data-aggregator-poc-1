import sqlite3
import datetime
import hashlib
import yaml
from src.aop.logs.log_error import LogError
from src.aop.logs.log_msg import LogMsgs
from src.aop.logs.log_warning import LogWarning

logerror = LogError()
logmsgs = LogMsgs()
logwarning = LogWarning()

stream = open("settings/config_data.yml")
dictionary = yaml.load(stream, Loader=yaml.BaseLoader)
application_table_name = dictionary['application_table_name']
threatmodel_table_name = dictionary['threatmodel_table_name']
git_base_data_table_name = dictionary['git_base_data_table_name']
git_language_table_name = dictionary['git_language_table_name']
git_contributions_table_name = dictionary['git_contributions_table_name']
git_details_csv = dictionary['git_basic_csv']
git_languages_csv = dictionary['git_language_csv']
git_contributors_csv = dictionary['git_contributors']


def unique_id_generator(sys_id):
    hash = hashlib.sha1(str.encode(sys_id)).hexdigest()
    len = int(dictionary['uuid_char_len'])
    return hash[:len]


class DbOperation:

    def __init__(self, db):
        self.db = 'resources/' + db
        self.sqliteConnection = sqlite3.connect(self.db)
        self.cursor = self.sqliteConnection.cursor()

    def check_table_exists(self, table_name: str, query):
        self.cursor.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{0}'".format(table_name))

        # if the count is 1, then table exists
        if self.cursor.fetchone()[0] == 1:
            logmsgs.logs_msg('{0} Table is present'.format(table_name))
        else:
            logmsgs.logs_msg("{0} Table is not present, creating one.....".format(table_name))
            self.cursor.execute("CREATE TABLE {0} {1}".format(table_name, query))

    def update(self, table_name: str = None, app_name: str = None, last_updated: str = None, op_status: str = None,
               install_type: str = None, responsible_manager: str = None, business_criticality: str = None,
               sys_id: str = None,
               git_urls: str = None, psa_user_name: str = None, psa_name: str = None, es_user_name: str = None,
               es_name: str = None):
        query = "UPDATE {0} SET application_name ='{7}', updated_at ='{1}', operational_status='{2}', install_type='{3}', responsible_manager='{4}', business_criticality='{5}', git_urls= '{8}', Partner_Security_Advocate_user_name='{9}', Partner_Security_Advocate_Name='{10}', Executive_Sponsor_user_name='{11}', Executive_Sponsor_Name='{12}' WHERE sys_id='{6}';".format(
            table_name, last_updated, op_status, install_type, responsible_manager, business_criticality, sys_id,
            app_name, git_urls, psa_user_name, psa_name, es_user_name, es_name)
        result = self.cursor.execute(query)
        if result.arraysize:
            logmsgs.logs_msg('Table row updated successfully')
        else:
            logwarning.logs_warning('Table row NOT updated successfully')

    def insert(self, table_name: str = None, uuid: str = None, name: str = None, updated_at: str = None,
               op_status: str = None, install_type: str = None,
               responsible_manager: str = None,
               business_criticality: str = None, sys_id: str = None, git_urls: str = None, psa_user_name: str = None,
               psa_name: str = None, es_user_name: str = None, es_name: str = None):
        query = """INSERT INTO {0} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""".format(table_name)
        values = (
            uuid, name, updated_at, op_status, install_type, responsible_manager, business_criticality, sys_id,
            git_urls,
            psa_user_name, psa_name, es_user_name, es_name)
        result = self.cursor.execute(query, values)
        if result.arraysize:
            logmsgs.logs_msg('New value inserted successfully into the table')
        else:
            logwarning.logs_warning('Failed to insert new value into the table')

    def update_table(self, table_name: str = None, uuid: str = None, app: str = None, last_updated: str = None,
                     op_status: str = None, install_type: str = None,
                     responsible_manager: str = None, business_criticality: str = None, sys_id: str = None,
                     git_urls: str = None, psa_user_name: str = None,
                     psa_name: str = None, es_user_name: str = None, es_name: str = None):
        data_fetch = "select sys_id from {0};".format(table_name)
        self.cursor.execute(data_fetch)
        records = self.cursor.fetchall()
        for record in records:
            if sys_id == record[0]:
                self.update(table_name, app, last_updated, op_status, install_type, responsible_manager,
                            business_criticality, sys_id, git_urls, psa_user_name, psa_name, es_user_name, es_name)
                break
            else:
                continue
        else:
            self.insert(table_name, uuid, app, last_updated, op_status, install_type, responsible_manager,
                        business_criticality, sys_id, git_urls)

    def git_base_update(self, table_name, app_name, app_id=None, git_details=None, updated_at=None, updated_by=None):
        query = "UPDATE {0} SET app_id='{2}', git_details={3},  date='{4}', updated_by='{5}' WHERE application_name='{1}';".format(
            table_name, app_name, app_id, git_details, updated_at,
            updated_by)
        result = self.cursor.execute(query)
        if result.arraysize:
            logmsgs.logs_msg('Table row updated successfully')
        else:
            logwarning.logs_warning('Table row NOT updated successfully')

    def git_base_insert(self, table_name=None, app_name=None, app_id=None, git_details=None, updated_at=None, updated_by=None):
        try:
            query = """INSERT INTO {0} VALUES (?, ?, ?, ?, ?)""".format(table_name)
            values = (app_name, app_id, git_details, updated_at,
                      updated_by)
            result = self.cursor.execute(query, values)
            if result.arraysize:
                logmsgs.logs_msg('New value inserted successfully into the table')
            else:
                logwarning.logs_warning('Failed to insert new value into the table')
        except Exception as e:
            logerror.logs_error("Error: " + str(e))

    def update_git_base_table(self, table_name: str = None, app: str = None, app_id=None, git_details=None, updated_at=None, updated_by=None):
        data_fetch = "select application_name from {0};".format(table_name)
        self.cursor.execute(data_fetch)
        records = self.cursor.fetchall()
        for record in records:
            if app == record[0]:
                self.git_base_update(table_name, app, app_id, git_details, updated_at, updated_by)
                break
            else:
                continue
        else:
            try:
                self.git_base_insert(table_name, app, app_id, git_details, updated_at, updated_by)
            except Exception as e:
                logerror.logs_error("Not inserted " + str(e))
        self.sqliteConnection.commit()

    def git_language_table_update(self, table_name=None, app=None, app_id=None, loc=None, git_language_details=None):
        data_fetch = "select application_name from {0};".format(table_name)
        self.cursor.execute(data_fetch)
        records = self.cursor.fetchall()
        for record in records:
            if app == record[0]:
                self.git_language_update(table_name, app, app_id,
                                         loc, git_language_details)
                break
            else:
                continue
        else:
            try:
                self.git_language_insert(table_name, app, app_id,
                                         loc, git_language_details)
            except Exception as e:
                logerror.logs_error("Not inserted " + str(e))

    def git_language_update(self, table_name, app, app_id, loc, git_language_details):
        query = "UPDATE '{0}' SET app_id='{2}', git_language='{3}', loc={4} WHERE application_name='{1}';".format(
            table_name, app, app_id, git_language_details, loc)
        result = self.cursor.execute(query)
        if result.arraysize:
            logmsgs.logs_msg('Table row updated successfully')
        else:
            logwarning.logs_warning('Table row NOT updated successfully')

    def git_language_insert(self, table_name, app, app_id, loc, git_language_details):
        try:
            query = "INSERT INTO {0} VALUES (?, ?, ?, ?)".format(table_name)
            values = (app, app_id, git_language_details, loc)
            result = self.cursor.execute(query, values)
            if result.arraysize:
                logmsgs.logs_msg('New value inserted successfully into the table')
            else:
                logwarning.logs_warning('Failed to insert new value into the table')
        except Exception as e:
            logerror.logs_error("Error: " + str(e))

    def git_contributions_update(self, table_name=None, app_name=None, app_id=None, contributions_details=None):
        data_fetch = "select application_name from {0};".format(table_name)
        self.cursor.execute(data_fetch)
        records = self.cursor.fetchall()
        for record in records:
            if app_name == record[0]:
                self.update_contributions(table_name, app_name, app_id, contributions_details)
                break
            else:
                continue
        else:
            try:
                self.insert_contributions(table_name, app_name, app_id, contributions_details)
            except Exception as e:
                logerror.logs_error("Not inserted " + str(e))

    def update_contributions(self, table_name, app_name, app_id, contributions_details):
        query = "UPDATE {0} SET app_id='{2}', contribution_details='{3}' WHERE application_name='{1}';".format(
            table_name, app_name, app_id, contributions_details)
        result = self.cursor.execute(query)
        if result.arraysize:
            logmsgs.logs_msg('Table row updated successfully')
        else:
            logwarning.logs_warning('Table row NOT updated successfully')

    def insert_contributions(self, table_name, app_name, app_id, contributions_details):
        try:
            query = """INSERT INTO {0} VALUES (?, ?, ?)""".format(table_name)
            values = (app_name, app_id, contributions_details)
            result = self.cursor.execute(query, values)
            if result.arraysize:
                logmsgs.logs_msg('New value inserted successfully into the table')
            else:
                logwarning.logs_warning('Failed to insert new value into the table')
        except Exception as e:
            logerror.logs_error("Error: " + str(e))

    '''Main calling functions'''

    def application_data_operation(self, name=None, op_status=None, install_type=None, responsible_manager=None,
                                   business_criticality=None, sys_id=None, git_urls=None, psa_user_name=None,
                                   psa_name=None, es_user_name=None, es_name=None):
        try:
            uuid = unique_id_generator(sys_id)
            query = "(uuid TEXT PRIMARY KEY, application_name TEXT, updated_at DATETIME, operational_status TEXT, " \
                    "install_type TEXT, responsible_manager TEXT, business_criticality TEXT, sys_id TEXT, git_urls " \
                    "STRING, Partner_Security_Advocate_user_name TEXT, Partner_Security_Advocate_Name TEXT, " \
                    "Executive_Sponsor_user_name TEXT, Executive_Sponsor_Name TEXT); "
            self.check_table_exists(application_table_name, query)
            updated_at = datetime.date.today().strftime("%m-%d-%y")
            self.update_table(table_name=application_table_name, uuid=uuid, app=name, last_updated=updated_at,
                              op_status=op_status, install_type=install_type, responsible_manager=responsible_manager,
                              business_criticality=business_criticality, sys_id=sys_id, git_urls=git_urls,
                              psa_user_name=psa_user_name,
                              psa_name=psa_name, es_user_name=es_user_name, es_name=es_name)
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            logerror.logs_error(error)

    def git_base_data_table(self, app_name=None, app_id=None, git_details=None, session_owner=None):
        try:
            query = "(application_name TEXT, app_id TEXT, git_details STRING, date DATETIME, updated_by TEXT); "
            self.check_table_exists(git_base_data_table_name, query)
            updated_at = datetime.date.today().strftime("%m-%d-%y")
            self.update_git_base_table(table_name=git_base_data_table_name, app=app_name, app_id=app_id, git_details=git_details,
                                       updated_at=updated_at, updated_by=session_owner)
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            logerror.logs_error(error)

    def git_language_details(self, application_name=None, app_id=None, loc=None, git_language_details=None):
        try:
            query = "(application_name TEXT, app_id TEXT, git_language STRING, loc INT);"
            self.check_table_exists(git_language_table_name, query)
            self.git_language_table_update(table_name=git_language_table_name, app=application_name, app_id=app_id,
                                           git_language_details=git_language_details, loc=loc)
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            logerror.logs_error(error)

    def git_contributor_details(self, app_name=None, app_id=None, contributions_details=None):
        try:
            query = "(application_name TEXT, app_id TEXT, contribution_details STRING);"
            self.check_table_exists(git_contributions_table_name, query)
            self.git_contributions_update(table_name=git_contributions_table_name, app_name=app_name, app_id=app_id, contributions_details=contributions_details)
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            logerror.logs_error(error)

    def threatmodel_data_operation(self):
        try:
            data_fetch = "select application_name, Threat_Model_ID from {0};".format(threatmodel_table_name)
            self.cursor.execute(data_fetch)
            records = self.cursor.fetchall()
            return records
        except sqlite3.Error as error:
            logerror.logs_error(error)
        finally:
            if self.sqliteConnection:
                self.sqliteConnection.close()

    def search_with_sys_id(self, table_name):
        data_fetch = "select sys_id from {0};".format(table_name)
        self.cursor.execute(data_fetch)
        records = self.cursor.fetchall()
        return records

    def fetch_a_row(self, table_name, param='', param_value=''):
        query = "select * from {0} where {1}='{2}'".format(table_name, param, param_value)
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        return records

    def search_with_app_id(self, table_name):
        data_fetch = "select app_id from {0};".format(table_name)
        self.cursor.execute(data_fetch)
        records = self.cursor.fetchall()
        return records
