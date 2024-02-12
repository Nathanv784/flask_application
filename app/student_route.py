from app import app ,db
from app.models import Student , Notes
from db import db
from flask import Flask, render_template, request, jsonify

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/students/all', methods=['GET'])

def get_students():
    students = Student.query.all()
    student_list = [{'id': student.id, 'firstname': student.firstname, 'lastname': student.lastname, 'email': student.email} for student in students]
    return jsonify({'students': student_list})

@app.route('/students/add', methods=['POST'])

def add_student():
    data = request.get_json()

    new_student = Student(firstname=data['firstname'], lastname=data['lastname'], email=data['email'])
    db.session.add(new_student)
    db.session.commit()

    return jsonify({'message': 'Student added successfully'}), 201

@app.route('/students/get/<int:student_id>', methods=['GET'])

def get_student_details(student_id):
    user_notes = db.session.query(Student,Notes).join(Notes).filter(Student.id == student_id).all()
    result =[]
    for user, note in user_notes:
        result.append({
            'id': user.id,
            'firstname': user.firstname,
            'id': note.id,
            'Content': note.content
        })
    return jsonify(result)

@app.route('/students/update/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    # Get the updated data from the request body
    data = request.get_json()

    # Retrieve the student by ID
    student = Student.query.get_or_404(student_id)

    # Update the student attributes
    student.firstname = data.get('firstname', student.firstname)
    student.lastname = data.get('lastname', student.lastname)
    student.email = data.get('email', student.email)

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Student updated successfully'}), 200

@app.route('/students_notes/delete/<int:student_id>', methods=['DELETE'])
def delete_record(student_id):
    student = Student.query.get(student_id)

    if student:
        # Delete associated notes first
        notes = Notes.query.filter_by(student_id=student_id).all()
        for note in notes:
            db.session.delete(note)

        # Now delete the student
        db.session.delete(student)
        db.session.commit()

        return jsonify({'message': f'Student with ID {student_id} and associated notes deleted successfully'}), 200
    else:
        return jsonify({'error': f'Student with ID {student_id} not found'}), 404   
     
    
@app.route('/students/delete/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)

    if student:
        # Now delete the student
        db.session.delete(student)
        db.session.commit()

        return jsonify({'message': f'Student with ID {student_id} deleted successfully'}), 200
    else:
        return jsonify({'error': f'Student with ID {student_id} not found'}), 404

