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


class TestKubeAdvanced(core.MuranoTestsCore):
    @classmethod
    def setUpClass(cls):
        super(TestKubeAdvanced, cls).setUpClass()

        cls.kubernetes = CONF.murano.kubernetes_image
        cls.flavor = CONF.murano.standard_flavor

    def setUp(self):
        super(TestKubeAdvanced, self).setUp()

        self.environments = []

    def tearDown(self):
        super(TestKubeAdvanced, self).tearDown()

    def test_k8s_deploy_docker_crate_nginxsite_glassfish(self):
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

        post_body = {
            "host": self.pod,
            "name": self.rand_name("NginxS"),
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

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Glass"),
            "password": self.rand_name("O5t@"),
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
                           [self.cluster['name'], "gateway-1", 4200, 80,
                            4848, 8080]
                           ], kubernetes=True)

    def test_k8s_deploy_docker_crate_nginx_mongodb(self):
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
        self.create_service(environment, session, post_body)

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
                           [self.cluster['name'], "gateway-1", 4200, 80, 27017]
                           ], kubernetes=True)

    def test_k8s_deploy_mariadb_postgresql_mongodb(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("MariaDB"),
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

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Postgres"),
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
                           [self.cluster['name'], "gateway-1", 3306, 27017]
                           ], kubernetes=True)

    def test_k8s_deploy_redis_tomcat_influxdb(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Redis"),
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

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Tomcat"),
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

        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 6379, 8080,
                            8083, 8086]
                           ], kubernetes=True)

    def test_k8s_deploy_mysql_nginxsite_redis(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("MySQL"),
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

        post_body = {
            "host": self.pod,
            "name": self.rand_name("NginxS"),
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

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Redis"),
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
                           [self.cluster['name'], "gateway-1", 3306, 80, 6379]
                           ], kubernetes=True)

    @tag('light')
    def test_k8s_deploy_mysql_wait_deploy_tomcat(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("MySQL"),
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
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.pod = self.get_service(environment, self.pod['name'])

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Tomcat"),
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
                           [self.cluster['name'], "gateway-1", 3306, 8080]
                           ], kubernetes=True)

    @tag('light')
    def test_k8s_deploy_nginx_wait_deploy_httpd_multipod(self):
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
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 80]
                           ], kubernetes=True)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.cluster = self.get_service(environment,
                                                self.cluster['name'])
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod2 = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod2,
            "name": self.rand_name("HTTPd"),
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
                           [self.cluster['name'], "gateway-1", 80, 1025]
                           ], kubernetes=True)

    def test_k8s_deploy_tomcat_wait_deploy_mariadb(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Tomcat"),
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
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.pod = self.get_service(environment, self.pod['name'])

        post_body = {
            "host": self.pod,
            "name": self.rand_name("MariaDB"),
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
                           [self.cluster['name'], "gateway-1", 3306, 8080]
                           ], kubernetes=True)

    def test_k8s_deploy_glassfish_wait_deploy_jenkins_multipod(self):
        post_body = self.get_k8s_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.cluster = self.create_service(environment, session, post_body)
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod,
            "name": self.rand_name("Glass"),
            "password": self.rand_name("O5t@"),
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
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.cluster = self.get_service(environment,
                                                self.cluster['name'])
        post_body = self.get_k8s_pod(self.cluster, 0, "testkey=testvalue")
        self.pod2 = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.pod2,
            "name": self.rand_name("Jenkins"),
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
                           [self.cluster['name'], "gateway-1", 4848, 8080, 1025]
                           ], kubernetes=True)

    def test_k8s_deploy_nginx_wait_deploy_crate(self):
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
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 80]
                           ], kubernetes=True)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.pod = self.get_service(environment, self.pod['name'])

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
                           [self.cluster['name'], "gateway-1", 80, 4200]
                           ], kubernetes=True)

    def test_k8s_deploy_mongodb_wait_deploy_nginx(self):
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
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.pod = self.get_service(environment, self.pod['name'])

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
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.status_check(environment,
                          [[self.cluster['name'], "master-1", 8080],
                           [self.cluster['name'], "minion-1", 4194],
                           [self.cluster['name'], "gateway-1", 80, 27017]
                           ], kubernetes=True)