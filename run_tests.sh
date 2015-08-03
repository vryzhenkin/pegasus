#!/usr/bin/env bash

mode="$1"

script_dir() {
    cwd=${PWD}
    scr_dir=$(dirname "$BASH_SOURCE")
    cd ${scr_dir}
    full_dir_name=${PWD}
    cd ${cwd}
    echo ${full_dir_name}
}

PEGASUS_DIR=$(script_dir)

source ${PEGASUS_DIR}/tools/init_env_variables.sh

if [ ! -f ${PEGASUS_DIR}/openrc ]; then
    error "openrc file not found. Exiting."
    message "Please, put your openrc to top directory of Pegasus"
    exit 1
fi

if [[ -z ${mode} ]]; then
    message "Looks like you started tests without mode."
    echo "You can start a light test-run using './run_tests.sh light.'"
    echo "Or if you want to perform full run, you need to use './run_tests.sh full'"
    exit 1
fi

MURANO_TESTS_DIR=${PEGASUS_DIR}/pegasus/tests/murano/

source ${PEGASUS_DIR}/tools/prepare_tests.sh

source ${PEGASUS_DIR}/.venv/bin/activate

case ${mode} in
    *light*)
    message "Running Murano tests in light mode"
    nosetests -v --with-openstack --openstack-show-elapsed --openstack-color \
    --with-html-output --html-out-file=${PEGASUS_DIR}/pegasus_results.html \
    --with-xunit --xunit-file=${PEGASUS_DIR}/pegasus_results.xml -a light ${MURANO_TESTS_DIR}
    ;;
    *full*)
    message "Running Murano tests in full mode"
    nosetests -v --with-openstack --openstack-show-elapsed --openstack-color \
    --with-html-output --html-out-file=${PEGASUS_DIR}/pegasus_results.html \
    --with-xunit --xunit-file=${PEGASUS_DIR}/pegasus_results.xml ${MURANO_TESTS_DIR}
    ;;
esac

RETVAL=$?

deactivate

exit ${RETVAL}