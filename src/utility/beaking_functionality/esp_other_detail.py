from src.aop.logs.log_error import LogError
import requests

logerror = LogError()


def partner_security_advocate_data(data, auth, headers):
    security_architect_data = {}
    try:
        service_offering_link = data['result'][0]['u_service_offering']['link']
        service_offering_response = requests.get(service_offering_link, auth=auth, headers=headers)
        service_offering_data = service_offering_response.json()
        security_architect_link = service_offering_data['result']['u_partner_security_architect']['link']
        security_architect_response = requests.get(security_architect_link, auth=auth, headers=headers)
        security_architect_data = security_architect_response.json()
    except Exception as psa_exception:
        logerror.logs_error("PSA Service Failure......" + str(psa_exception))
    return security_architect_data


def executive_sponsor(data, auth, headers):
    assigned_to_data = {}
    try:
        service_offering_link = data['result'][0]['u_service_offering']['link']
        service_offering_response = requests.get(service_offering_link, auth=auth, headers=headers)
        service_offering_data = service_offering_response.json()
        service_name_link = service_offering_data['result']['u_service_name']['link']
        service_name_response = requests.get(service_name_link, auth=auth, headers=headers)
        service_name_data = service_name_response.json()
        assigned_to_link = service_name_data['result']['assigned_to']['link']
        assigned_to_response = requests.get(assigned_to_link, auth=auth, headers=headers)
        assigned_to_data = assigned_to_response.json()
    except Exception as es_exception:
        logerror.logs_error("ES Service Failure......" + str(es_exception))
    return assigned_to_data


def break_responsible_manager(responsible_manager):
    # Application Owner
    splited_array = responsible_manager.split(' ')
    if len(splited_array) > 3:
        owner_firstname = responsible_manager.split(' ')[0]
        owner_middlename = responsible_manager.split(' ')[1]
        owner_lastname = responsible_manager.split(' ')[-2]
    else:
        owner_firstname = responsible_manager.split(' ')[0]
        owner_lastname = responsible_manager.split(' ')[1]
    usr_name = responsible_manager.split(' ')[-1][1:-1]
    return usr_name, owner_firstname, owner_lastname


def break_psa_details(psa_nickname):
    psa_nickname = psa_nickname.split(' ')
    psa_first_name = psa_nickname[0]
    psa_last_name = psa_nickname[-1]
    return psa_first_name, psa_last_name


def break_es_details(es_nickname):
    es_nickname = es_nickname.split(' ')
    es_first_name = es_nickname[0]
    es_last_name = es_nickname[-1]
    return es_first_name, es_last_name

