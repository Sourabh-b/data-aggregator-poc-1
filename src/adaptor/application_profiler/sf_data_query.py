import yaml


class SfOperations:
    def __init__(self):
        self.stream = open("settings/config_data.yml")
        self.dictionary = yaml.load(self.stream, Loader=yaml.BaseLoader)
        self.stream.close()

    def threatmodel(self, sf, updated_date, app_id):
        threat_model_done = self.dictionary['threatmodel']['threatmodel_done']
        data = {
            self.dictionary['threatmodel']['threatmodel_status']: threat_model_done,
            self.dictionary['threatmodel']['threatmodel_date']: updated_date  # Validated updated date
        }
        result = sf.App__c.update(app_id, data)
        return result

    def deployed_on(self, sf, app_id, install_type):
        if install_type == self.dictionary['esp_data']['install_type'][0]:
            data = {
                self.dictionary['install_type']['sf_field']: self.dictionary['install_type']['Externally Hosted']
            }
        elif install_type == self.dictionary['esp_data']['install_type'][1]:
            data = {
                self.dictionary['install_type']['sf_field']: self.dictionary['install_type']['On Premise']
            }
        elif install_type == self.dictionary['esp_data']['install_type'][2]:
            data = {
                self.dictionary['install_type']['sf_field']: self.dictionary['install_type']['External SaaS']
            }
        elif install_type == self.dictionary['esp_data']['install_type'][3]:
            data = {
                self.dictionary['install_type']['sf_field']: self.dictionary['install_type']['on_premise']
            }
        elif install_type == self.dictionary['esp_data']['install_type'][4]:
            data = {
                self.dictionary['install_type']['sf_field']: self.dictionary['install_type']['External PaaS']
            }
        elif install_type == self.dictionary['esp_data']['install_type'][5]:
            data = {
                self.dictionary['install_type']['sf_field']: self.dictionary['install_type']['External IaaS']
            }
        else:
            data = {
                self.dictionary['install_type']['sf_field']: 'Not Available in ESP'
            }
        result = sf.App__c.update(app_id, data)
        return result

    def application_lyf_cycle(self, sf, app_id, op_status):
        if op_status == self.dictionary['esp_data']['op_status'][0]:
            data = {
                self.dictionary['op_status']['sf_field']: self.dictionary['op_status']['Pipeline']
            }
        elif op_status == self.dictionary['esp_data']['op_status'][1]:
            data = {
                self.dictionary['op_status']['sf_field']: self.dictionary['op_status']['Retired']
            }
        elif op_status == self.dictionary['esp_data']['op_status'][2]:
            data = {
                self.dictionary['op_status']['sf_field']: self.dictionary['op_status']['Operational']
            }
        else:
            data = {
                self.dictionary['op_status']['sf_field']: 'Not Available in ESP'
            }
        result = sf.App__c.update(app_id, data)
        return result

    def application_owner(self, usr_id, sf, app_id):
        if usr_id is not None:
            data = {
                self.dictionary['application_owner']: usr_id
            }
            result = sf.App__c.update(app_id, data)
            return result

    def business_criticality(self, business_criticality, sf, app_id):
        if str(business_criticality) == self.dictionary['esp_data']['business_criticality'][0]:
            data = {
                self.dictionary['business_criticality']["field_name"]: self.dictionary['business_criticality']["col1"]
            }
        elif str(business_criticality) == self.dictionary['esp_data']['business_criticality'][1]:
            data = {
                self.dictionary['business_criticality']["field_name"]: self.dictionary['business_criticality']["col2"]
            }
        elif str(business_criticality) == self.dictionary['esp_data']['business_criticality'][2]:
            data = {
                self.dictionary['business_criticality']["field_name"]: self.dictionary['business_criticality']["col3"]
            }
        elif str(business_criticality) == self.dictionary['esp_data']['business_criticality'][3]:
            data = {
                self.dictionary['business_criticality']["field_name"]: self.dictionary['business_criticality']["col4"]
            }
        elif str(business_criticality) == self.dictionary['esp_data']['business_criticality'][4]:
            data = {
                self.dictionary['business_criticality']["field_name"]: self.dictionary['business_criticality']["col5"]
            }
        else:
            data = {
                self.dictionary['business_criticality']["field_name"]: "Not Available in ESP"
            }

        result = sf.App__c.update(app_id, data)
        return result

    def partner_security_advocate_data(self, sf, app_id, psa_usr_id):
        data = {
                self.dictionary['psa_field_name']: psa_usr_id
                }
        result = sf.App__c.update(app_id, data)
        return result

    def executive_sponsor_data(self, sf, app_id, es_usr_id):
        data = {
            self.dictionary['es_field_name']: es_usr_id
        }
        result = sf.App__c.update(app_id, data)
        return result