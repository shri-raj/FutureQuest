from flask import Flask, render_template, request
import pandas as pd
import joblib
from statistics import mean

app = Flask(__name__)

model = joblib.load('model.pkl')

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/questionnaire')
def questionnaire():
    return render_template('test.html')

@app.route('/predict', methods=['POST'])
def predict():
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

    prediction = model.predict(features)

    career_roles = {
        1: 'Research Scientist', 2: 'Pilot', 3: 'Engineer', 4: 'Fashion Designer',
        5: 'Pharmacist', 6: 'Accountant', 7: 'Teacher', 8: 'Lawyer',
        9: 'Architect', 10: 'Graphic Designer', 11: 'Psychologist', 12: 'Business Analyst',
        13: 'Marketing Manager', 14: 'Web Developer', 15: 'Software Engineer',
        16: 'Doctor', 17: 'Veterinarian', 18: 'Data Analyst', 19: 'Nurse'
    }

    predicted_career = career_roles.get(prediction[0])
    return render_template('results.html', career=predicted_career)

if __name__ == '__main__':
    app.run(debug=True)
