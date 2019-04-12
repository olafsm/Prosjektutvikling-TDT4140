<img src="Gruppe52/staticfiles/media/logo/pinterest_board_photo.png" height="250">

## Matega [![pipeline status](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-52/badges/master/build.svg)](https://gitlab.com/programvareutvikling-v19/gruppe-52/commits/master)[![pipeline status](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-52/badges/master/coverage.svg)](https://gitlab.com/programvareutvikling-v19/gruppe-52/commits/master)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Tenk deg at du sitter med mye mat i kjøleskapet ditt som du ikke aner hva du skal bruke 
ingrediensene til. Mange har et problem med å ende opp med å lage den enklest mulige matretten. Dette er en medvirkende faktor i Norge sitt store matsvinn-problem, og vi vil være et fremtredende firma når det gjelder bærekraft og miljøproblemer.

Vi ønsker oss en plattform der man kan fylle inn ingrediensene man har, slik at plattformen automagisk finner de mest passende oppskriftene. Disse oppskriftene skal være laget av kokker og ha kvalitetsstempler. I tillegg ønsker vi at brukere skal kunne vurdere oppskriftene de har laget.

Nettsiden finnes på [matega.eu](http://matega.eu). 

Mer informasjon og brukermanual finner du på [wiki-siden](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-52/wikis/home).

## Dev setup
*  Last ned siste versjon av [Docker Desktop](https://www.docker.com/products/docker-desktop) (Kun macOS, linux og Windows 10 Pro/Education)
*  Installer [git](https://git-scm.com/downloads)

```shell
# Clone fra GitLab
$ git clone https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-52.git
```
### Med docker 
```shell
# CD til prosjektmappen
$ CD ~path-to-project/gruppe-52

# Bygg Docker-filen (laster ned dependencies som trengs)
$ docker-compose build

# Lag tables i databasen 
$ docker-compose run web python manage.py makemigrations
$ docker-compose run web python manage.py migrate

# Lag en admin-bruker
$ docker-compose run web python manage.py createsuperuser

# Kjør serveren på http://localhost:8000/
$ docker-compose up
```
### Uten docker
Endre Gruppe52/settings.py:(ikke push disse endringene)
```diff
DATABASES = {
    'default': {
-        'ENGINE': 'django.db.backends.postgresql',
-        'NAME': 'postgres',
-        'USER': 'postgres',
-        'HOST': 'db',
-        'PASSWORD': 'admin',
-        'PORT': 5432,
+        'ENGINE': 'django.db.backends.sqlite3',
+         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
```shell
# CD til prosjektmappen
$ CD ~path-to-project/gruppe-52

# Installer requirements
$ pip install requirements.txt

# Lag tables i databasen
$ python manage.py makemigrations
$ python manage.py migrate

# Lag en admin-bruker
$ python manage.py createsuperuser

# Kjør serveren på http://localhost:8000/
$ python manage.py runserver
```

### Testing
```shell
$ docker-compose run web python manage.py test
```
Eksempel på en suksessful test
```shell
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.011s

OK
Destroying test database for alias 'default'...
```
### License 



MIT © Matega 2019


Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

