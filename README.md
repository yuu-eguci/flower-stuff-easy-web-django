flower-stuff-easy-web-django
===

## Requirements

- Python 3.13
- pipenv

Main packages: Django 5.2 LTS, TensorFlow 2.21 (Keras 3). `Pipfile` lists the packages the app uses directly, and `Pipfile.lock` pins everything. `requirements.txt` is generated from the lock with `pipenv requirements > requirements.txt`.

## Installation

- 🐳 flower-stuff-easy-web-docker ([https://github.com/yuu-eguci/flower-stuff-easy-web-docker](https://github.com/yuu-eguci/flower-stuff-easy-web-docker))

> [!NOTE]
> flower-stuff-easy-web-docker is archived and its container uses Python 3.8.
> It works with this repository up to commit `e14760d` (Python 3.8, Django 3.2, TensorFlow 2.6), not with later commits.

## Tests

The settings read these environment variables, so set dummy values to run the tests:

```bash
pipenv install --deploy
APP_HDF5_DRIVE_ID=dummy APP_HDF5_VERSION=dummy APP_PINCODE=dummy DJANGO_SECRET_KEY=test-only-not-secret \
    pipenv run python manage.py test
```

The tests do not need the real model. `app/tests/fixtures/legacy_model.h5` is a tiny model saved with TensorFlow 2.6.0, made by `app/tests/fixtures/make_legacy_model.py`.

## CI / Deployment

- `.github/workflows/ci.yml` runs flake8, the tests and pip-audit on pull requests and on pushes to `main`. It also checks that `requirements.txt` matches `Pipfile.lock`. It uses no secrets and has read-only permissions.
- `.github/workflows/lint-build-deploy-to-webapp.yml` deploys to Azure App Service. It runs only when started manually (`workflow_dispatch`); pushes to `main` no longer deploy. It still uses Python 3.8 and old actions, and is not maintained.
