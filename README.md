# database-northwind
Oppgave rundt bruk av databaser i python med bruk av django. Hensikt\
å kunne hente ut informasjon fra ulike tabeller og analysere innholdet.\
Deretter formatere det og lagre det som sql filer. 

**Libraries som må lastes ned i forkant eller underveis:**
- python 3.12.7 eller 3.13.2
- django 5.1.6
- matplotlib
- psycopg2
- tabulate
- numpy

Docker desktop eller tilsvarende vil også være nødvendig.

**Forberedelser:**\
Åpne en cmd vindu og sett opp virtual environmnet på ønsket plassering med: \
``py -m venv [virtual_environment_navn]``\
og aktiver med:\
``Srcipt\activate.bat``

Installer de ulike libraries med:\
``pip install django==5.1.6``\
``pip install psycopg2 matplotlib tabulate numpy``

start nytt django prosjekt med:\
``django-admin startproject [prosjekt_navn]`` 

i prosjekt mappen skal man se følgende:
```
[prosjekt_navn] <- mappe
manage.py
```

Lag en django-app med:\
``py manage.py [app_navn]``

Gå først til ``[prosjekt_navn]/settings.py`` og endre følgende
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
til 
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_navn'
]
```
og
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
til
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'northwind',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '55432',
    }
}
```
Last ned folderen og innholdet i ``data/northwind_psql-master`` og \
legg på samme nivå som ``[prosjekt_navn]``. Bruk docker desktop eller\
gjennom cmd og gå til innholdet i ``northwind_psql-master`` og bruk:\
``docker-compose up``

Gå tilbake til cmd vinduet som har blitt brukt så langt\
og gå inn i mappen ``[prosjekt_navn]`` og bruk:\
``py manage.py inspectdb > [app_navn]\models.py``

Gå til ``[app_navn]/admin.py`` og legg til følgende:
```
from .models import * 

admin.site.register(Categories)
admin.site.register(CustomerCustomerDemo)
admin.site.register(CustomerDemographics)
admin.site.register(Customers)
admin.site.register(EmployeeTerritories)
admin.site.register(Employees)
admin.site.register(OrderDetails)
admin.site.register(Orders)
admin.site.register(Products)
admin.site.register(Region)
admin.site.register(Shippers)
admin.site.register(Suppliers)
admin.site.register(Territories)
admin.site.register(UsStates) 
```
``from django.contrib import admin`` skal ikke fjernes.

Gå tilbake til ``[prosjekt_navn]`` mappen og bruk:\
``py manage.py makemigrations [app_navn]``\
``py manage.py migrate``

### Valgfritt
Bruk\
``py manage.py createsuperuser``\
og legg til brukernavn, email og passord for å lage admin bruker. Bruk:\
``py manage.py runserver``\
og skriv inn:\
``127.0.0.1:8000/admin/``\
i en nettleser. Man kan gå inn for å se at alt er som det skal, men er ikke nødvendig.\
For å stoppe/lukke serveren bruk:\
``ctrl + c``

På dette stadiet er oppsettet med Django ferdig. legg til mappen ``support text``,\
og filen ``help.json`` i mappen. I ``[prosjekt_navn]`` legg til ``main.py``, og mappen\
``classes``, inkludert alt innholdet som kan bli funnet fra denne github siden.
Alt skal nå være satt opp, og man kan så kjøre koden ved å bruke:\
``py main.py``

Filene i mappen ``[prosjekt_navn]`` skal være tilsvarende som:
```
- prosjekt_navn:
    - app_navn:
        - migrations:
            - __init__.py
            - 0001_initial.py
        - __init__.py
        - admin.py
        - apps.py
        - models.py
        - tests.py
        - views.py
    - classes:
        - interface:
            - query_functions.py
            - utility.py
        - base.py
        - create_sql.py
        - delivery_time.py
        - employee_analytics.py
        - product_query.py
        - sales.py
        - storage_query.py
    - prosjekt_navn:
        - __init__.py
        - asgi.py
        - settings.py
        - urls.py
        - wsgi.py
    - support text:
        - help.json
    - main.py
    - manage.py
```
