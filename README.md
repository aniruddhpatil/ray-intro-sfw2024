# Introduction to Ray

This is a quick setup repository to get your own local environment running.

## Instructions

### Pre-requisites
1. `docker`
2. `docker-compose`
3. `make`

### How to setup

1. Once you clone the repository update the `docker/Dockerfile.ray` base image to use the exact version of Python to be used. \
   It should look like this if you use Python 3.11 \
   \
   `FROM rayproject/ray:2.9.2-py311 as base`  
  
   
2. Run `pip install -r docker/requirements.txt` to get all the libraries requried. 

   Don't forget to setup a virtual environment to keep your Python installation clean.



3. Just run `make all` and get started!
