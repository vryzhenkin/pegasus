    def test_deploy_docker_nginx_wait_deploy_httpd(self):
        post_body = {
            "instance": {
                "name": self.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": "",
                "flavor": "m1.large",
                "image":
                    "Ubuntu14.04 x64 (pre-installed murano agent and docker)",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
            },
            "name": "DockerVM",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker VM Service"
                },
                "type": "io.murano.apps.docker.DockerSingleVMServer50",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "docker": self.docker_service,
            "image": 'nginx',
            "name": self.rand_name("Nginx"),
            "port": 80,
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
        self.deployment_success_check(environment, 22, 1025)
        session = self.create_session(environment)

        post_body = {
            "docker": self.docker_service,
            "image": 'httpd',
            "name": self.rand_name("HTTPd"),
            "port": 80,
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
        self.deployment_success_check(environment, 22, 1025, 1026)

    def test_deploy_docker_mysql_wait_deploy_tomcat(self):
        post_body = {
            "instance": {
                "name": self.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": "",
                "flavor": "m1.large",
                "image":
                    "Ubuntu14.04 x64 (pre-installed murano agent and docker)",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
            },
            "name": "DockerVM",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker VM Service"
                },
                "type": "io.murano.apps.docker.DockerSingleVMServer50",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "docker": self.docker_service,
            "image": 'mysql',
            "name": self.rand_name("MySQL"),
            "port": 3306,
            "password": self.rand_name("O5t@"),
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
        self.deployment_success_check(environment, 22, 1025)
        session = self.create_session(environment)

        post_body = {
            "docker": self.docker_service,
            "image": 'tutum/tomcat',
            "name": self.rand_name("Tomcat"),
            "port": 8080,
            "password": self.rand_name("O5t@"),
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
        self.deployment_success_check(environment, 22, 1025, 1026)

    def test_deploy_docker_nginxsite_wait_deploy_phpzendserver(self):
        post_body = {
            "instance": {
                "name": self.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": "",
                "flavor": "m1.large",
                "image":
                    "Ubuntu14.04 x64 (pre-installed murano agent and docker)",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
            },
            "name": "DockerVM",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker VM Service"
                },
                "type": "io.murano.apps.docker.DockerSingleVMServer50",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "docker": self.docker_service,
            "image": 'nginx',
            "name": self.rand_name("NginxS"),
            "port": 80,
            "url": 'http://github.com/???',
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
        self.deployment_success_check(environment, 22, 1025)
        session = self.create_session(environment)

        post_body = {
            "docker": self.docker_service,
            "image": 'php-zendserver',
            "name": self.rand_name("PHP-Zend"),
            "port": 80,
            "portAdmin": 10081,
            "password": self.rand_name("O5t@"),
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
        self.deployment_success_check(environment, 22, 1025, 1026, 1027)

    def test_deploy_docker_tomcat_wait_deploy_mariadb(self):
        post_body = {
            "instance": {
                "name": self.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": "",
                "flavor": "m1.large",
                "image":
                    "Ubuntu14.04 x64 (pre-installed murano agent and docker)",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
            },
            "name": "DockerVM",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker VM Service"
                },
                "type": "io.murano.apps.docker.DockerSingleVMServer50",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "docker": self.docker_service,
            "image": 'tutum/tomcat',
            "name": self.rand_name("Tomcat"),
            "port": 8080,
            "password": self.rand_name("O5t@"),
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
        self.deployment_success_check(environment, 22, 1025)
        session = self.create_session(environment)

        post_body = {
            "docker": self.docker_service,
            "image": 'tutum/mariadb',
            "name": self.rand_name("MariaDB"),
            "port": 3306,
            "password": self.rand_name("O5t@"),
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
        self.deployment_success_check(environment, 22, 1025, 1026)

    def test_deploy_docker_glassfish_wait_deploy_jenkins(self):
        post_body = {
            "instance": {
                "name": self.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": "",
                "flavor": "m1.large",
                "image":
                    "Ubuntu14.04 x64 (pre-installed murano agent and docker)",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
            },
            "name": "DockerVM",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker VM Service"
                },
                "type": "io.murano.apps.docker.DockerSingleVMServer50",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "docker": self.docker_service,
            "image": 'tutum/glassfish',
            "name": self.rand_name("Glass"),
            "password": self.rand_name("O5t@"),
            "portAdmin": 4848,
            "portHTTP": 8080,
            "portHTTPS": 8181,
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
        self.deployment_success_check(environment, 22, 1025, 1026, 1027)
        session = self.create_session(environment)

        post_body = {
            "docker": self.docker_service,
            "image": 'jenkins',
            "name": self.rand_name("Jenkins"),
            "port": 8080,
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
        self.deployment_success_check(environment, 22, 1025, 1026, 1027, 1028)

    def test_deploy_docker_nginx_wait_deploy_crate(self):
        post_body = {
            "instance": {
                "name": self.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": "",
                "flavor": "m1.large",
                "image":
                    "Ubuntu14.04 x64 (pre-installed murano agent and docker)",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
            },
            "name": "DockerVM",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker VM Service"
                },
                "type": "io.murano.apps.docker.DockerSingleVMServer50",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "docker": self.docker_service,
            "image": 'nginx',
            "name": self.rand_name("Nginx"),
            "port": 80,
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
        self.deployment_success_check(environment, 22, 1025)
        session = self.create_session(environment)

        post_body = {
            "docker": self.docker_service,
            "image": 'crate',
            "name": self.rand_name("Crate"),
            "port4200": 4200,
            "port4300": 4300,
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
        self.deployment_success_check(environment, 22, 1025, 1026, 1027)

    def test_deploy_docker_postgresql_wait_deploy_influxdb(self):
        post_body = {
            "instance": {
                "name": self.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": "",
                "flavor": "m1.large",
                "image":
                    "Ubuntu14.04 x64 (pre-installed murano agent and docker)",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
            },
            "name": "DockerVM",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker VM Service"
                },
                "type": "io.murano.apps.docker.DockerSingleVMServer50",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "docker": self.docker_service,
            "image": 'postgres',
            "name": self.rand_name("Postgres"),
            "port": 5432,
            "password": self.rand_name("O5t@"),
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker PostgreSQL"
                },
                "type": "io.murano.apps.docker.DockerPostgres",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.deployment_success_check(environment, 22, 1025)
        session = self.create_session(environment)

        post_body = {
            "docker": self.docker_service,
            "image": 'tutum/influxdb',
            "name": self.rand_name("Influx"),
            "port": 8083,
            "portAPI": 8086,
            "preCreateDB": 'db1;db2',
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
        self.deployment_success_check(environment, 22, 1025, 1026, 1027)

    def test_deploy_docker_mongodb_wait_deploy_nginx(self):
        post_body = {
            "instance": {
                "name": self.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": "",
                "flavor": "m1.large",
                "image":
                    "Ubuntu14.04 x64 (pre-installed murano agent and docker)",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
            },
            "name": "DockerVM",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker VM Service"
                },
                "type": "io.murano.apps.docker.DockerSingleVMServer50",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.docker_service = self.create_service(environment, session,
                                                  post_body)
        post_body = {
            "docker": self.docker_service,
            "image": 'mongo',
            "name": self.rand_name("Mongo"),
            "port": 27017,
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
        self.deployment_success_check(environment, 22, 1025)
        self.delete_session(environment, session)
        session = self.create_session(environment)

        post_body = {
            "docker": self.docker_service,
            "image": 'nginx',
            "name": self.rand_name("Nginx"),
            "port": 80,
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
        self.deployment_success_check(environment, 22, 1025, 1026)