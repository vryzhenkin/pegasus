import os

from keystoneclient.v2_0 import client as keystoneclient

from etc import config as cfg

CONF = cfg.cfg.CONF


class BasicAuth(object):
    @staticmethod
    def _get_auth():
        username = os.environ.get('OS_USERNAME')
        password = os.environ.get('OS_PASSWORD')
        tenant_name = os.environ.get('OS_TENANT_NAME')
        uri = os.environ.get('OS_AUTH_URL')

        if cfg.load_config():
            username = username or CONF.murano.user
            password = password or CONF.murano.password
            tenant_name = tenant_name or CONF.murano.tenant
            uri = uri or CONF.murano.auth_url

        def get_keystone_client():
            keystone = keystoneclient.Client(username=username,
                                             password=password,
                                             tenant_name=tenant_name,
                                             auth_url=uri)
            return keystone

        return get_keystone_client()

    @classmethod
    def _get_endpoint(cls, service_type, endpoint_type):
        keystone = cls._get_auth()
        endpoint = \
            keystone.service_catalog.url_for(service_type=service_type,
                                             endpoint_type=endpoint_type)
        return endpoint
