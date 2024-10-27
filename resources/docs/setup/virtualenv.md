# Virtual Environment Setup

## Instructions

Navigate to your installation directory.

**Suggested:** ```/opt/apps/insrt```

```bash
virtualenv ./venv
. ./venv/bin/activate
pip install pipenv
pipenv lock
pipenv install
```