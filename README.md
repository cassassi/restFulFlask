# restFulFlask
Creation d'une API REST (one-many)

#creation d'environement python3
mkdir appRestFulFlask
cd appRestFulFlask
export VENV=~/appRestFulFlask/env
python3 -m venv $VENV
source env/bin/activate

#installation
postgres doit etre installé
pip3 install flask
pip3 install psycopg2
pip3 install Flask-SQLAlchemy

#configuration
config.cfg : changer mot de passe et login et crier une base de donnee vide

#lancer l'application
python3 app.py

#tester l'application
Ensemble (GET, POST)
http http://127.0.0.1:5000/api/persons
http POST http://127.0.0.1:5000/api/persons name=franc

Individu (GET, POST)
http http://127.0.0.1:5000/api/persons/1
http DELETE http://127.0.0.1:5000/api/persons/2
http PUT http://127.0.0.1:5000/api/persons/3 name=marc



