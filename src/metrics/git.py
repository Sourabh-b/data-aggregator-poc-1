import csv
import yaml
import sqlite3

stream = open("settings/config_data.yml")
dictionary = yaml.load(stream, Loader=yaml.BaseLoader)
git_details_csv = dictionary['git_basic_csv']
git_languages_csv = dictionary['git_language_csv']
git_contributors_csv = dictionary['git_contributors']
git_base_data_table_name = "TBL_GIT_DETAILS"
git_language_table_name = "TBL_GIT_LANGUAGE"
git_contributions_table_name = "TBL_GIT_CONTRIBUTIONS"

config_file = open("settings/config_secrets.yml")
parsed_file = yaml.load(config_file, Loader=yaml.BaseLoader)
db = parsed_file['db_name'] + ".db"


def git_basic_details_csv(db, table_name=git_base_data_table_name):
    file_path = 'git_metrics/' + git_details_csv
    header = ['application_name', 'app_id', 'git_repo', 'commit_date', 'pr_date', 'contributor_count', 'git_urls', 'date', 'updated_by']
    with open(file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    db = 'resources/' + db
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    data_fetch = "select * from {0};".format(table_name)
    cursor.execute(data_fetch)
    records = cursor.fetchall()
    f = open(file_path, 'a')
    writer = csv.writer(f)
    for record in records:
        writer.writerow(record)
    f.close()


def git_languages_details_csv(db, table_name=git_language_table_name):
    file_path = 'git_metrics/' + git_languages_csv
    header = ['application_name', 'languages', 'loc', 'percentage']
    with open(file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    db = 'resources/' + db
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    data_fetch = "select * from {0};".format(table_name)
    cursor.execute(data_fetch)
    records = cursor.fetchall()
    f = open(file_path, 'a')
    writer = csv.writer(f)
    for record in records:
        writer.writerow(record)
    f.close()


def git_contributors_details_csv(db, table_name=git_contributions_table_name):
    file_path = 'git_metrics/' + git_contributors_csv
    header = ['application_name', 'name', 'contributions', 'commits', 'additions', 'deletions']
    with open(file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    db = 'resources/' + db
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    data_fetch = "select * from {0};".format(table_name)
    cursor.execute(data_fetch)
    records = cursor.fetchall()
    f = open(file_path, 'a')
    writer = csv.writer(f)
    for record in records:
        writer.writerow(record)
    f.close()

git_basic_details_csv(db)
git_languages_details_csv(db)
git_contributors_details_csv(db)
