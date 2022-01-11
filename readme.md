# Hello everyone.

## Some words about this project.

I wrote a pretty big API that has a lot of features. I tried to implement many things that small and medium stores have. Maybe it wasn't exactly what I thought it would be, or maybe you don't think I did what I thought it would be. Possibly. But I did what seemed right to me at the time.

I tried very hard to write code that was close to industrial projects and write readable code with docstrings.

The project has a layer called services which implements the database via ORM, and this layer is where all the business logic is. The view layer is the controller layer which accepts requests, redirects them to the services layer, and sends out responses with the data generated in the services layer.

I also used a library like Celery for pending tasks like sending emails to customers' emails. And I used docker/docker-compose for easy startup and testing.

I didn't write the integration of the payment system because, without fronted, it doesn't make any sense to me to implement this system. To be honest, I tried to do it, but it didn't work. And I didn't plan to write the fronted part. But there is a blueprint or simulation of this system in the project, but it is just there as a "plug".

About the tests. I tried to write at least some tests. But I think that they are not written in a proper way and not in a proper amount, but I will try in the next projects to cover as much code with quality tests as possible

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