from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


class Contributions(db.Model):
    version = db.Column(db.Integer)
    status = db.Column(db.String(35))

    idpoi = db.Column(db.Integer, db.ForeignKey(
        'pois.id'), primary_key=True)
    idfield = db.Column(db.Integer, db.ForeignKey(
        'fields.id'), primary_key=True)
    idvalue = db.Column(db.Integer, db.ForeignKey(
        'values.id'), primary_key=True)

    pois = db.relationship("Pois", backref=db.backref(
        "contributions", cascade="all, delete-orphan"))
    fields = db.relationship("Fields", backref=db.backref(
        "contributions", cascade="all, delete-orphan"))
    values = db.relationship("Values", backref=db.backref(
        "contributions", cascade="all, delete-orphan"))

    #def __init__(self, pois=None, fields=None, values=None):
    #    self.pois = pois
    #    self.fields = fields
    #    self.values = values

    def __repr__(self):
        return '<Contributions {}>'.format(self.pois.id + " " + self.fields.name + " " + self.values.value)


class Generaltypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    typespoi = db.relationship('Typespois', backref='generaltypes', lazy='dynamic')


class Typespois(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    generaltypes_id = db.Column(db.Integer, db.ForeignKey('generaltypes.id'), nullable=False)
    pois = db.relationship('Pois', backref='typespois', lazy='dynamic')


class Pois(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer)
    typespois_id = db.Column(db.Integer, db.ForeignKey('typespois.id'), nullable=False)


    fields = db.relationship('Fields', secondary='contributions',
                             backref=db.backref('pois', lazy='dynamic'))
    values = db.relationship('Values', secondary='contributions',
                             backref=db.backref('pois', lazy='dynamic'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Fields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pos = db.Column(db.Integer)
    name = db.Column(db.String(80))
    required = db.Column(db.Boolean)
    # values=db.relationship('Values', secondary=possede, backref=db.backref('fields', lazy = 'dynamic')  )


class Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text)
    createdDate = db.Column(db.Date)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(35))
    firstName = db.Column(db.String(35))
    email = db.Column(db.String(35))
    picture = db.Column(db.String(35))
    values = db.relationship('Values', backref='users_id', lazy='dynamic')

# poi
# @app.route('/api/pois', methods=['GET'])
# def returnAllPois():
# 	allAsso = Contributions.query.all()
# 	malist = [] #format qui nous arrange pas
# 	tempPoi=0
# 	tempField=0
# 	tempValue=0
# 	for ass in allAsso:
# 		onePoi = Pois.query.filter_by(idPoi=ass.id).first()
# 		if(tempPoi!=onePoi):
# 			tempPoi=onePoi
# 			malist.append({'idPoi': onePoi.idPoi, 'version': onePoi.version, 'tour_id': onePoi.tour_id})
# 		oneField = Fields.query.filter_by(idField=ass.idfields).first()
# 		if(tempField!=oneField):
# 			tempField=oneField
# 			oneValue = Values.query.filter_by(idValue=ass.idvalues).first()
# 			if(tempValue!=oneValue):
# 				tempValue=oneValue
# 				if(oneField.nameField!='description'):
# 					malist.append({oneField.nameField : oneValue.fieldValues})
#
# 	#creation d'une format approprier en utilisant le dictionnaire
# 	malistFormatBon=[] #format ideal
# 	dictionnaire={}
# 	compteurPoi=0;
# 	compteur=2
# 	for i in range(len(malist)):
# 		for cle, valeur in malist[i].items():
# 			if(cle=='idPoi'):
# 				compteurPoi+=1;
# 			if(compteur==compteurPoi):
# 				malistFormatBon.append(dictionnaire)
# 				dictionnaire={}
# 				compteur+=1
# 			dictionnaire[cle]=valeur
# 	malistFormatBon.append(dictionnaire)
# 	return jsonify({'pois': malistFormatBon})
#
# @app.route('/api/pois/<int:idp>', methods=['GET'])
# def returnOnepoi(idp):
# 	allAsso = Contributions.query.filter_by(idpoi=idp).all()
# 	malist = [] #format qui nous arrange pas
# 	tempPoi=0
# 	tempField=0
# 	tempValue=0
# 	for ass in allAsso:
# 		onePoi = Pois.query.filter_by(idPoi=ass.pois_id).first()
# 		if(tempPoi!=onePoi):
# 			tempPoi=onePoi
# 			malist.append({'idPoi': onePoi.idPoi, 'version': onePoi.version, 'tour_id': onePoi.tour_id})
# 		oneField = Fields.query.filter_by(idField=ass.fields_id).first()
# 		if(tempField!=oneField):
# 			tempField=oneField
# 			oneValue = Values.query.filter_by(idValue=ass.values_id).first()
# 			if(tempValue!=oneValue):
# 				tempValue=oneValue
# 				malist.append({oneField.nameField : oneValue.fieldValues})
#
# 	#creation d'une format approprier en utilisant le dictionnaire
# 	malistFormatBon=[] #format ideal
# 	dictionnaire={}
# 	compteurPoi=0;
# 	compteur=2
# 	for i in range(len(malist)):
# 		for cle, valeur in malist[i].items():
# 			if(cle=='idPoi'):
# 				compteurPoi+=1;
# 			if(compteur==compteurPoi):
# 				malistFormatBon.append(dictionnaire)
# 				dictionnaire={}
# 				compteur+=1
# 			dictionnaire[cle]=valeur
# 	malistFormatBon.append(dictionnaire)
# 	return jsonify({'pois': malistFormatBon})
#
#
#
# @app.route('/api/pois', methods=['POST'])
# def addOnePoi():
#     # p=Pois(version=request.json['version'], tour_id=request.json['tour_id'])
#     # db.session.add(p)
#     # db.session.commit()
#     # allPois=Pois.query.all()
#     # malist=[]
#     # for poi in allPois:
#     # 	malist.append({'idPoi' : poi.idPoi, 'version' : poi.version, 'tour_id' : poi.tour_id})
#     # return jsonify({'pois' : malist})
#
#     currentPoi = Pois(tour_id=request.json['tour_id'], version=1)
#     for key, value in request.json.items():
#         if key not in ['tour_id']:
#             currentField = Fields(pos=1, nameField=key)
#             currentValue = Values(fieldValues=value)
#             currentasso = Contributions(
#                 currentPoi, currentField, currentValue)
#             db.session.add(currentasso)
#             db.session.commit()
#     return jsonify({'Poi' : currentPoi.idPoi}), 201
#

db.create_all()
db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
