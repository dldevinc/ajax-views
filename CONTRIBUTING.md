# Contribution

## Development

### Setup

1. Make sure you have [pipx](https://pipx.pypa.io/stable/installation/) installed.
1. Install [poetry](https://python-poetry.org/docs/#installation)
   ```shell
   pipx install poetry
   ```
1. Install [nox](https://nox.thea.codes/en/stable/tutorial.html#installation)
   ```shell
   pipx install nox
   ```

1. Clone the repository:
   ```shell
   git clone https://github.com/dldevinc/ajax-views
   ```
1. Navigate to the project root directory:
   ```shell
   cd ajax-views
   ```
1. Install python dependencies:
   ```shell
   poetry install
   ```1. Install Django without modifying `poetry.lock` file:
   ```shell
   poetry run pip install django
   ```1. Run test project
   ```shell
   python3 manage.py migrate
   python3 manage.py loaddata tests/fixtures.json
   python3 manage.py runserver
   ```
   > Django admin credentials: `admin` / `admin`

### Formatting

To run `black`, `isort` and `flake8`:

```shell
nox -Rt style fix
```

### Testing

To run unit tests:

```shell
nox -Rt test
```
