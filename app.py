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

class Comments(db.Model):
    message = db.Column(db.Text)
    title = db.Column(db.String(50))
    createdDate = db.Column(db.Date)
    iduser = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    idpoi = db.Column(db.Integer, db.ForeignKey(
        'pois.id'), primary_key=True)

    users = db.relationship("Users", backref=db.backref(
        "comments", cascade="all, delete-orphan"))
    pois = db.relationship("Pois", backref=db.backref(
        "comments", cascade="all, delete-orphan"))

class Rewards(db.Model):
    idaward = db.Column(db.Integer, db.ForeignKey(
        'awards.id'), primary_key=True)
    iduser = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)

    award = db.relationship("Awards", backref=db.backref(
        "rewards", cascade="all, delete-orphan"))
    users = db.relationship("Users", backref=db.backref(
        "rewards", cascade="all, delete-orphan"))


class Generaltypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    name_fr = db.Column(db.String(80))
    name_en = db.Column(db.String(80))
    name_es = db.Column(db.String(80))
    name_de = db.Column(db.String(80))
    name_it = db.Column(db.String(80))
    typespoi = db.relationship('Typespois', backref='generaltypes', lazy='dynamic')


class Typespois(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    name_fr = db.Column(db.String(80))
    name_en = db.Column(db.String(80))
    name_es = db.Column(db.String(80))
    name_de = db.Column(db.String(80))
    name_it = db.Column(db.String(80))
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


class Types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    size = db.Column(db.Integer)
    fields = db.relationship('Fields', backref='types', lazy='dynamic')


class Fields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pos = db.Column(db.Integer)
    name = db.Column(db.String(80))
    required = db.Column(db.Boolean)
    types_id = db.Column(db.Integer, db.ForeignKey('types.id'))


class Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text)
    createddate = db.Column(db.Date)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(35))
    firstname = db.Column(db.String(35))
    email = db.Column(db.String(35))
    picture = db.Column(db.String(35))
    values = db.relationship('Values', backref='users', lazy='dynamic')
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    accounts_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('Users', backref='categories', lazy='dynamic')

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    users = db.relationship('Users', backref='accounts', lazy='dynamic')

class Awards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typeAward = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(25), nullable=False)



# --------------------------------------------pois---------------------------------------------------------
@app.route('/api/pois', methods=['GET'])
def returnAllPois():
	allAsso = Contributions.query.all()

	malist = [] #format qui nous arrange pas
	tempPoi=0
	tempField=0
	tempValue=0
	for ass in allAsso:
		onePoi = Pois.query.filter_by(id=ass.idpoi).first()
		if(tempPoi!=onePoi):
			tempPoi=onePoi
			malist.append({'id': onePoi.id, 'tour_id': onePoi.tour_id})
		oneField = Fields.query.filter_by(id=ass.idfield).first()
		if(tempField!=oneField):
			tempField=oneField
			oneValue = Values.query.filter_by(id=ass.idvalue).first()
			if(tempValue!=oneValue):
				tempValue=oneValue
				if(oneField.name != 'description'):
					malist.append({oneField.name : oneValue.value})
	#creation d'une format approprier en utilisant le dictionnaire
	malistFormatBon=[] #format ideal
	dictionnaire={}
	compteurPoi=0;
	compteur=2
	for i in range(len(malist)):
		for cle, valeur in malist[i].items():
			if(cle=='id'):
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
	allAsso = Contributions.query.filter_by(idpoi=idp).all()

	malist = [] #format qui nous arrange pas
	tempPoi=0
	tempField=0
	tempValue=0
	for ass in allAsso:
		onePoi = Pois.query.filter_by(id = ass.idpoi).first()
		if(tempPoi!=onePoi):
			tempPoi=onePoi
			malist.append({'id': onePoi.id, 'tour_id': onePoi.tour_id})
		oneField = Fields.query.filter_by(id=ass.idfield).first()
		if(tempField!=oneField):
			tempField=oneField
			oneValue = Values.query.filter_by(id=ass.idvalue).first()
			if(tempValue!=oneValue):
				tempValue=oneValue
				malist.append({oneField.name : oneValue.value})

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
            currentasso = Contributions(
                currentPoi, currentField, currentValue)
            db.session.add(currentasso)
            db.session.commit()
    return jsonify({'Poi' : currentPoi.idPoi}), 201

