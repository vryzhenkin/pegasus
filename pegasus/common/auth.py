import os
import logging

from keystoneclient.v2_0 import client as keystoneclient

from etc import config as cfg

CONF = cfg.cfg.CONF

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
fh = logging.FileHandler('runner.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
fh.setFormatter(formatter)
LOG.addHandler(fh)


class BasicAuth(object):

    http = True

    #if used https download haproxy.pem
    cert_path = os.environ.get('OS_CACERT')

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

            try:
                keystone = keystoneclient.Client(username=username,
                                                 password=password,
                                                 tenant_name=tenant_name,
                                                 auth_url=uri)
            except Exception as e:
                if 'Authorization Failed' in str(e):

                    LOG.warning('Trying HTTPS')
                    LOG.debug('HTTP failed exception: {0}, trying HTTPS'.format(e))

                    try:
                        keystone = keystoneclient.Client(username=username,
                                                         password=password,
                                                         tenant_name=tenant_name,
                                                         auth_url=uri,
                                                         cacert=BasicAuth.cert_path)
                    except Exception as e:
                        if 'Authorization Failed' in str(e):
                            LOG.debug('Invalid URL or invalid cert for HTTPS: {0}'.format(e))
                            exit(1)
                    else:
                        LOG.warning('Get keystone by HTTPS is OK')
                        BasicAuth.HTTP = False
                        return keystone
                pass

            else:
                LOG.warning('Get keystone by HTTP is OK')
                return keystone

        return get_keystone_client()

    @classmethod
    def _get_endpoint(cls, service_type, endpoint_type):
        keystone = cls._get_auth()
        endpoint = \
            keystone.service_catalog.url_for(service_type=service_type,
                                             endpoint_type=endpoint_type,
                                             )
        return endpoint
