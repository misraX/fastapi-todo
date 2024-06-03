Tools used:

- pre-commit
  - conventional-pre-commit
  - ruff
- pipenv

Project Structure:

```text
├── app/
│   ├── user/
│   │   ├── api/
│   │   │   └── __init__.py
│   │   ├── model/
│   │   │   └── __init__.py
│   │   ├── schema/
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── todo/
│   │   ├── api/
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   └── __init__.py
│   │   └── __init__.py
│   └── __init__.py
├── core/
│   ├── db/
│   │   └── __init__.py
│   ├── settings/
│   │   └── __init__.py
│   ├── schema/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── user/
│   │   └── __init__.py
│   ├── todo/
│   │   └── __init__.py
│   └── __init__.py
├── .env
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── main.py
```
