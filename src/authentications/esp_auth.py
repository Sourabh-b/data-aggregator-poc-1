from esp.auth.sts_auth import SecuredTrustServiceAuth


def authentication(username, password, sts_uri, instance):
    """
    :param username: generic user id
    :param password: generic user password
    :param sts_uri: sts base uri to connect with esp(based on env[stage/prod])
    :param instance: domain
    :return: session
    """
    sts_auth = SecuredTrustServiceAuth(sts_uri=sts_uri, instance=instance,
                                       ws_user=username, ws_password=password)
    return sts_auth
