#!/usr/bin/env bash

mode="$1"

USER_NAME=$(whoami)

if [ ${USER_NAME}==root ]; then
    CWD=/root
else
    CWD=/home/${USER_NAME}
fi

PEGASUS_DIR=${CWD}/pegasus

MURANO_TESTS_DIR=${PEGASUS_DIR}/pegasus/tests/murano/

source ${PEGASUS_DIR}/tools/prepare_tests.sh

source ${PEGASUS_DIR}/.venv/bin/activate

case ${mode} in
    *light*)
    nosetests -v --with-openstack --openstack-show-elapsed --openstack-color \
    --with-html-output --html-out-file=${PEGASUS_DIR}/pegasus_results.html \
    --with-xunit --xunit-file=${PEGASUS_DIR}/pegasus_results.xml -a light ${MURANO_TESTS_DIR}
    ;;
    *full*)
    nosetests -v --with-openstack --openstack-show-elapsed --openstack-color \
    --with-html-output --html-out-file=${PEGASUS_DIR}/pegasus_results.html \
    --with-xunit --xunit-file=${PEGASUS_DIR}/pegasus_results.xml ${MURANO_TESTS_DIR}
    ;;
esac

RETVAL=$?

deactivate

exit ${RETVAL}