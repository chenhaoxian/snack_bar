#!/bin/bash

# update package apt source to use mirror
sed -i '1i deb mirror://mirrors.ubuntu.com/mirrors.txt precise main restricted universe multiverse' /etc/apt/sources.list 
sed -i '1i deb mirror://mirrors.ubuntu.com/mirrors.txt precise-updates main restricted universe multiverse' /etc/apt/sources.list 
sed -i '1i deb mirror://mirrors.ubuntu.com/mirrors.txt precise-backports main restricted universe multiverse' /etc/apt/sources.list 
sed -i '1i deb mirror://mirrors.ubuntu.com/mirrors.txt precise-security main restricted universe multiverse' /etc/apt/sources.list 

# install_docker_update_packages
sudo apt-get update -y

# install_docker_dependency
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# install_docker_add_gpg_key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# install_docker_add_gpg_key_fingerprint
sudo apt-key fingerprint 0EBFCD88

# install_docker_enable_stable_repos
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# install_docker_install
sudo apt-get update -y && sudo apt-get install -y docker-ce

# install_docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# verification
sudo docker version
docker-compose --version
