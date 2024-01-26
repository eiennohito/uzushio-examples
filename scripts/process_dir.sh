#!/bin/env bash

process_dir() {
    pushd $PWD
    cd "$1"
    python3 ~/work/uzushio-examples/scripts/extract.py *.gz
    popd
}

find . -mindepth 1 -maxdepth 1 -type d -print0 | while IFS= read -r -d $'\0' file;
do
    # echo "$file"
    process_dir $(readlink -f "$file")
done