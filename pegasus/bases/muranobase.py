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


import socket
import time
import random
import json
import logging
import telnetlib
import uuid

import yaml
import requests
import testresources
import testtools
import muranoclient.common.exceptions as exceptions

from etc import config as cfg
from pegasus.common import clients

CONF = cfg.cfg.CONF

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
fh = logging.FileHandler('runner.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
fh.setFormatter(formatter)
LOG.addHandler(fh)


class MuranoTestsCore(testtools.TestCase, testtools.testcase.WithAttributes,
                      testresources.ResourcedTestCase, clients.OsClients):
    """This manager provides access to Murano-api service."""

    @classmethod
    def setUpClass(cls):
        super(MuranoTestsCore, cls).setUpClass()

        cfg.load_config()
        cls.murano_url = cls._get_endpoint(service_type='application_catalog',
                                            endpoint_type='publicURL')
        cls.murano_endpoint = cls.murano_url + '/v1/'
        cls.keyname = CONF.murano.keyname
        cls.availability_zone = CONF.murano.availability_zone

    @classmethod
    def upload_package(cls, package_name, body, app, ):
        files = {'%s' % package_name: open(app, 'rb')}
        return cls.murano.packages.create(body, files)

    def setUp(self):
        super(MuranoTestsCore, self).setUp()
        self.keystone = self._get_auth()
        self.heat = self.get_heat_client(self.keystone)
        self.murano = self.get_murano_client(self.keystone)
        self.headers = {'X-Auth-Token': self.murano.auth_token,
                        'content-type': 'application/json'}

        self.environments = []
        LOG.debug('Running test: {0}'.format(self._testMethodName))

    def tearDown(self):
        super(MuranoTestsCore, self).tearDown()
        for env in self.environments:
            try:
                self.environment_delete(env)
                self.purge_stacks(env)
                time.sleep(10)
            except Exception:
                pass

    @classmethod
    def rand_name(cls, name='murano_env'):
        return name + str(random.randint(1, 0x7fffffff))

    def environment_delete(self, environment_id, timeout=180):
        try:
            self.murano.environments.delete(environment_id)
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    self.murano.environments.get(environment_id)
                except exceptions.HTTPNotFound:
                    return
            raise exceptions.HTTPOverLimit(
                'Environment {0} was not deleted in {1} seconds'.format(
                    environment_id, timeout))
        except (exceptions.HTTPForbidden, exceptions.HTTPOverLimit):
            self.murano.environments.delete(environment_id, abandon=True)
            LOG.warning('Environment {0} from test {1} abandoned'.format(
                environment_id, self._testMethodName))

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.murano.environments.get(environment_id)
            except exceptions.HTTPNotFound:
                return
        raise Exception(
            'Environment {0} was not deleted in {1} seconds'.format(
                environment_id, timeout))

    def wait_for_environment_deploy(self, environment):
        start_time = time.time()
        status = environment.manager.get(environment.id).status
        while status != 'ready':
            status = environment.manager.get(environment.id).status
            if time.time() - start_time > 1800:
                time.sleep(60)
                self._log_report(environment)
                self.fail(
                    'Environment deployment is not finished in 1200 seconds')
            elif status == 'deploy failure':
                self._log_report(environment)
                time.sleep(60)
                self.fail('Environment has incorrect status {0}'.format(status))
            time.sleep(5)
        LOG.debug('Environment {0} is ready'.format(environment.name))
        return environment.manager.get(environment.id)

    def check_port_access(self, ip, port, negative=False):
        result = 1
        start_time = time.time()
        while time.time() - start_time < 600:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((str(ip), port))
            sock.close()

            if result == 0 or negative:
                break
            time.sleep(5)
        if negative:
            self.assertNotEqual(0, result, '%s port is opened on instance' % port)
        else:
            self.assertEqual(0, result, '%s port is closed on instance' % port)

    def check_k8s_deployment(self, ip, port, timeout=3600, negative=False):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                LOG.debug('Checking: {0}:{1}'.format(ip, port))
                self.verify_connection(ip, port, negative)
                return
            except RuntimeError as e:
                time.sleep(10)
                LOG.debug(e)
        self.fail('Containers are not ready')

    def verify_connection(self, ip, port, negative=False):
        try:
            tn = telnetlib.Telnet(ip, port)
            tn.write('GET / HTTP/1.0\n\n')
            buf = tn.read_all()
            LOG.debug('Data:\n {0}'.format(buf))
            if negative and len(buf) == 0:
                LOG.debug('Port negative test in action.')
                return
            elif len(buf) != 0:
                tn.sock.sendall(telnetlib.IAC + telnetlib.NOP)
                return
            else:
                raise RuntimeError('Resource at {0}:{1} not exist'.
                                   format(ip, port))
        except socket.error as e:
            LOG.debug('Found reset: {0}'.format(e))

    def deployment_success_check(self, environment, *ports):
        """
        :param environment:
        :param ports:
        """
        deployment = self.murano.deployments.list(environment.id)[-1]

        self.assertEqual('success', deployment.state,
                         'Deployment status is {0}'.format(deployment.state))

        ip = environment.services[0]['instance']['floatingIpAddress']

        if ip:
            for port in ports:
                self.check_port_access(ip, port)
        else:
            self.fail('Instance does not have floating IP')

    def status_check(self, environment, configurations, kubernetes=False,
                     negative=False):
        """
        Function which gives opportunity to check multiple instances
        :param environment: Murano environment
        :param configurations: Array of configurations.
        :param kubernetes: Used for parsing multiple instances in one service
               False by default.
        Example: [[instance_name, *ports], [instance_name, *ports]] ...
        Example k8s: [[cluster['name'], instance_name, *ports], [...], ...]
        """
        for configuration in configurations:
            if kubernetes:
                service_name = configuration[0]
                LOG.debug('Service: {0}'.format(service_name))
                inst_name = configuration[1]
                LOG.debug('Instance: {0}'.format(inst_name))
                ports = configuration[2:]
                LOG.debug('Acquired ports: {0}'.format(ports))
                ip = self.get_k8s_ip_by_instance_name(environment, inst_name,
                                                      service_name)
                if ip and ports and negative:
                    for port in ports:
                        self.check_port_access(ip, port, negative)
                        self.check_k8s_deployment(ip, port, negative)
                elif ip and ports:
                    for port in ports:
                        self.check_port_access(ip, port)
                        self.check_k8s_deployment(ip, port)
                else:
                    self.fail('Instance does not have floating IP')
            else:
                inst_name = configuration[0]
                ports = configuration[1:]
                ip = self.get_ip_by_instance_name(environment, inst_name)
                if ip and ports:
                    for port in ports:
                        self.check_port_access(ip, port)
                else:
                    self.fail('Instance does not have floating IP')

    def get_ip_by_appname(self, environment, appname):
        """
        Returns ip of instance with a deployed application using
        application name
        :param environment: Murano environment
        :param appname: Application name or substring of application name
        :return:
        """
        for service in environment.services:
            if appname in service['name']:
                return service['instance']['floatingIpAddress']

    def get_ip_by_instance_name(self, environment, inst_name):
        """
        Returns ip of instance using instance name
        :param environment: Murano environment
        :param name: String, which is substring of name of instance or name of
        instance
        :return:
        """
        for service in environment.services:
            if inst_name in service['instance']['name']:
                return service['instance']['floatingIpAddress']

    def get_k8s_ip_by_instance_name(self, environment, inst_name, service_name):
        """
        Returns ip of specific kubernetes node (gateway, master, minion) based.
        Search depends on service name of kubernetes and names of spawned
        instances
        :param environment: Murano environment
        :param inst_name: Name of instance or substring of instance name
        :param service_name: Name of Kube Cluster application in Murano
        environment
        :return: Ip of Kubernetes instances
        """
        for service in environment.services:
            if service_name in service['name']:
                if "gateway" in inst_name:
                    for gateway in service['gatewayNodes']:
                        if inst_name in gateway['instance']['name']:
                            LOG.debug(gateway['instance']['floatingIpAddress'])
                            return gateway['instance']['floatingIpAddress']
                elif "master" in inst_name:
                    LOG.debug(service['masterNode']['instance'][
                        'floatingIpAddress'])
                    return service['masterNode']['instance'][
                        'floatingIpAddress']
                elif "minion" in inst_name:
                    for minion in service['minionNodes']:
                        if inst_name in minion['instance']['name']:
                            LOG.debug(minion['instance']['floatingIpAddress'])
                            return minion['instance']['floatingIpAddress']

    def create_env(self):
        name = self.rand_name('MuranoTe')
        environment = self.murano.environments.create({'name': name})
        self.environments.append(environment.id)
        LOG.debug('Created Environment:\n {0}'.format(environment))
        return environment

    def create_session(self, environment):
        return self.murano.sessions.configure(environment.id)

    def delete_session(self, environment, session):
        return self.murano.sessions.delete(environment.id, session.id)

    def add_service(self, environment, data, session):
        """
        This function adding a specific service to environment
        Returns a specific class <Service>
        :param environment:
        :param data:
        :param session:
        :return:
        """

        LOG.debug('Added service:\n {0}'.format(data))
        return self.murano.services.post(environment.id,
                                         path='/', data=data,
                                         session_id=session.id)

    def create_service(self, environment, session, json_data):
        """
        This function adding a specific service to environment
        Returns a JSON object with a service
        :param environment:
        :param session:
        :param json_data:
        :return:
        """
        LOG.debug('Added service:\n {0}'.format(json_data))
        headers = self.headers.copy()
        headers.update({'x-configuration-session': session.id})
        endpoint = '{0}environments/{1}/services'.format(self.murano_endpoint,
                                                         environment.id)
        return requests.post(endpoint, data=json.dumps(json_data),
                             headers=headers).json()

    def delete_service(self, environment, session, service):
        LOG.debug('Removed service: {0}'.format(service.name))
        self.murano.services.delete(
            environment.id, path='/{0}'.format(self.get_service_id(service)),
            session_id=session.id)
        updated_env = self.get_environment(environment)
        return updated_env

    def deploy_environment(self, environment, session):
        self.murano.sessions.deploy(environment.id, session.id)
        return self.wait_for_environment_deploy(environment)

    def get_environment(self, environment):
        return self.murano.environments.get(environment.id)

    def get_service(self, environment, service_name, to_json=True):
        for service in self.murano.services.list(environment.id):
            if service.name == service_name and to_json:
                service = service.to_dict()
                service = json.dumps(service)
                return yaml.load(service)
            elif service.name == service_name:
                return service

    def get_service_id(self, service):
        #TODO(freerunner): Rework this part after service object will have an id attribute
        env_service = service.to_dict()
        s_id = env_service['?']['id']
        return s_id

    def _quick_deploy(self, name, *apps):
        environment = self.murano.environments.create({'name': name})
        self.environments.append(environment.id)

        session = self.murano.sessions.configure(environment.id)

        for app in apps:
            self.murano.services.post(environment.id,
                                      path='/',
                                      data=app,
                                      session_id=session.id)

        self.murano.sessions.deploy(environment.id, session.id)

        return self.wait_for_environment_deploy(environment)

    def _get_stack(self, environment_id):

        for stack in self.heat.stacks.list():
            if environment_id in stack.description:
                return stack

    def purge_stacks(self, environment_id):
        stack = self._get_stack(environment_id)
        if not stack:
            return
        else:
            self.heat.stacks.delete(stack.id)

    def check_path(self, env, path, inst_name=None):
        environment = env.manager.get(env.id)
        if inst_name:
            ip = self.get_ip_by_instance_name(environment, inst_name)
        else:
            ip = environment.services[0]['instance']['floatingIpAddress']
        resp = requests.get('http://{0}/{1}'.format(ip, path))
        if resp.status_code == 200:
            pass
        else:
            self.fail("Service path unavailable")

    # TODO: Add function to check that environment removed.

    def get_last_deployment(self, environment):
        deployments = self.murano.deployments.list(environment.id)
        return deployments[0]

    def get_deployment_report(self, environment, deployment):
        history = ''
        report = self.murano.deployments.reports(environment.id, deployment.id)
        for status in report:
            history += '\t{0} - {1}\n'.format(status.created, status.text)
        return history

    def _log_report(self, environment):
        deployment = self.get_last_deployment(environment)
        details = deployment.result['result']['details']
        LOG.error('Exception found:\n {0}'.format(details))
        report = self.get_deployment_report(environment, deployment)
        LOG.debug('Report:\n {0}\n'.format(report))

    @classmethod
    def get_docker_app(cls):
        body = {
            "instance": {
                "name": cls.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": cls.keyname,
                "flavor": cls.flavor,
                "image": cls.docker,
                "availabilityZone": cls.availability_zone,
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
                "type": "io.murano.apps.docker.DockerStandaloneHost",
                "id": str(uuid.uuid4())
            }
        }
        return body

    @classmethod
    def get_k8s_app(cls):
        body = {
            "gatewayCount": 1,
            "gatewayNodes": [
                {
                    "instance": {
                        "name": cls.rand_name("gateway-1"),
                        "assignFloatingIp": True,
                        "keyname": cls.keyname,
                        "flavor": cls.flavor,
                        "image": cls.kubernetes,
                        "availabilityZone": cls.availability_zone,
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
                    "name": cls.rand_name("master-1"),
                    "assignFloatingIp": True,
                    "keyname": cls.keyname,
                    "flavor": cls.flavor,
                    "image": cls.kubernetes,
                    "availabilityZone": cls.availability_zone,
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
                        "name": cls.rand_name("minion-1"),
                        "assignFloatingIp": True,
                        "keyname": cls.keyname,
                        "flavor": cls.flavor,
                        "image": cls.kubernetes,
                        "availabilityZone": cls.availability_zone,
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
            "name": cls.rand_name("KubeCluster")
        }
        return body

    @classmethod
    def get_k8s_pod(cls, cluster, replicas, labels):
        body = {
            "kubernetesCluster": cluster,
            "labels": labels,
            "name": cls.rand_name("pod"),
            "replicas": replicas,
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Kubernetes Pod"
                },
                "type": "io.murano.apps.docker.kubernetes.KubernetesPod",
                "id": str(uuid.uuid4())
            }
        }
        return body
