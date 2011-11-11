#!/usr/bin/env bash

git clone git://avida.devosoft.org/avida.git
git remote set-url origin --push gitolite@avida.devosoft.org:avida-core.git

cd avida
git submodule init
git submodule update

cd avida-core
git remote set-url origin --push gitolite@avida.devosoft.org:avida-core.git

cd ../
./build_avida