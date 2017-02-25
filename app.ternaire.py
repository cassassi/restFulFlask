from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


possede=db.Table('possede',                            
 
                             db.Column('pois_id', db.Integer,db.ForeignKey('pois.idPoi'), nullable=False),
                             db.Column('fields_id',db.Integer,db.ForeignKey('fields.idField'),nullable=False),
			     db.Column('values_id',db.Integer,db.ForeignKey('values.idValue'),nullable=False),
                             db.PrimaryKeyConstraint('pois_id', 'fields_id', 'values_id') )
 
class Pois(db.Model):
	idPoi = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(35),nullable=False)
	fields=db.relationship('Fields', secondary=possede, backref='pois' )  
	values=db.relationship('Values', secondary=possede, backref='pois' )
 
class Fields(db.Model):
	idField=db.Column(db.Integer, primary_key=True)
	pos=db.Column(db.Integer)
	nameField=db.Column(db.String(35))  
	values=db.relationship('Values', secondary=possede, backref='fields' )

class Values(db.Model):
	idValue=db.Column(db.Integer, primary_key=True)
	fieldValues=db.Column(db.Text)
	createdDate=db.Column(db.Date)
	status=db.Column(db.String(35))  
	users = db.relationship('Users', backref='value', lazy='dynamic') 

class Users(db.Model):
	idUser=db.Column(db.Integer, primary_key=True)
	nameUser=db.Column(db.Text)
	value_id = db.Column(db.Integer, db.ForeignKey('values.idValue'))
	


manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Pois, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Fields, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Values, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Users, methods=['GET', 'POST', 'DELETE', 'PUT'])

if __name__ == "__main__":
	app.run(debug=True)




