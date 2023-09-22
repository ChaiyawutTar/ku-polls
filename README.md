
[![Unit Tests](https://github.com/ChaiyawutTar/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/ChaiyawutTar/ku-polls/actions/workflows/django.yml)
## KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
    on the [Django Tutorial project][django-tutorial], with
    additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Installation

Here is **[Install Instruction](Installation.md)**.

You can run with this command.

```bash
python manage.py runserver
```

Anyway, if you set `DEBUG = False` then django production server will not load static files for you.
You need to set `DEBUG = True` or run this command.

```bash
python manage.py runserver --insecure
```

Then, connect to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Demo SuperUser

|Username|Passsword|
|:--:|:--:|
|admin|admin|

## Demo User

|Username|Password|
|:--:|:--:|
|santa|Santa0818313336|
|harry|hackme|
|Peach|Peach0818313336|

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Development Plan](../../wiku/Development%20Plan)

[django-tutorial]: TODO-write-the-django-tutorial-URL-here
