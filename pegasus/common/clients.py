from muranoclient import client as muranoclient
from heatclient import client as heatclient

import os

import pegasus.common.auth as auth


class OsClients(auth.BasicAuth):

    @classmethod
    def get_murano_client(cls, auth_client=None):
        keystone = auth_client if auth_client else cls._get_auth()
        murano_endpoint = cls._get_endpoint(service_type='application_catalog',
                                            endpoint_type='publicURL')

        if auth.BasicAuth.http:
            murano = muranoclient.Client('1', endpoint=murano_endpoint,
                                         token=keystone.auth_token,
                                         )
            return murano
        else:
            murano = muranoclient.Client('1', endpoint=murano_endpoint,
                                         token=keystone.auth_token,
                                         cacert=auth.BasicAuth.cert_path,
                                         )
            return murano

    @classmethod
    def get_heat_client(cls, auth_client=None):
        keystone = auth_client if auth_client else cls._get_auth()
        heat_endpoint = cls._get_endpoint(service_type='orchestration',
                                          endpoint_type='publicURL')
        if auth.BasicAuth.http:
            heat = heatclient.Client('1', endpoint=heat_endpoint,
                                     token=keystone.auth_token)
            return heat
        else:
            heat = heatclient.Client('1', endpoint=heat_endpoint,
                                     token=keystone.auth_token,
                                     cacert=auth.BasicAuth.cert_path,)
            return heat
