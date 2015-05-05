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

import config as cfg
import muranomanager as core
import time

CONF = cfg.cfg.CONF


class MuranoKubeTest(core.MuranoTestsCore):
    @classmethod
    def setUpClass(cls):
        super(MuranoKubeTest, cls).setUpClass()

        cls.kubernetes = CONF.murano.kubernetes_image
        cls.flavor = CONF.murano.standard_flavor

    def setUp(self):
        super(MuranoKubeTest, self).setUp()

        self.environments = []

    def tearDown(self):
        super(MuranoKubeTest, self).tearDown()

    def test_deploy_k8s_influx_grafana(self):
        post_body = {
            "gatewayCount": 1,
            "gatewayNodes": [
                {
                    "instance": {
                        "name": self.rand_name("gateway-1"),
                        "assignFloatingIp": True,
                        "keyname": self.keyname,
                        "flavor": self.flavor,
                        "image": self.kubernetes,
                        "?": {
                            "type": "io.murano.resources.LinuxMuranoInstance",
                            "id": str(uuid.uuid4())
                        }
                    },
                    "?": {
                        "type": "io.murano.apps.docker.kubernetes.KubernetesGatewayNode",
                        "id": str(uuid.uuid4())
                    }
                }
            ],
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Kubernetes Cluster"
                },
                "type": "io.murano.apps.docker.kubernetes.KubernetesCluster",
                "id": str(uuid.uuid4())
            },
            "nodeCount": 1,
            "dockerRegistry": "",
            "masterNode": {
                "instance": {
                    "availabilityZone": "nova",
                    "name": self.rand_name("master-1"),
                    "assignFloatingIp": True,
                    "keyname": self.keyname,
                    "flavor": self.flavor,
                    "image": self.kubernetes,
                    "?": {
                        "type": "io.murano.resources.LinuxMuranoInstance",
                        "id": str(uuid.uuid4())
                    }
                },
                "?": {
                    "type": "io.murano.apps.docker.kubernetes.KubernetesMasterNode",
                    "id": str(uuid.uuid4())
                }
            },
            "minionNodes": [
                {
                    "instance": {
                        "name": self.rand_name("minion-1"),
                        "assignFloatingIp": True,
                        "keyname": self.keyname,
                        "flavor": self.flavor,
                        "image": self.kubernetes,
                        "?": {
                            "type": "io.murano.resources.LinuxMuranoInstance",
                            "id": str(uuid.uuid4())
                        }
                    },
                    "?": {
                        "type": "io.murano.apps.docker.kubernetes.KubernetesMinionNode",
                        "id": str(uuid.uuid4())
                    },
                    "exposeCAdvisor": True
                }
            ],
            "name": self.rand_name("KubeCluster")
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)

        post_body = {
            "kubernetesCluster": self.cluster,
            "labels": "testkey=testvalue",
            "name": self.rand_name("pod"),
            "replicas": 0,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Kubernetes Pod"
                },
                "type": "io.murano.apps.docker.kubernetes.KubernetesPod",
                "id": str(uuid.uuid4())
            }
        }
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Influx"),
            "preCreateDB": 'db1;db2',
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker InfluxDB"
                },
                "type": "io.murano.apps.docker.DockerInfluxDB",
                "id": str(uuid.uuid4())
            }
        }
        self.influx_service = self.create_service(environment, session,
                                                  post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Grafana"),
            "influxDB": self.influx_service,
            "grafanaUser": self.rand_name("user"),
            "grafanaPassword": self.rand_name("pass"),
            "dbName": self.rand_name("base"),
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker Grafana"
                },
                "type": "io.murano.apps.docker.DockerGrafana",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 22, 8080],
                           [self.cluster['name'], "minion-1", 22, 4194],
                           [self.cluster['name'], "gateway-1", 22, 8083, 8086, 80]
                           ], kubernetes=True)