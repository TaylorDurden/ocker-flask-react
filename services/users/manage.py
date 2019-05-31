# _*_ coding: utf-8 _*_
# !/usr/bin/env python3

from flask.cli import FlaskGroup
import unittest
from project import create_app, db
from project.api.models import User
import coverage
import os

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


# def __run_env():
#     os.system('export FLASK_APP=project/__init__.py')
#     os.system('export FLASK_ENV=development')
#     os.system('export APP_SETTINGS=project.config.DevelopmentConfig')
#     os.system(
#         'export DATABASE_URL=postgres://postgres:postgres@localhost:5432/users_dev')
#     os.system(
#         'export DATABASE_TEST_URL=postgres://postgres:postgres@localhost-db:5435/users_test')
#     os.system(
#         'python manage.py run -h 0.0.0.0')


@cli.command('recreate_db')
def recreate_db():
    # __run_env()
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('recreate_db success.')


@cli.command()
def test():
    """Runs the tests without code coverage"""
    # __run_env()
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    # __run_env()
    taylor = User(username='taylor', email="taylor@gmail.com")
    jack = User(username='jack', email="jack@163.org")
    db.session.add(taylor)
    db.session.add(jack)
    jack.follow(taylor)

    db.session.commit()


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    # __run_env()
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@cli.command()
def start():
    """ python manage.py start """
    # __run_env()
    # os.system('export FLASK_APP=project/__init__.py')
    # os.system('export FLASK_ENV=development')
    # os.system('export APP_SETTINGS=project.config.DevelopmentConfig')
    # os.system(
    #     'export DATABASE_URL=postgres://postgres:postgres@localhost:5432/users_dev')
    # os.system(
    #     'export DATABASE_TEST_URL=postgres://postgres:postgres@localhost-db:5435/users_test')
    # os.system(
    #     'python manage.py run -h 0.0.0.0')


if __name__ == '__main__':
    cli()
