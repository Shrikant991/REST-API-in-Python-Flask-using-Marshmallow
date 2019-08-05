from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app=Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
ma=Marshmallow(app)

#Datebase
class Patient(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100),unique=True)
	doctor_assigned=db.Column(db.String(100))
	date_of_admission=db.Column(db.String(100))
	room=db.Column(db.String(10))


	def __init__(self,name,doctor_assigned,date_of_admission,room):
		self.name=name
		self.doctor_assigned=doctor_assigned
		self.date_of_admission=date_of_admission
		self.room=room


class PatientSchema(ma.Schema):
	class Meta:
		fields=('id','name','doctor_assigned','date_of_admission','room')

patient_schema=PatientSchema(strict=True)
patients_schema=PatientSchema(many=True,strict=True)

#Creating a new Patient record
@app.route('/create',methods=['POST'])
def add_patient():
	name=request.json['name']
	doctor_assigned=request.json['doctor_assigned']
	date_of_admission=request.json['date_of_admission']
	room=request.json['room']

	new_patient=Patient(name,doctor_assigned,date_of_admission,room)

	db.session.add(new_patient)
	db.session.commit()
	return 'Record created!'
    
	#return patient_schema.jsonify(new_patient)


#Getting all patient records
@app.route('/patient',methods=['GET'])
def get_patients():
	all_patients=Patient.query.all()
	result=patients_schema.dump(all_patients)
	return jsonify(result.data)

#Getting a patient's record by its unique ID
@app.route('/patient/<id>',methods=['GET'])
def get_patient(id):
	patient=Patient.query.get(id)
	return patient_schema.jsonify(patient)

#Updating a patient's record by its unique ID
@app.route('/update/<id>',methods=['PUT'])
def update_patient(id):
	patient=Patient.query.get(id)

	name=request.json['name']
	doctor_assigned=request.json['doctor_assigned']
	date_of_admission=request.json['date_of_admission']
	room=request.json['room']

	patient.name=name
	patient.doctor_assigned=doctor_assigned
	patient.date_of_admission=date_of_admission
	patient.room=room

	db.session.commit()
	return 'Record updated!'

	#return patient_schema.jsonify(patient)

#Deleting patient's record by its unique ID
@app.route('/delete/<id>',methods=['DELETE'])
def delete_patient(id):
	patient=Patient.query.get(id)
	db.session.delete(patient)

	db.session.commit()
	return 'Record deleted!'
	#return patient_schema.jsonify(patient)

if __name__ =='__main__':
	app.run(debug=True)