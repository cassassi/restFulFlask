from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


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
	version = db.Column(db.Integer)
	tour_id = db.Column(db.Integer)
	fields=db.relationship('Fields', secondary=possede, backref=db.backref('pois', lazy = 'dynamic')  )
	values=db.relationship('Values', secondary=possede, backref=db.backref('pois', lazy = 'dynamic')  )  
 
class Fields(db.Model):
	idField=db.Column(db.Integer, primary_key=True)
	pos=db.Column(db.Integer)
	nameField=db.Column(db.String(35))  
	requiredField=db.Column(db.Boolean)
	#values=db.relationship('Values', secondary=possede, backref=db.backref('fields', lazy = 'dynamic')  )

class Values(db.Model):
	idValue=db.Column(db.Integer, primary_key=True)
	fieldValues=db.Column(db.Text)
	createdDate=db.Column(db.Date)
	status=db.Column(db.String(35))  
	users = db.relationship('Users', backref='value', lazy='dynamic') 

class Users(db.Model):
	idUser=db.Column(db.Integer, primary_key=True)
	lastNameUser=db.Column(db.String(35)) 
	firstNameUser=db.Column(db.String(35)) 
	email=db.Column(db.String(35)) 
	pictureUser=db.Column(db.String(35)) 
	value_id = db.Column(db.Integer, db.ForeignKey('values.idValue'))

#poi
@app.route('/api/pois', methods=['GET'])
def returnAllPois():
	allPois=Pois.query.all()
	malist=[]

	for poi in allPois:
		malist.append({'idPoi' : poi.idPoi, 'version' : poi.version, 'tour_id' : poi.tour_id})
	return jsonify({'pois' : malist})

@app.route('/api/pois', methods=['POST'])
def addOnePoi():
	p=Pois(version=request.json['version'], tour_id=request.json['tour_id'])
	db.session.add(p)
	db.session.commit()
	allPois=Pois.query.all()
	malist=[]
	for poi in allPois:
		malist.append({'idPoi' : poi.idPoi, 'version' : poi.version, 'tour_id' : poi.tour_id})
	return jsonify({'pois' : malist})

@app.route('/api/pois/<int:idp>', methods=['GET'])
def returnOnepoi(idp):
	onePoi=Pois.query.filter_by(idPoi=idp).first()
	if onePoi==None:
		return jsonify({'poi' : 'no results was founds'})
	malist=[]
	malist.append({'idPoi' : onePoi.idPoi, 'version' : onePoi.version, 'tour_id' : onePoi.tour_id})
	return jsonify({'poi' : malist[0]})


#Field
@app.route('/api/fields', methods=['GET'])
def returnAllFields():
	allFields=Fields.query.all()
	malist=[]

	for field in allFields:
		malist.append({'idField' : field.idField, 'pos' : field.pos, 'nameField' : field.nameField, 'requiredField' : field.requiredField})
	return jsonify({'fields' : malist})

@app.route('/api/fields', methods=['POST'])
def addOneField():
	f=Fields(pos=request.json['pos'], nameField=request.json['nameField'], requiredField=request.json['requiredField'])
	db.session.add(f)
	db.session.commit()
	allFields=Fields.query.all()
	malist=[]
	for field in allFields:
		malist.append({'idField' : field.idField, 'pos' : field.pos, 'nameField' : field.nameField, 'requiredField' : field.requiredField})
	return jsonify({'fields' : malist})

@app.route('/api/fields/<int:idp>', methods=['GET'])
def returnOneField(idp):
	oneField=Fields.query.filter_by(idField=idp).first()
	if oneField==None:
		return jsonify({'field' : 'no results was founds'})
	malist=[]
	malist.append({'idField' : oneField.idField, 'pos' : oneField.pos, 'nameField' : oneField.nameField, 'requiredField' : oneField.requiredField})
	return jsonify({'field' : malist[0]})


#Value
@app.route('/api/values', methods=['GET'])
def returnAllValues():
	allValues=Values.query.all()
	malist=[]

	for value in allValues:
		malist.append({'idValue' : value.idValue, 'fieldValues' : value.fieldValues, 'createdDate' : value.createdDate, 'status' : value.status})
	return jsonify({'values' : malist})

@app.route('/api/values', methods=['POST'])
def addOneValue():
	v=Values(fieldValues=request.json['fieldValues'], createdDate=request.json['createdDate'], status=request.json['status'])
	db.session.add(v)
	db.session.commit()
	allValues=Values.query.all()
	malist=[]
	for value in allValues:
		malist.append({'idValue' : value.idValue, 'fieldValues' : value.fieldValues, 'createdDate' : value.createdDate, 'status' : value.status})
	return jsonify({'values' : malist})

@app.route('/api/values/<int:idp>', methods=['GET'])
def returnOneValue(idp):
	oneValue=Values.query.filter_by(idValue=idp).first()
	if oneValue==None:
		return jsonify({'value' : 'no results was founds'})
	malist=[]
	malist.append({'idValue' : oneValue.idValue, 'fieldValues' : oneValue.fieldValues, 'createdDate' : oneValue.createdDate, 'status' : oneValue.status})
	return jsonify({'value' : malist[0]})

@app.route('/api/possede', methods=['GET'])

def returnconnexion():
	v=Values.query.all()
	f=Fields.query.all()
	malist=[]
	for value in v:
		for field in value.fields:
			for poi in field.pois:
				malist.append({'idPoi':poi.idPoi,'idField':field.idField, 'idValue':value.idValue})
	return jsonify({'possede' : malist})

@app.route('/api/possede', methods=['POST'])
def addconnection():
	p=Pois.query.filter_by(idPoi=request.json['idPoi']).first()
	v=Values.query.filter_by(idValue=request.json['idValue']).first()
	f=Fields.query.filter_by(idField=request.json['idField']).first()
	v.fields.append(f)
	f.pois.append(p)
	db.session.commit()

	v=Values.query.all()
	f=Fields.query.all()
	malist=[]
	for value in v:
		for field in value.fields:
			for poi in field.pois:
				malist.append({'idPoi':poi.idPoi,'idField':field.idField, 'idValue':value.idValue})
	return jsonify({'possede' : malist})

#p=Pois.query.filter_by(idPoi=1).first()                                
#v=Values.query.filter_by(idValue=1).first()                      
#f=Fields.query.filter_by(idField=1).first()                      
#v.fields.append(f)
#f.pois.append(p)
#db.session.commit()




if __name__ == "__main__":
	app.run(debug=True)




