# database-northwind
## røff skisse
oppgave rundt database i python med bruk av django

krever:
``python 3.12.7``\
``django 5.1.6``\
``numpy``\
``matplotlib``\
``tabulate``\

sett opp virtual environmnet med 

``py -m venv [prosjektnavn]``

installer de ulike libraries nevnt ovenfor.
start nytt django prosjekt med 

``django-admin startproject [navn]`` 

legg koden inn i prosjekt mappen. 
lag en app ved bruk av 

``py manage.py startapp [navn]``

og legg koden fra application inn app mappen. 
installer docker, og bruk 

``docker-compose up`` 

på northwind.sql filen. bruk så

``py manage.py inspectdb``
``py manage.py inspectdb > models.py``

deretter bruk

``py manage.py makemigrations [app-navn]``
``py manage.py migrate``

legg inn resten av filene. Bruk for å kjøre koden 

``py main.py``
