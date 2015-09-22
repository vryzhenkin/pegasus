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


class MuranoDockerTestAdvanced(core.MuranoTestsCore):
    @classmethod
    def setUpClass(cls):
        super(MuranoDockerTestAdvanced, cls).setUpClass()

        cls.docker = CONF.murano.docker_image
        cls.flavor = CONF.murano.advanced_flavor

    def setUp(self):
        super(MuranoDockerTestAdvanced, self).setUp()

        self.environments = []

    def tearDown(self):
        super(MuranoDockerTestAdvanced, self).tearDown()

    def test_deploy_docker_crate_nginxsite_glassfish(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "host": self.docker_service,
            "image": 'crate',
            "name": self.rand_name("Crate"),
            "interfacePort": 4200,
            "transportPort": 4300,
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
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 4200, 4300, 80, 4848,
                                      8080, 8181)

    def test_deploy_docker_crate_nginx_mongodb(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)

        post_body = {
            "host": self.docker_service,
            "image": 'crate',
            "name": self.rand_name("Crate"),
            "interfacePort": 4200,
            "transportPort": 4300,
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
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
            "image": 'mongo',
            "name": self.rand_name("Mongo"),
            "port": 27017,
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
        self.deployment_success_check(environment, 22, 4200, 4300, 80, 27017)

    def test_deploy_docker_mariadb_postgresql_mongodb(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)

        post_body = {
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
            "image": 'mongo',
            "name": self.rand_name("Mongo"),
            "port": 27017,
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
        self.deployment_success_check(environment, 22, 3306, 5432, 27017)

    def test_deploy_docker_jenkins_httpd_mysql_phpzendserver(self):
        self.skipTest("Skipped due to removed application from repository")
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)

        post_body = {
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
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
        self.mysql = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.docker_service,
            "image": 'php-zendserver',
            "name": self.rand_name("PHP-Zend"),
            "port": 80,
            "adminPort": 10081,
            "password": self.rand_name("O5t@"),
            "publish": True,
            "database": self.mysql,
            "dbName": self.rand_name(""),
            "dbUser": self.rand_name("Us3@"),
            "dbPass": self.rand_name("P@s5"),
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker PHP-ZendServer"
                },
                "type": "io.murano.apps.docker.DockerPHPZendServer",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.deployment_success_check(environment, 22, 8080, 80, 3306,
                                      1025, 10081)

    def test_deploy_docker_redis_tomcat_influxdb(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)

        post_body = {
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
            "image": 'tutum/influxdb',
            "name": self.rand_name("Influx"),
            "interfacePort": 8083,
            "apiPort": 8086,
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
        self.deployment_success_check(environment, 22, 6379, 8080, 8083, 8086)

    def test_deploy_docker_mysql_nginxsite_redis(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)

        post_body = {
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
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

        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 3306, 80, 6379)

    @tag('light')
    def test_deploy_docker_nginx_wait_deploy_httpd(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 80)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.docker_service = self.get_service(
            environment, self.docker_service['name'])

        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 80, 1025)

    def test_deploy_docker_mysql_wait_deploy_tomcat(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 3306)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.docker_service = self.get_service(
            environment, self.docker_service['name'])

        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 3306, 8080)

    def test_deploy_docker_nginxsite_wait_deploy_mysql_phpzendserver(self):
        self.skipTest("Skipped due to removed application from repository")
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 80)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.docker_service = self.get_service(
            environment, self.docker_service['name'])

        post_body = {
            "host": self.docker_service,
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
        self.mysql = self.create_service(environment, session, post_body)

        post_body = {
            "host": self.docker_service,
            "image": 'php-zendserver',
            "name": self.rand_name("PHP-Zend"),
            "port": 80,
            "adminPort": 10081,
            "password": self.rand_name("O5t@"),
            "publish": True,
            "database": self.mysql,
            "dbName": self.rand_name(""),
            "dbUser": self.rand_name("Us3@"),
            "dbPass": self.rand_name("P@s5"),
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker PHP-ZendServer"
                },
                "type": "io.murano.apps.docker.DockerPHPZendServer",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.deployment_success_check(environment, 22, 80, 3306, 1025, 10081)

    def test_deploy_docker_tomcat_wait_deploy_mariadb(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 8080)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.docker_service = self.get_service(
            environment, self.docker_service['name'])

        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 8080, 3306)

    def test_deploy_docker_glassfish_wait_deploy_jenkins(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 4848, 8080, 8181)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.docker_service = self.get_service(
            environment, self.docker_service['name'])

        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 4848, 8080, 8181, 1025)

    def test_deploy_docker_nginx_wait_deploy_crate(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 80)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.docker_service = self.get_service(
            environment, self.docker_service['name'])

        post_body = {
            "host": self.docker_service,
            "image": 'crate',
            "name": self.rand_name("Crate"),
            "interfacePort": 4200,
            "transportPort": 4300,
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
        self.deployment_success_check(environment, 22, 80, 4200, 4300)

    def test_deploy_docker_postgresql_wait_deploy_influxdb(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 5432)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.docker_service = self.get_service(
            environment, self.docker_service['name'])

        post_body = {
            "host": self.docker_service,
            "image": 'tutum/influxdb',
            "name": self.rand_name("Influx"),
            "interfacePort": 8083,
            "apiPort": 8086,
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
        self.deployment_success_check(environment, 22, 5432, 8083, 8086)

    def test_deploy_docker_mongodb_wait_deploy_nginx(self):
        post_body = self.get_docker_app()
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "host": self.docker_service,
            "image": 'mongo',
            "name": self.rand_name("Mongo"),
            "port": 27017,
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
        self.deployment_success_check(environment, 22, 27017)
        environment = self.get_environment(environment)
        session = self.create_session(environment)
        self.docker_service = self.get_service(
            environment, self.docker_service['name'])

        post_body = {
            "host": self.docker_service,
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
        self.deployment_success_check(environment, 22, 27017, 80)