# ---------------------------------------contributions---------------------------------------------------------
@app.route('/api/contributions', methods=['GET'])
def returnAllContributions():
    allAsso = Contributions.query.all()

    malist = [] #format qui nous arrange pas
    tempPoi=0
    tempField=0
    tempValue=0
    for ass in allAsso:

        oneValue = Values.query.filter_by(id=ass.idvalue).first()
        if(tempValue!=oneValue):
            tempValue=oneValue
            malist.append({'id': oneValue.id, 'created_date': oneValue.createddate, 'value': oneValue.value})

            oneUser = Values.query.filter_by(id=oneValue.users_id).first()
            theUser = Users.query.filter_by(id=oneUser.id).first()
            malist.append({'user_name': theUser.lastname})

        onePoi = Pois.query.filter_by(id=ass.idpoi).first()
        malist.append({'poi_id': onePoi.id})

        oneField = Fields.query.filter_by(id=ass.idfield).first()
        if(tempField!=oneField):
            tempField=oneField
            malist.append({'field.name' : oneField.name})

        malist.append({'status': ass.status})
    #creation d'une format approprier en utilisant le dictionnaire
    malistFormatBon=[] #format ideal
    dictionnaire={}
    compteurContrib=0;
    compteur=2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle=='id'):
                compteurContrib+=1;
            if(compteur==compteurContrib):
                malistFormatBon.append(dictionnaire)
                dictionnaire={}
                compteur+=1
            dictionnaire[cle]=valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'contributions': malistFormatBon})


@app.route('/api/contributions/<int:idp>', methods=['GET'])
def returnContributionsById(idp):
    allAsso = Contributions.query.filter_by(idpoi=idp).all()

    malist = [] #format qui nous arrange pas
    tempPoi=0
    tempField=0
    tempValue=0
    for ass in allAsso:

        oneValue = Values.query.filter_by(id=ass.idvalue).first()
        if(tempValue!=oneValue):
            tempValue=oneValue
            malist.append({'id': oneValue.id, 'created_date': oneValue.createddate, 'value': oneValue.value})

            oneUser = Values.query.filter_by(id=oneValue.users_id).first()
            theUser = Users.query.filter_by(id=oneUser.id).first()
            malist.append({'user_name': theUser.lastname})

        onePoi = Pois.query.filter_by(id=ass.idpoi).first()
        malist.append({'poi_id': onePoi.id})

        oneField = Fields.query.filter_by(id=ass.idfield).first()
        if(tempField!=oneField):
            tempField=oneField
            malist.append({'field.name' : oneField.name})

        malist.append({'status': ass.status})
    #creation d'une format approprier en utilisant le dictionnaire
    malistFormatBon=[] #format ideal
    dictionnaire={}
    compteurContrib=0;
    compteur=2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle=='id'):
                compteurContrib+=1;
            if(compteur==compteurContrib):
                malistFormatBon.append(dictionnaire)
                dictionnaire={}
                compteur+=1
            dictionnaire[cle]=valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'contributionsById': malistFormatBon})

# --------------------------------------------versions---------------------------------------------------------

@app.route('/api/versions/poi/<int:idp>', methods=['GET'])
def returnVersionsOfOnePoi(idp):
    allAsso = Contributions.query.filter_by(idpoi=idp).all()

    malist = [] #format qui nous arrange pas
    tempPoi=0
    tempField=0
    tempValue=0
    tempVersion = 0
    for ass in allAsso:

        oneVersion = Contributions.query.filter_by(version=ass.version).first()
        #if(tempVersion!=oneVersion):
            #tempVersion=oneVersion
        malist.append({'version': oneVersion.version})

        onePoi = Pois.query.filter_by(id=ass.idpoi).first()
        #if(tempPoi!=onePoi):
            #tempPoi=onePoi
        malist.append({'id': onePoi.id, 'tour_id': onePoi.tour_id})

        oneField = Fields.query.filter_by(id=ass.idfield).first()
        if(tempField!=oneField):
            tempField=oneField
            oneValue = Values.query.filter_by(id=ass.idvalue).first()
            if(tempValue!=oneValue):
                tempValue=oneValue
                malist.append({oneField.name : oneValue.value})



    #creation d'une format approprier en utilisant le dictionnaire
    malistFormatBon=[] #format ideal
    dictionnaire={}
    compteurVersion=0;
    compteur=2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle=='version'):
                compteurVersion+=1;
            if(compteur==compteurVersion):
                malistFormatBon.append(dictionnaire)
                dictionnaire={}
                compteur+=1
            dictionnaire[cle]=valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'versions': malistFormatBon})


db.create_all()
db.session.commit()




if __name__ == "__main__":
    app.run(debug=True)
