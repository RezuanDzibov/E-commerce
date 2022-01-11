# Hello everyone.

## Some words about this project.

This project is a kind of summation of my knowledge that I have acquired. 
And I tried to implement this knowledge in this project. 
But their implementation does not claim to be "best practice".

# Technologies used

## Backend

![python](https://img.shields.io/badge/Python3-yellow?style=for-the-badge&logo=python)
![django](https://img.shields.io/badge/Django-00a328?style=for-the-badge&logo=django)
![django-rest-framework](https://img.shields.io/badge/DRF-c70d00?style=for-the-badge&logo=django)
![celery](https://img.shields.io/badge/Celery-a6ff00c70d00?style=for-the-badge&logo=celery) 

## Database

![postgres](https://img.shields.io/badge/Postgres-282438?style=for-the-badge&logo=postgresql)
![redis](https://img.shields.io/badge/Reids-FFFFFF?style=for-the-badge&logo=redis)

## Tools

![docker](https://img.shields.io/badge/Docker-160d91?style=for-the-badge&logo=Docker)
![docker-compose](https://img.shields.io/badge/Docker_compose-160d91?style=for-the-badge&logo=docker)
![postman](https://img.shields.io/badge/Postman-dba240?style=for-the-badge&logo=postman)

![git](https://img.shields.io/badge/GIT-black?style=for-the-badge&logo=git)
![gitHub](https://img.shields.io/badge/github-292621?style=for-the-badge&logo=github)

## Before you start this project, you should make sure that you have docker and docker-compose installed and fill out the .env file. Here are the fields you need to fill in: 

```
SECRET_KEY
DEBUG
DJANGO_ALLOWED_HOSTS
SQL_ENGINE
SQL_USER
SQL_PASSWORD
SQL_DATABASE
SQL_HOST
SQL_PORT
DATABASE
EMAIL_BACKEND
EMAIL_HOST
EMAIL_USE_TLS
EMAIL_PORT
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
CELERY_BROKER
CELERY_BACKEND
```

## And if so, you can clone the repository and run the project with the command:
```
docker-compose up --build
```
## And now the project should be up and running. If there will be errors connecting to the database (that the database on port 5432 is not found), this is how it works. 
<br>

## After you run docker-compose, an admin account will be created from init_admin.json fixture.
```
Email: admin@gmail.com
Password: admin
```

# Thank you for your attention.