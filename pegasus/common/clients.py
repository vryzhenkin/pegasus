from muranoclient import client as muranoclient
from heatclient import client as heatclient

import pegasus.common.auth as auth


class OsClients(auth.BasicAuth):
    keystone = auth.BasicAuth._get_auth()

    @classmethod
    def get_murano_client(cls):
        murano_endpoint = cls._get_endpoint(service_type='application_catalog',
                                            endpoint_type='publicURL')
        murano = muranoclient.Client('1', endpoint=murano_endpoint,
                                     token=cls.keystone.auth_token)
        return murano

    @classmethod
    def get_heat_client(cls):
        heat_endpoint = cls._get_endpoint(service_type='orchestration',
                                          endpoint_type='publicURL')
        heat = heatclient.Client('1', endpoint=heat_endpoint,
                                 token=cls.keystone.auth_token)
        return heat
