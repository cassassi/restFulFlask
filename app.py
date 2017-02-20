from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

class Persons(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	pets = db.relationship('Pets', backref='owner', lazy='dynamic')

class Pets(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	owner_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

languages = [{'id' : 1, 'name' : 'Javascript'},{'id' : 2, 'name' : 'Python'}, {'id' : 3, 'name' : 'Ruby'}]


#groupe persons
@app.route('/api/persons', methods=['GET'])
def returnAllpersons():
	r=Persons.query.all()
	malist=[]
	for person in r:
		malist.append({'id' : person.id, 'name' : person.name})
	return jsonify({'persons' : malist})
	
@app.route('/api/persons', methods=['POST'])
def addOnepersons():
	p1=Persons(name=request.json['name'])
	db.session.add(p1)
	db.session.commit()
	r=Persons.query.all()
	malist=[]
	for person in r:
		malist.append({'id' : person.id, 'name' : person.name})
	return jsonify({'persons' : malist})

#individu person
#@app.route('/api/persons/<int:id>', methods=['GET'])
#def returnOneperson(id):
#	r=Persons.query.all()
#	malist=[]
#	for person in r:
#		if id==person.id:
#			malist.append({'id' : person.id, 'name' : person.name})
#			return jsonify({'person' : malist[0]})
#	return jsonify({'person' : 'no results was founds'})

#individu person
@app.route('/api/persons/<int:idp>', methods=['GET'])
def returnOneperson(idp):
	r=Persons.query.filter_by(id=idp).first()
	if r==None:
		return jsonify({'person' : 'no results was founds'})
	malist=[]
	malist.append({'id' : r.id, 'name' : r.name})
	return jsonify({'person' : malist[0]})
	

#@app.route('/api/persons/<int:id>', methods=['DELETE'])
#def deleteOneperson(id):
#	r=Persons.query.all()
#	malist=[]
#	for person in r:
#		if id==person.id:
#			r2=person
#			db.session.delete(r2)
#			db.session.commit()
#		else:
#			malist.append({'id' : person.id, 'name' : person.name})
#	return jsonify({'persons' : malist})
@app.route('/api/persons/<int:idp>', methods=['DELETE'])
def deleteOneperson(idp):
	r=Persons.query.filter_by(id=idp).first()
	if r==None:
		return jsonify({'persons' : 'no object to delete'})
	db.session.delete(r)
	db.session.commit()
	malist=[]
	for person in Persons.query.all():
		malist.append({'id' : person.id, 'name' : person.name})
	return jsonify({'persons' : malist})
	
@app.route('/api/persons/<int:idp>', methods=['PUT'])
def modifyOneperson(idp):
	r=Persons.query.filter_by(id=idp).first()
	if r==None:
		return jsonify({'persons' : 'no object to modify'})
	#supprimer l'element a modifier
	db.session.delete(r)
	db.session.commit()
	
	#le recrier en gardant le meme id
	p1=Persons(id=r.id, name=request.json['name'])
	db.session.add(p1)
	db.session.commit()

	malist=[]
	malist.append({'id' : r.id, 'name' : p1.name})
	return jsonify({'persons' : malist[0]})	



if __name__ == "__main__":
	app.run(debug=True)




