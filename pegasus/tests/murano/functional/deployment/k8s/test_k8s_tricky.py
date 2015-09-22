# Copyright (c) 2015 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import uuid

from nose.plugins.attrib import attr as tag

from etc import config as cfg
from pegasus.bases import muranobase as core

CONF = cfg.cfg.CONF

class TestKubeTricky(core.MuranoTestsCore):
    @classmethod
    def setUpClass(cls):
        super(TestKubeTricky, cls).setUpClass()

        cls.kubernetes = CONF.murano.kubernetes_image
        cls.flavor = CONF.murano.standard_flavor

    def setUp(self):
        super(TestKubeTricky, self).setUp()

        self.environments = []

    def tearDown(self):
        super(TestKubeTricky, self).tearDown()

    def test_k8s_app_removal(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Nginx"),
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker Nginx"
                },
                "type": "io.murano.apps.docker.DockerNginx",
                "id": str(uuid.uuid4())
            }
        }
        nginx = self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 80]
                           ], kubernetes=True)

        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.pod = self.get_service(environment, self.pod['name'])
        service_for_removal = self.get_service(environment, nginx['name'],
                                               to_json=False)
        environment = self.delete_service(environment, session,
                                          service_for_removal)
        post_body = {
            "host": self.pod,
            "name": self.rand_name("Crate"),
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker Crate"
                },
                "type": "io.murano.apps.docker.DockerCrate",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 4200]
                           ], kubernetes=True)
        self.status_check(environment,
                          [[self.cluster['name'], "gateway-1", 80]],
                          kubernetes=True, negative=True)