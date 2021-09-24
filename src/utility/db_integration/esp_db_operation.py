from src.storage.sqlite import DbOperation
from src.api_consumer.esp_data.esp_apps_list import *

log_error = LogError()


def insert_into_db(data, esp_app_detail, business_criticality, db, auth):
    try:
        for result in data['result']:
            name = result['name']
            sys_id = result['sys_id']
            operational_status = result['operational_status']
            install_type = result['install_type']
            esp_details_url = esp_app_detail.format(name)
            business_criticality_url = business_criticality.format(name)
            get_esp_data = get_esp_details(esp_details_url, auth)
            get_business_criticality_data = get_business_criticality(business_criticality_url, auth)
            responsible_manager = get_esp_data['result'][0]["u_responsibility_manager"]["display_value"]
            business_criticality_value_ = get_business_criticality_data['result'][0]["u_res_business_criticality"]
            business_criticality_value = (
                business_criticality_value_ if business_criticality_value_ is not None else '')
            psa_user_name, psa_name = get_psa_data(get_esp_data, auth)
            es_user_name, es_name = get_es_data(get_esp_data, auth)
            db_operation = DbOperation(db)
            db_operation.application_data_operation(name=name, sys_id=sys_id, op_status=operational_status,
                                                    install_type=install_type, responsible_manager=responsible_manager,
                                                    business_criticality=business_criticality_value,
                                                    psa_user_name=psa_user_name, psa_name=psa_name,
                                                    es_user_name=es_user_name, es_name=es_name)
    except Exception as e:
        log_error.logs_error("Error " + str(e))
