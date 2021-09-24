# Hello everyone.

## Some words about it project.
This project is being developed by me as an educational one. And there may be something not implemented at the proper level or should be done in a way (approach). Thank you for your attention.

# Technologies used

## Backend

![python](https://img.shields.io/badge/Python3-yellow?style=for-the-badge&logo=python)
![django](https://img.shields.io/badge/Django-00a328?style=for-the-badge&logo=django)
![django-rest-framework](https://img.shields.io/badge/DRF-c70d00?style=for-the-badge&logo=django)
![celery](https://img.shields.io/badge/Celery-a6ff00c70d00?style=for-the-badge&logo=celery) 

## Database

![postgres](https://img.shields.io/badge/Postgres-282438?style=for-the-badge&logo=postgresql)

## Tools

![Docker](https://img.shields.io/badge/Docker-160d91?style=for-the-badge&logo=Docker)
![Postman](https://img.shields.io/badge/Postman-dba240?style=for-the-badge&logo=postman)

![Git](https://img.shields.io/badge/GIT-black?style=for-the-badge&logo=git)
![GitHub](https://img.shields.io/badge/github-292621?style=for-the-badge&logo=github)

![VScode](https://img.shields.io/badge/VSCode-blue?style=for-the-badge&logo=visual-studio-code)

# The essence of the project and what it is.

## This is a simple e-commerce project. Which provide basic e-commerce functionality.

### Some features that can be highlighted.

+ Customer
  + Customer user model which based by AbstactUser.
  + It has CustomerManager which base by BaseUser Manager
  + Username field replaced by email field. It's login for a customer.
  + When a new customer is created, a shopping cart is created for him. And when you delete a customer, his cart is deleted. This is all implemented using django signals.
+ Item
  + When an item is created, it is associated with the requestor cart using a generic foreignkey relationship.
  + When the order is placed. This item is associated with the created order through the field that was associated with the cart.
+ Order
  + When an order is created, it is linked through a foreign key to the customer creating the order.
+ Product
  + The category model was created using the django-mptt library.
  + It is possible to add an unlimited number of images for products. This is implemented using a foreign key relationship from the Image model to the Product model.

# A few of my explanatory words about this project. 

## This project is being developed (developed) in Python version 3 on the framework django and django-rest-freamework and related technologies (django-mppt, django-filter, djoser and etc).

## Development process

### In this project, I tried to stick to the MVC style. And where more than CRUD is needed, I added a services layer in which I implemented all the processing of input data and the issuance of serialized objects.

___

### I hope it didn't work out. 

![mem](https://www.meme-arsenal.com/memes/b97a97429274113ed382a1cfa179d9d9.jpg)