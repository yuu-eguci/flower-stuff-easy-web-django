flower-stuff-easy-web-django
===

## Installation

- 🐳 flower-stuff-easy-web-docker ([https://github.com/yuu-eguci/flower-stuff-easy-web-docker](https://github.com/yuu-eguci/flower-stuff-easy-web-docker))

## CI / Deployment

- `.github/workflows/ci.yml` runs flake8 on pull requests and on pushes to `main`. It uses no secrets and has read-only permissions.
- `.github/workflows/lint-build-deploy-to-webapp.yml` deploys to Azure App Service. It runs only when started manually (`workflow_dispatch`); pushes to `main` no longer deploy.
