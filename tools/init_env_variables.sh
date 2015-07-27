#!/bin/bash

USER_NAME="${USER_NAME:-developer}"
USER_HOME_DIR="/home/${USER_NAME}"
DEST="${USER_HOME_DIR}/pegasus"
VIRTUALENV_DIR="${DEST}/.venv"
PEGASUS_REPORTS_DIR="${DEST}/"

PYTHON_VERSION="${PYTHON_VERSION:-2.7.9}"
PYTHON_LOCATION="https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz"

PIP_LOCATION="https://raw.github.com/pypa/pip/master/contrib/get-pip.py"