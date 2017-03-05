from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


class Association_PFV(db.Model):
    __tablename__ = 'association_pfv'
    pois_id = db.Column(db.Integer, db.ForeignKey(
        'pois.idPoi'), primary_key=True)
    fields_id = db.Column(db.Integer, db.ForeignKey(
        'fields.idField'), primary_key=True)
    values_id = db.Column(db.Integer, db.ForeignKey(
        'values.idValue'), primary_key=True)

    pois = db.relationship("Pois", backref=db.backref(
        "association_pfv", cascade="all, delete-orphan"))
    fields = db.relationship("Fields", backref=db.backref(
        "association_pfv", cascade="all, delete-orphan"))
    values = db.relationship("Values", backref=db.backref(
        "association_pfv", cascade="all, delete-orphan"))

    #def __init__(self, pois=None, fields=None, values=None):
    #    self.pois = pois
    #    self.fields = fields
    #    self.values = values

    def __repr__(self):
        return '<Association_PFV {}>'.format(self.pois.id + " " + self.fields.name + " " + self.values.fieldValues)
class Pois(db.Model):
    idPoi = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer)
    tour_id = db.Column(db.Integer)
    fields = db.relationship('Fields', secondary='association_pfv',
                             backref=db.backref('pois', lazy='dynamic'))
    values = db.relationship('Values', secondary='association_pfv',
                             backref=db.backref('pois', lazy='dynamic'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Fields(db.Model):
    idField = db.Column(db.Integer, primary_key=True)
    pos = db.Column(db.Integer)
    nameField = db.Column(db.String(35))
    requiredField = db.Column(db.Boolean)
    # values=db.relationship('Values', secondary=possede, backref=db.backref('fields', lazy = 'dynamic')  )


class Values(db.Model):
    idValue = db.Column(db.Integer, primary_key=True)
    fieldValues = db.Column(db.Text)
    createdDate = db.Column(db.Date)
    status = db.Column(db.String(35))
    users = db.relationship('Users', backref='value', lazy='dynamic')


class Users(db.Model):
    idUser = db.Column(db.Integer, primary_key=True)
    lastNameUser = db.Column(db.String(35))
    firstNameUser = db.Column(db.String(35))
    email = db.Column(db.String(35))
    pictureUser = db.Column(db.String(35))
    value_id = db.Column(db.Integer, db.ForeignKey('values.idValue'))

# poi
@app.route('/api/pois', methods=['GET'])
def returnAllPois():
	allAsso = Association_PFV.query.all()
	malist = [] #format qui nous arrange pas
	tempPoi=0
	tempField=0
	tempValue=0
	for ass in allAsso:	
		onePoi = Pois.query.filter_by(idPoi=ass.pois_id).first()
		if(tempPoi!=onePoi):
			tempPoi=onePoi
			malist.append({'idPoi': onePoi.idPoi, 'version': onePoi.version, 'tour_id': onePoi.tour_id})
		oneField = Fields.query.filter_by(idField=ass.fields_id).first()
		if(tempField!=oneField):
			tempField=oneField
			oneValue = Values.query.filter_by(idValue=ass.values_id).first()
			if(tempValue!=oneValue):
				tempValue=oneValue
				if(oneField.nameField!='description'):
					malist.append({oneField.nameField : oneValue.fieldValues})
	
	#creation d'une format approprier en utilisant le dictionnaire
	malistFormatBon=[] #format ideal
	dictionnaire={}
	compteurPoi=0;
	compteur=2
	for i in range(len(malist)):
		for cle, valeur in malist[i].items():
			if(cle=='idPoi'):
				compteurPoi+=1;
			if(compteur==compteurPoi):
				malistFormatBon.append(dictionnaire)
				dictionnaire={}
				compteur+=1
			dictionnaire[cle]=valeur
	malistFormatBon.append(dictionnaire)
	return jsonify({'pois': malistFormatBon})

@app.route('/api/pois/<int:idp>', methods=['GET'])
def returnOnepoi(idp):
	allAsso = Association_PFV.query.filter_by(pois_id=idp).all()
	malist = [] #format qui nous arrange pas
	tempPoi=0
	tempField=0
	tempValue=0
	for ass in allAsso:	
		onePoi = Pois.query.filter_by(idPoi=ass.pois_id).first()
		if(tempPoi!=onePoi):
			tempPoi=onePoi
			malist.append({'idPoi': onePoi.idPoi, 'version': onePoi.version, 'tour_id': onePoi.tour_id})
		oneField = Fields.query.filter_by(idField=ass.fields_id).first()
		if(tempField!=oneField):
			tempField=oneField
			oneValue = Values.query.filter_by(idValue=ass.values_id).first()
			if(tempValue!=oneValue):
				tempValue=oneValue
				malist.append({oneField.nameField : oneValue.fieldValues})
	
	#creation d'une format approprier en utilisant le dictionnaire
	malistFormatBon=[] #format ideal
	dictionnaire={}
	compteurPoi=0;
	compteur=2
	for i in range(len(malist)):
		for cle, valeur in malist[i].items():
			if(cle=='idPoi'):
				compteurPoi+=1;
			if(compteur==compteurPoi):
				malistFormatBon.append(dictionnaire)
				dictionnaire={}
				compteur+=1
			dictionnaire[cle]=valeur
	malistFormatBon.append(dictionnaire)
	return jsonify({'pois': malistFormatBon})



@app.route('/api/pois', methods=['POST'])
def addOnePoi():
    # p=Pois(version=request.json['version'], tour_id=request.json['tour_id'])
    # db.session.add(p)
    # db.session.commit()
    # allPois=Pois.query.all()
    # malist=[]
    # for poi in allPois:
    # 	malist.append({'idPoi' : poi.idPoi, 'version' : poi.version, 'tour_id' : poi.tour_id})
    # return jsonify({'pois' : malist})

    currentPoi = Pois(tour_id=request.json['tour_id'], version=1)
    for key, value in request.json.items():
        if key not in ['tour_id']:
            currentField = Fields(pos=1, nameField=key)
            currentValue = Values(fieldValues=value)
            currentasso = Association_PFV(
                currentPoi, currentField, currentValue)
            db.session.add(currentasso)
            db.session.commit()
    return jsonify({'Poi' : currentPoi.idPoi}), 201


db.create_all()
db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
