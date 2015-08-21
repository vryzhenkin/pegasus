#!/usr/bin/env bash

source ${PEGASUS_DIR}/tools/init_env_variables.sh

install_system_requirements() {
    message "Enable default CentOS repo"
    yum -y reinstall centos-release

    message "Installing system requirements"
    yum -y install git
    yum -y install gcc
    yum -y install python-devel
    yum -y install zlib-devel
    yum -y install readline-devel
    yum -y install bzip2-devel
    yum -y install libgcrypt-devel
    yum -y install openssl-devel
    yum -y install libffi-devel
    yum -y install libxml2-devel
    yum -y install libxslt-devel
}

install_python27_pip_virtualenv() {
    message "Installing Python 2.7"
    if command -v python2.7 &>/dev/null; then
        message "Python 2.7 already installed!"
    else
        local temp_dir="$(mktemp -d)"
        cd ${temp_dir}
        wget ${PYTHON_LOCATION}
        tar xzf Python-${PYTHON_VERSION}.tgz
        cd Python-${PYTHON_VERSION}
        ./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
        make -j5 altinstall

        message "Installing pip and virtualenv for Python 2.7"
        local get_pip_file="$(mktemp)"
        wget -O ${get_pip_file} ${PIP_LOCATION}
        python2.7 ${get_pip_file}
        pip2.7 install -U tox
    fi
}

install_system_requirements
install_python27_pip_virtualenv

cd ${PEGASUS_DIR}

python ${PEGASUS_DIR}/tools/install_venv.py

source ${PEGASUS_DIR}/.venv/bin/activate

source ${PEGASUS_DIR}/openrc

murano bundle-import --is-public --exists-action s app-servers
murano bundle-import --is-public --exists-action s container-based-apps
murano bundle-import --is-public --exists-action s monitoring
murano bundle-import --is-public --exists-action s databases
murano package-import --is-public --exists-action s io.murano.apps.WordPress

deactivate
