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
class Employee(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100),unique=True)
	email=db.Column(db.String(100))
	salary=db.Column(db.Integer)

	def __init__(self,name,email,salary):
		self.name=name
		self.email=email
		self.salary=salary

class EmployeeSchema(ma.Schema):
	class Meta:
		fields=('id','name','email','salary')

employee_schema=EmployeeSchema(strict=True)
employees_schema=EmployeeSchema(many=True,strict=True)

#Creating a new employee record
@app.route('/create',methods=['POST'])
def add_employee():
	name=request.json['name']
	email=request.json['email']
	salary=request.json['salary']

	new_employee=Employee(name,email,salary)

	db.session.add(new_employee)
	db.session.commit()
	return 'Record created!'
    
	#return employee_schema.jsonify(new_employee))


#Getting all employee records
@app.route('/employee',methods=['GET'])
def get_employees():
	all_employees=Employee.query.all()
	result=employees_schema.dump(all_employees)
	return jsonify(result.data)

#Getting a employee's record by its unique ID
@app.route('/employee/<id>',methods=['GET'])
def get_employee(id):
	employee=Employee.query.get(id)
	return employee_schema.jsonify(employee)

#Updating a employee's record by its unique ID
@app.route('/update/<id>',methods=['PUT'])
def update_employee(id):
	employee=Employee.query.get(id)

	name=request.json['name']
	email=request.json['email']
	salary=request.json['salary']

	employee.name=name
	employee.email=email
	employee.salary=salary

	db.session.commit()
	return 'Record updated!'

	#return employee_schema.jsonify(employee)

#Deleting employee's record by its unique ID
@app.route('/delete/<id>',methods=['DELETE'])
def delete_employee(id):
	employee=Employee.query.get(id)
	db.session.delete(employee)

	db.session.commit()
	return 'Record deleted!'
	#return employee_schema.jsonify(employee)

if __name__ =='__main__':
	app.run(debug=True)