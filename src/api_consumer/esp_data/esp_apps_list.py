import requests
from src.utility.beaking_functionality.esp_other_detail import partner_security_advocate_data, executive_sponsor
from src.aop.logs.log_error import LogError

headers = {"Content-Type": "application/json", "Accept": "application/json"}
log_error = LogError()


def get_apps(url, auth):
    # Do the HTTP request
    response = requests.get(url, auth=auth, headers=headers)
    data = response.json()
    return data


def get_esp_details(esp_app_detail, auth):

    # Do the HTTP request
    response = requests.get(esp_app_detail, auth=auth, headers=headers)
    data = response.json()
    return data


def get_business_criticality(business_criticality, auth):

    # Do the HTTP request
    response = requests.get(business_criticality, auth=auth, headers=headers)
    data = response.json()
    return data


def get_psa_data(data, auth):
    psa_data = partner_security_advocate_data(data, auth, headers)
    try:
        psa_user_name = psa_data['result']['user_name']
        psa_nickname = psa_data['result']['u_nickname']
        return psa_user_name, psa_nickname
    except Exception as psa_exception:
        log_error.logs_error('No PSA data received...' + str(psa_exception))


def get_es_data(data, auth):
    es_data = executive_sponsor(data, auth, headers)
    try:
        es_user_name = es_data['result']['user_name']
        es_nickname = es_data['result']['u_nickname']
        return es_user_name, es_nickname
    except Exception as es_exception:
        log_error.logs_error("No Executive Sponsor data received...." + str(es_exception))