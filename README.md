# docker-flask-react
# Microservices with Docker, Flask, and React

[![Build Status](https://travis-ci.com/TaylorDurden/docker-flask-react.svg?branch=master)](https://travis-ci.org/TaylorDurden/docker-flask-react)

#flask-migrate

1.docker-compose -f docker-compose-dev.yml exec users python manage.py db init # for the 1st time
2.docker-compose -f docker-compose-dev.yml exec users python manage.py db migrate -m "xxx"
3.docker-compose -f docker-compose-dev.yml exec users python manage.py db upgrade