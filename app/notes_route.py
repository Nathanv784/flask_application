from app import app ,db
from app.models import Notes , Student
from db import db
from flask import Flask, render_template, request, jsonify

@app.route('/students/<int:student_id>/notes', methods=['GET'])

def get_student_notes(student_id):
    student = Student.query.get_or_404(student_id)
    notes = student.notes
    note_list = [{'id': note.id, 'content': note.content} for note in notes]
    return jsonify({'notes': note_list})

@app.route('/students/<int:student_id>/notes', methods=['POST'])

def add_student_notes(student_id):
    data = request.get_json()

    if 'content' not in data:
        return jsonify({'error': 'Missing key: content'}), 400  # Bad Request

    student = Student.query.get_or_404(student_id)
    new_note = Notes(content=data['content'], student=student)

    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Note added successfully'}), 201

@app.route('/notes/delete/<int:student_id>', methods=['DELETE'])
def delete_notes(student_id):
    notes = Notes.query.filter_by(student_id=student_id).all()

    if notes:
        # Delete each note
        for note in notes:
            db.session.delete(note)

        db.session.commit()

        return jsonify({'message': f'Notes associated with Student ID {student_id} deleted successfully'}), 200
    else:
        return jsonify({'error': f'No notes found for Student ID {student_id}'}), 404
