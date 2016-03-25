# Copyright (c) 2016 Mirantis, Inc.
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

from etc import config as cfg
from pegasus.bases import muranobase as core

CONF = cfg.cfg.CONF


class TestKubeSimple(core.MuranoTestsCore):
    @classmethod
    def setUpClass(cls):
        super(TestKubeSimple, cls).setUpClass()

        cls.kubernetes = CONF.murano.kubernetes_image
        cls.flavor = CONF.murano.standard_flavor

    def setUp(self):
        super(TestKubeSimple, self).setUp()

        self.environments = []

    def tearDown(self):
        super(TestKubeSimple, self).tearDown()

    def test_k8s_add_action_nodesup(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'nginx',
            "name": self.rand_name("NginxS"),
            "port": 80,
            "siteRepo": 'https://github.com/gabrielecirulli/2048.git',
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker Nginx Site"
                },
                "type": "io.murano.apps.docker.DockerNginxSite",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 80],
                           ], kubernetes=True)
        environment = self.get_environment(environment)
        action_id = self.get_action_id(environment, 'scaleNodesUp')
        # TODO: Need to add action properties to run_action func to define
        # body of action arguments
        arguments = {}
        self.run_action(environment, action_id, arguments)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "minion-2", 4194],
                           [self.cluster['name'], "gateway-1", 80],
                           ], kubernetes=True)

    def test_k8s_add_action_gatewaysup(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'httpd',
            "name": self.rand_name("HTTPd"),
            "port": 80,
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker HTTPd"
                },
                "type": "io.murano.apps.docker.DockerHTTPd",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 80]
                           ], kubernetes=True)
        environment = self.get_environment(environment)
        action_id = self.get_action_id(environment, 'scaleGatewaysUp')
        # TODO: Need to add action properties to run_action func to define
        # body of action arguments
        arguments = {}
        self.run_action(environment, action_id, arguments)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 80],
                           [self.cluster['name'], "gateway-2", 80]
                           ], kubernetes=True)
