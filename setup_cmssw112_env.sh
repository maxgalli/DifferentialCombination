#!/bin/bash

install_dir=$1
if [[ -z $install_dir ]]; then
    echo "usage: $0 <install_dir>"
    exit -1
fi

if [[ -z "${PYTHONPATH}" ]]; then
    export PYTHONPATH="${install_dir}/lib/python2.7/site-packages"
else
    export PYTHONPATH="$PYTHONPATH:${install_dir}/lib/python2.7/site-packages"
fi

export PATH=$PATH:"${install_dir}/bin/"
