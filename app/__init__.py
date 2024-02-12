from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models import Student , Notes
from db import db
from dotenv import load_dotenv
import os

load_dotenv()



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI") #config with the pgadmin database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
#db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

# Import routes after creating app and db to avoid circular imports
import app.student_route as student_route
import app.notes_route as notes_route

import app.student_route as student_route
import app.notes_route as notes_route
from app.models import Student , Notes

