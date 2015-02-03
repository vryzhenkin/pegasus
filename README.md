# docker-murano-tests
This test-suite created for testing Docker Applications in Murano on MOX.
In future it will be used by Murano Team for testing Docker Applications in murano kilo-release.

# How to run

You need to install requirements.txt and configure config.conf.
Please remember, murano_url should ends by port, not by a version.

You can use nosetests to run tests directly.

    pip install nose

For high priority sanity test cases you need to run test_deploy_docker.py

    nosetests -sv test_deploy_docker.py

Running single test from test-suite

    nosetests -sv test_deploy_docker.py:MuranoDockerTest.test_deploy_docker_redis

For high priority advanced test cases you need to use test_deploy_docker_advanced.py

    nosetests -sv test_deploy_docker_advanced.py

Now, we still working under medium priority advanced test cases. ETA is 3.02.2015
