## Index
1. [Installation](#installation)
2. [Running the project](#running-the-project)
    1. [Accessing a container](#accessing-a-container)
4. [Other useful commands](#other-useful-commands)

## Installation
### Main Project

- Install [Docker](https://www.docker.com/products/overview)
  and [Docker Compose](https://docs.docker.com/compose/install/)
  
Note: `compose` is now part of the Docker CLI and you can skip installing `docker-compose` and instead use `docker compose` (without the hyphen) in all the following commands.

- `$ docker-compose build`

## Running the project

Run Docker development server

- `$ docker-compose up`

### Accessing a container

You can access shell in a container

- `$ docker exec -i -t <CONTAINER_NAME_OR_ID> /bin/bash`

E.g.

- `$ docker ps # get the name from the list of running containers`
- `$ docker exec -i -t acmessangeerbackend-app-1  /bin/bash`

## Other useful commands

- `$ docker kill $(docker ps -q) # stop all docker containers`
- `$ docker rm $(docker ps -a -q) # remove all docker containers`
- `$ docker rmi $(docker images -q) # remove all docker images`
- `$ docker exec -i -t  acmessangeerbackend-app-1  python src/manage.py makemigrations # make migrations`
- `$ docker exec -i -t  acmessangeerbackend-app-1  python src/manage.py migrate # run migrations`

## API Access
`http://localhost:8000/`