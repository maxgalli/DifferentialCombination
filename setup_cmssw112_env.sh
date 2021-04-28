#!/bin/bash

install_dir=$1
if [[ -z $install_dir ]]; then
    echo "usage: $0 <install_dir>"
    exit -1
fi

if [[ -z "${PYTHONPATH}" ]]; then
    export PYTHONPATH="${install_dir}/lib/python/"
else
    export PYTHONPATH="$PYTHONPATH:${install_dir}/lib/python/"
fi

export PATH=$PATH:"${install_dir}/bin/"
