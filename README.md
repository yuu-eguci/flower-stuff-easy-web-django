flower-stuff-easy-web-django
===

## Installation

- 🐳 flower-stuff-easy-web-docker ([https://github.com/yuu-eguci/flower-stuff-easy-web-docker](https://github.com/yuu-eguci/flower-stuff-easy-web-docker))

## Tests

The settings read these environment variables, so set dummy values to run the tests:

```bash
pipenv install --deploy
APP_HDF5_DRIVE_ID=dummy APP_HDF5_VERSION=dummy APP_PINCODE=dummy DJANGO_SECRET_KEY=test-only-not-secret \
    pipenv run python manage.py test
```

The tests do not need the real model. `app/tests/fixtures/legacy_model.h5` is a tiny model saved with TensorFlow 2.6.0, made by `app/tests/fixtures/make_legacy_model.py`.

## CI / Deployment

- `.github/workflows/ci.yml` runs flake8 and the tests on pull requests and on pushes to `main`. It uses no secrets and has read-only permissions.
- `.github/workflows/lint-build-deploy-to-webapp.yml` deploys to Azure App Service. It runs only when started manually (`workflow_dispatch`); pushes to `main` no longer deploy.
