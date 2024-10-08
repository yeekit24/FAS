# FAS
Financial Assistance Scheme Management System

This project is tested on ARM x64(Mac OS/linux) architecture, will support Window in future.

## Prequisties:
- docker
- docker compose
For more info, visit `https://docs.docker.com/engine/install/`

## Technologies Stack:
- Docker
- Python 3.8
- Postgres 16.4
- Django
- Django Rest Framework
- Django-YASG
- Pre-commit

## How to start this
1. git clone this repository into your local drive. You should able to locate env.example file in the repository. Rename `env.example` to `.env` in your local repository.

2. Run the following command to start the application.
```bash
$ docker compose up --build
```

## Repository Guide:
- `src` - contains the source code of the application
- `docs` - contains the POSTMAN collection for the API
- `requirements` -  contains the dependencies of the application
- `compose` - contains the docker setup file of the application
- `config` - contains the configuration of the application.

Under `compose` and `requirements`, we separate the config file into local and prod for different configuration/requirements(eg: local development can have superuser while production we do not recommended that)

## Documentation:
### Swagger:
You can visit `http://localhost:8000/v1/api/specs/swagger/` for the available API endpoints
If you want to test the API with swagger, put `Bearer 123` after you click Authorize.

### Postman:
Locate postman collection under your local repository `{{PROJECT_DIR}}/docs/FAS.postman_collection.json`

### Admin Panel:
visit `http://localhost:8000/adm1n/` to access the admin panel. You can use the following credentials to login.
```
    Username: admin
    Password: 123
```

## Authorization and Authentication:
We are using admin user to authenticate and authorization API access.
For advanced security, we can create a new user in admin panel, with control over which API endpoint can be accessed.

## CI/CD hook:
Before you did any code changes, please make sure you have run the following command to check the code syntax.
```bash
$ pre-commit run --all-files
```
