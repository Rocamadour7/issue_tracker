# Issue Tracker
App for tracking issues of a github repository, using Django.

### Requirements
* Django 2.0.1
* Social-Auth Django 2.1.0

*Check [requirements.txt](requirements.txt) for all the dependencies.*

### Usage
1. Clone the repository
2. Create a virtual environments and active it. *Optional*
3. Clone the .env.example and rename it .env, fill it with the relevant data.
4. Install requirements by `pip install -r requirements.txt`
5. Run `python manage.py makemigrations` to create the migrations files.
6. Run `python manage.py migrate` to create the database and to copy the models structure.
7. Run `python manage.py createsuperuser` to create a Super User to get access to the admin site. *Optional*
8. Run `python manage.py runserver` to run the server, and access it in `localhost:8000`.

![alt-text][img_1]

![alt-text][img_2]

![alt-text][img_3]

![alt-text][img_4]

![alt-text][img_5]

[img_1]: images/img_01.PNG
[img_2]: images/img_02.PNG
[img_3]: images/img_03.PNG
[img_4]: images/img_04.PNG
[img_5]: images/img_05.PNG