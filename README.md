# Snack Bar - Face Recognition
## Prerequisites
- [Python Version: v3.6.4](https://www.python.org/downloads/release/python-364/) 
- [Pipenv Version: latest](http://pipenv.readthedocs.io/en/latest/)
- [ageitgey/face_recognition](https://github.com/ageitgey/face_recognition#installation-options) P.S. Remember to install dlib
- Camera for Client
- Please set the server/client as the project root directory in the IDE/deployment environment.

### Install dependency by pipenv for DEV
Enter the `server` or `client` folder to run below commands to installing the dependency for each part.
``` bash
# Please ENUSRE python3-dev had been installed

# install the virtual enviroment with dependency from Pipfile*
# dlib a C++ lib, a face_recognition requried lib, need a long time to compile
pipenv install
# check th dependency in Pipfile
pipenv graph

# enter virtual environment
pipenv shell
```


## Development
1. Start a mongodb locally
2. Start a Redis locally
3. Update the config for each part. (the `local` section on config.ini, etc.)

### Client
Run below commands.
```bash
pipenv shell
# for windows, default env is DEV, all server point to Hyman's
set env=local 
# for Unix-like, default env is DEV, all server point to Hyman's
export env=local
python client.py
```

### Server
1. Update `/etc/hosts` in Unix-Like or `%systemdrive%\Windows\System32\drivers\etc` in Windows to append below record. (Services' names mapping in the docker-compose.yml, for unifying the server config)
  - `<mongo_service_ip> face_rec_mongo`
  - `<redis_service_ip> face_rec_redis`
  - `<server_service_ip> face_rec_server`


## Deployment
### Client
Refer to [#Development](#Development)

### Server
Refer to the `snack_bar/.gitlab-ci.yml`, using `Docker` to standarize the deployment flow and environment.
- `Dockerfile-base` for building docker image with fixed dependency, such as `face_recognition`, `dlib`
- `Dockerfile-server` for building server app docker image 
- `docker-compose.yml` for composing the services

## Tests
### Client
1. Execute `coverage run test.py` in folder `snack_bar/client/` to run all tests for  client.
2. There will be a file `.coverage` generated to the `client/`, execute `converage report` to check the coverage.

### Server
TBC

## Structure
TBC
