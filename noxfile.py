import nox


DJANGO_VERSIONS = {
    "3.9": ["3.2", "4.0", "4.1", "4.2"],
    "3.10": ["3.2", "4.0", "4.1", "4.2", "5.0", "5.1"],
    "3.11": ["4.1", "4.2", "5.0", "5.1"],
    "3.12": ["4.2", "5.0", "5.1"],
    "3.13": ["5.1"],
}


@nox.session(tags=["style", "fix"])
def black(session):
    session.install("black")
    session.run("black", "ajax_views", "tests")


@nox.session(tags=["style", "fix"])
def isort(session):
    session.install("isort")
    session.run("isort", "ajax_views", "tests")


@nox.session(tags=["style"])
def flake8(session):
    session.install("flake8", "flake8-pyproject")
    session.run("flake8", "ajax_views")


@nox.session(tags=["test"])
@nox.parametrize(
    "python,django",
    [
        nox.param(python, django, tags=[f"django-{django}"])
        for python, django_versions in DJANGO_VERSIONS.items()
        for django in django_versions
    ],
)
def pytest(session, django):
    session.install("poetry")
    session.run_install("poetry", "install", "--with", "pytest")
    session.run_install("poetry", "run", "pip", "install", f"django~={django}.0")
    session.run("poetry", "run", "python3", "manage.py", "migrate")
    session.run("poetry", "run", "pytest", "--cov")
