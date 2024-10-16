from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import joblib
from statistics import mean
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('instance\career_predictions.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    career1 = db.Column(db.String(100), nullable=False)
    prob1 = db.Column(db.Float, nullable=False)
    career2 = db.Column(db.String(100), nullable=False)
    prob2 = db.Column(db.Float, nullable=False)
    career3 = db.Column(db.String(100), nullable=False)
    prob3 = db.Column(db.Float, nullable=False)

model = joblib.load('model.pkl')

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/past_entries')
def past_entries():
    predictions = Prediction.query.all()

    # Pass the records to the template
    return render_template('past_entries.html', records=predictions)

@app.route('/questionnaire')
def questionnaire():
    return render_template('test.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get user input
    name = request.form.get('name')
    email = request.form.get('email')

    features = []
    
    attributes = ['thinking', 'problem', 'creativity', 'communication', 'leadership', 
                  'empathy', 'science', 'teamwork', 'tech', 'design', 
                  'math', 'medical', 'legal', 'business', 'research', 
                  'marketing', 'teaching', 'software', 'artistic', 'attention']

    for attribute in attributes:
        scores = [
            float(request.form.get(f'{attribute}_q1', 0)),
            float(request.form.get(f'{attribute}_q2', 0)),
            float(request.form.get(f'{attribute}_q3', 0)),
        ]
        average_score = round(mean([score for score in scores if score > 0]))  # Calculate the average
        features.append(average_score)
    
    features = pd.DataFrame([features])

    # Get probabilities instead of direct predictions
    probabilities = model.predict_proba(features)
    
    # Get top 3 predictions and their corresponding probabilities
    top_indices = probabilities[0].argsort()[-3:][::-1]
    top_probabilities = probabilities[0][top_indices]
    
    career_roles = {
        1: 'Research Scientist', 2: 'Pilot', 3: 'Engineer', 4: 'Fashion Designer',
        5: 'Pharmacist', 6: 'Accountant', 7: 'Teacher', 8: 'Lawyer',
        9: 'Architect', 10: 'Graphic Designer', 11: 'Psychologist', 12: 'Business Analyst',
        13: 'Marketing Manager', 14: 'Web Developer', 15: 'Software Engineer',
        16: 'Doctor', 17: 'Veterinarian', 18: 'Data Analyst', 19: 'Nurse'
    }

    top_careers = [(career_roles[i + 1], top_probabilities[j]) for j, i in enumerate(top_indices)]
    
    # Save to the database
    new_prediction = Prediction(
        name=name,
        email=email,
        career1=top_careers[0][0],
        prob1=top_careers[0][1],
        career2=top_careers[1][0],
        prob2=top_careers[1][1],
        career3=top_careers[2][0],
        prob3=top_careers[2][1]
    )
    db.session.add(new_prediction)
    db.session.commit()

    return render_template('results.html', top_careers=top_careers)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the table if it doesn't exist
    app.run(debug=True)
