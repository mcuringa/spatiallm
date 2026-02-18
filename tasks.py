import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import toml
from functools import wraps
from dotenv import load_dotenv

import datetime



from invoke import task
import json


def get_project_config():
    config = {}
    with open('pyproject.toml', 'r') as f:
        config = toml.load(f)
    return config["project"]



def with_env(func):
    """Decorator to wrap a task after ENV vars are read"""
    @task
    @wraps(func)
    def wrapper(*args, **kwargs):
        load_dotenv()
        return func(*args, **kwargs)
    return wrapper


@task
def project_info(c):
    """Print project info from pyproject.toml"""
    project = get_project_config()
    print(json.dumps(project, indent=2))


@task 
def clean(c):
    """Remove dist and docs directories."""
    c.run("rm -rf dist")
    c.run("rm -rf docs")

@task
def build(c):
    """Build the package."""
    project = get_project_config()
    name = project['name']
    print(f"building {name} v{project['version']} ")
    c.run("rm -rf dist")
    c.run("python -m build")
    c.run(f"cp dist/{name}-{project['version']}.tar.gz dist/{name}-latest.tar.gz")


@with_env
def push(c, production=False):
    """Push the current distribution to pypi.
    By default, this pushes to testpypi.
    To push to pypi, use the -p or --production flag.
    """

    api_token = os.getenv("PYPI_API_TOKEN")
    print(api_token)

    project = get_project_config()
    current = f"{project['name']}-{project['version']}"
    print(current)
    if production:
        print("Pushing to pypi. This is NOT A DRILL.")
        c.run(f"twine upload dist/{current}* -u __token__ -p {api_token}")
    else:
        print("Just a dry run. Nothing done. Use --production to push to pypi.")
        

@task
def test(c, opt=""):
    """Run unit tests."""
    c.run(f"pytest {opt}")


@task
def tag(c):
    """Tag the current version."""
    project = get_project_config()
    version = project["version"]
    c.run(f"git tag -a {version} -m 'version {version}'")
    c.run(f"git push --tags")


