#!/usr/bin/env bash

USER_NAME=$(whoami)

if [ ${USER_NAME}==root ]; then
    CWD=/root
else
    CWD=/home/${USER}
fi

PEGASUS_DIR=${CWD}/pegasus

MURANO_TESTS_DIR=${PEGASUS_DIR}/pegasus/tests/murano/

source ${PEGASUS_DIR}/tools/prepare_tests.sh

source ${VIRTUALENV_DIR}/bin/activate

nosetests -v --with-openstack --openstack-show-elapsed --openstack-color \
--with-html-output --html-out-file=${PEGASUS_DIR}/pegasus_results.html \
--with-xunit --xunit-file=${PEGASUS_DIR}/pegasus_results.xml ${MURANO_TESTS_DIR}

deactivate