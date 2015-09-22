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

    @tag('light')
    def test_deploy_k8s_influx_grafana(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
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
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 8083, 8086, 80]
                           ], kubernetes=True)

    def test_deploy_k8s_mongodb(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Mongo"),
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker MongoDB"
                },
                "type": "io.murano.apps.docker.DockerMongoDB",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 27017]
                           ], kubernetes=True)

    def test_deploy_k8s_nginx(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'nginx',
            "name": self.rand_name("Nginx"),
            "port": 80,
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker Nginx"
                },
                "type": "io.murano.apps.docker.DockerNginx",
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

    def test_deploy_k8s_glassfish(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'tutum/glassfish',
            "name": self.rand_name("Glass"),
            "password": self.rand_name("O5t@"),
            "adminPort": 4848,
            "httpPort": 8080,
            "httpsPort": 8181,
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker GlassFish"
                },
                "type": "io.murano.apps.docker.DockerGlassFish",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 4848, 8080]
                           ], kubernetes=True)

    def test_deploy_k8s_mariadb(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'tutum/mariadb',
            "name": self.rand_name("MariaDB"),
            "port": 3306,
            "password": self.rand_name("O5t@"),
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker MariaDB"
                },
                "type": "io.murano.apps.docker.DockerMariaDB",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 3306]
                           ], kubernetes=True)

    def test_deploy_k8s_mysql(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'mysql',
            "name": self.rand_name("MySQL"),
            "port": 3306,
            "password": self.rand_name("O5t@"),
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker MySQL"
                },
                "type": "io.murano.apps.docker.DockerMySQL",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 3306]
                           ], kubernetes=True)

    def test_deploy_k8s_jenkins(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'jenkins',
            "name": self.rand_name("Jenkins"),
            "port": 8080,
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker Jenkins"
                },
                "type": "io.murano.apps.docker.DockerJenkins",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 8080]
                           ], kubernetes=True)

    def test_deploy_k8s_postgresql(self):
        self.skipTest('Unstable')
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'postgres',
            "name": self.rand_name("Postgres"),
            "port": 5432,
            "password": self.rand_name("O5t@"),
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker PostgreSQL"
                },
                "type": "io.murano.apps.docker.DockerPostgreSQL",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 5432]
                           ], kubernetes=True)

    def test_deploy_k8s_crate(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

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

    def test_deploy_k8s_redis(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'redis',
            "name": self.rand_name("Redis"),
            "port": 6379,
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker Redis"
                },
                "type": "io.murano.apps.docker.DockerRedis",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 6379]
                           ], kubernetes=True)

    def test_deploy_k8s_tomcat(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "image": 'tutum/tomcat',
            "name": self.rand_name("Tomcat"),
            "port": 8080,
            "password": self.rand_name("O5t@"),
            "publish": True,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker Tomcat"
                },
                "type": "io.murano.apps.docker.DockerTomcat",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 8080]
                           ], kubernetes=True)

    def test_deploy_k8s_httpd(self):
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

    def test_deploy_k8s_httpd_site(self):
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
            "siteRepo": "https://github.com/gabrielecirulli/2048.git",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker HTTPd"
                },
                "type": "io.murano.apps.docker.DockerHTTPdSite",
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

    def test_deploy_k8s_nginx_site(self):
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
                           [self.cluster['name'], "gateway-1", 80]
                           ], kubernetes=True)
