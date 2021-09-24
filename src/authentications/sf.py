from simple_salesforce import Salesforce


def sf_auth(username_salesforce, password_salesforce, security_token, client_id, domain):
    sf = Salesforce(username=username_salesforce, password=password_salesforce, security_token=security_token,
                    client_id=client_id, domain=domain)
    return sf