# restFulFlask
Creation d'une API REST 

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
config.cfg : changer le mot de passe et le login et crier une base de donnee vide
l'application se charge de crier les tables

#lancer l'application
python3 app.py

#tester l'application
Ensemble (GET)
http http://127.0.0.1:5000/api/pois

Individu (GET)
http http://127.0.0.1:5000/api/pois/1




