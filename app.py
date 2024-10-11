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
    print(features)
    features = pd.DataFrame([features])

    # Get probabilities instead of direct predictions
    probabilities = model.predict_proba(features)
    
    # Get top 3 predictions and their corresponding probabilities
    top_indices = probabilities[0].argsort()[-3:][::-1]  # Get the indices of the top 3 probabilities
    top_probabilities = probabilities[0][top_indices]
    
    career_roles = {
        1: 'Research Scientist', 2: 'Pilot', 3: 'Engineer', 4: 'Fashion Designer',
        5: 'Pharmacist', 6: 'Accountant', 7: 'Teacher', 8: 'Lawyer',
        9: 'Architect', 10: 'Graphic Designer', 11: 'Psychologist', 12: 'Business Analyst',
        13: 'Marketing Manager', 14: 'Web Developer', 15: 'Software Engineer',
        16: 'Doctor', 17: 'Veterinarian', 18: 'Data Analyst', 19: 'Nurse'
    }

    # Prepare the results
    top_careers = [(career_roles[i + 1], top_probabilities[j]) for j, i in enumerate(top_indices)]
    
    return render_template('results.html', top_careers=top_careers)


if __name__ == '__main__':
    app.run(debug=True)
