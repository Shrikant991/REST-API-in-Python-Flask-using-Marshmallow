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
class Student(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100),unique=True)
	email=db.Column(db.String(100))

	def __init__(self,name,email):
		self.name=name
		self.email=email

class StudentSchema(ma.Schema):
	class Meta:
		fields=('id','name','email')

student_schema=StudentSchema(strict=True)
students_schema=StudentSchema(many=True,strict=True)

#Creating a new student record
@app.route('/create',methods=['POST'])
def add_student():
	name=request.json['name']
	email=request.json['email']

	new_student=Student(name,email)

	db.session.add(new_student)
	db.session.commit()
	return 'Record created!'
    
	#return student_schema.jsonify(new_student)


#Getting all students records
@app.route('/student',methods=['GET'])
def get_students():
	all_students=Student.query.all()
	result=students_schema.dump(all_students)
	return jsonify(result.data)

#Getting a student's record by its unique ID
@app.route('/student/<id>',methods=['GET'])
def get_student(id):
	student=Student.query.get(id)
	return student_schema.jsonify(student)

#Updating a student's record by its unique ID
@app.route('/update/<id>',methods=['PUT'])
def update_student(id):
	student=Student.query.get(id)

	name=request.json['name']
	email=request.json['email']

	student.name=name
	student.email=email

	db.session.commit()
	return 'Record updated!'

	#return student_schema.jsonify(student)

#Deleting student's record by its unique ID
@app.route('/delete/<id>',methods=['DELETE'])
def delete_student(id):
	student=Student.query.get(id)
	db.session.delete(student)

	db.session.commit()
	return 'Record deleted!'
	#return student_schema.jsonify(student)

if __name__ =='__main__':
	app.run(debug=True)