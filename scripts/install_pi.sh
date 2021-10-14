#!/bin/bash
# install_raspberry_pi.sh

echo "Installing base dependencies"
sudo apt-get update
sudo apt-get install -y ffmpeg mpg321 \
    libsm6 libxext6 python3-pip python3-pip \
    libatlas-base-dev python3-h5py libgtk2.0-dev libgtk-3-0 \
    libilmbase-dev libopenexr-dev libgstreamer1.0-dev \
    gnustep-gui-runtime

if grep -q 'env/' .gitignore ; then /bin/true ; else echo 'env/' >> .gitignore ; fi

python3 -m pip install virtualenv

echo "Activating project virtual environment in $PWD/env"
# note - if installing python10 (non-default python3?), may need --system-site-packages (or pip can't find module pip??)
python3 -m virtualenv -p python3 env
. env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r src/requirements.txt
