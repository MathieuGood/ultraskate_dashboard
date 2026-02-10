# UltraskateDashboard

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Install

For webscraping features, you may need to install playwright

``` bash
uv run python -m playwright install
```

## API

```bash
# Start the server in development mode (auto-reload and pre-loading events)
uv run uvicorn api.app:app --reload
```

**API server URL** : <http://localhost:8000>
**Swagger UI**: <http://localhost:8000/docs>
**ReDoc**: <http://localhost:8000/redoc>
