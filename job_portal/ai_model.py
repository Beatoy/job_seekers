import os
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, log_loss
import matplotlib.pyplot as plt
import seaborn as sns
import random
import pickle

# Ensure directories exist
if not os.path.exists('static/ai_reports'):
    os.makedirs('static/ai_reports')

# --- 1. Data Simulation ---
def generate_synthetic_data(num_samples=1000):
    """
    Generates synthetic data for candidates and vacancies.
    Features: Degree, Experience Years, Skills (encoded), Previous Job Title
    Target: Recommended Vacancy Category
    """
    degrees = ['Computer Science', 'Information Systems', 'Software Engineering', 'Data Science', 'None']
    job_titles = ['Junior Developer', 'Senior Developer', 'Data Analyst', 'Project Manager', 'Intern']
    skills_list = ['Python', 'Java', 'C++', 'SQL', 'React', 'Node.js', 'Machine Learning', 'AWS']
    vacancy_categories = ['Backend Developer', 'Frontend Developer', 'Data Scientist', 'Full Stack Developer', 'Manager']

    data = []
    
    for _ in range(num_samples):
        # Randomly assign features
        degree = random.choice(degrees)
        experience = random.randint(0, 15)
        primary_skill = random.choice(skills_list)
        prev_job = random.choice(job_titles)
        
        # Logic to assign a target vacancy (to make the model learnable)
        category = 'Backend Developer' # Default
        
        if primary_skill in ['Python', 'Java', 'C++'] and degree in ['Computer Science', 'Software Engineering']:
            category = 'Backend Developer'
        elif primary_skill in ['React', 'Node.js']:
            category = 'Frontend Developer'
        elif primary_skill in ['Machine Learning', 'SQL'] and degree == 'Data Science':
            category = 'Data Scientist'
        elif primary_skill in ['AWS', 'React', 'Node.js'] and experience > 3:
            category = 'Full Stack Developer'
        elif experience > 8:
            category = 'Manager'
            
        # Add some noise
        if random.random() < 0.1:
            category = random.choice(vacancy_categories)

        data.append({
            'degree': degree,
            'experience': experience,
            'primary_skill': primary_skill,
            'prev_job': prev_job,
            'target_category': category
        })
        
    return pd.DataFrame(data)

print("Generating synthetic data...")
df = generate_synthetic_data(2000)

# --- 2. Preprocessing ---
print("Preprocessing data...")
# Encode categorical variables
le_degree = LabelEncoder()
le_skill = LabelEncoder()
le_job = LabelEncoder()
le_target = LabelEncoder()

df['degree_encoded'] = le_degree.fit_transform(df['degree'])
df['skill_encoded'] = le_skill.fit_transform(df['primary_skill'])
df['job_encoded'] = le_job.fit_transform(df['prev_job'])
df['target_encoded'] = le_target.fit_transform(df['target_category'])

# Features and Target
X = df[['degree_encoded', 'experience', 'skill_encoded', 'job_encoded']]
y = df['target_encoded']

# Normalize numerical features (experience)
scaler = StandardScaler()
X['experience'] = scaler.fit_transform(X[['experience']])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 3. Model Architecture (MLP) ---
print("Building and training model (Scikit-learn MLP)...")
# MLPClassifier with 2 hidden layers (64, 32 neurons)
clf = MLPClassifier(hidden_layer_sizes=(64, 32), 
                    activation='relu', 
                    solver='adam', 
                    max_iter=50, 
                    random_state=42,
                    verbose=True)

# --- 4. Training ---
# Scikit-learn's fit doesn't return history per epoch in the same way Keras does for plotting easily 
# without partial_fit, but MLPClassifier has loss_curve_
clf.fit(X_train, y_train)

# --- 5. Visualization & Evaluation ---
print("Generating reports...")

# Plot Loss Curve
plt.figure(figsize=(10, 6))
plt.plot(clf.loss_curve_)
plt.title('Model Loss over Iterations')
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.savefig('static/ai_reports/loss_plot.png')
plt.close()

# Accuracy is not tracked per epoch by default in sklearn MLP, but we can score the final model
train_acc = clf.score(X_train, y_train)
test_acc = clf.score(X_test, y_test)
print(f"Final Training Accuracy: {train_acc:.4f}")
print(f"Final Test Accuracy: {test_acc:.4f}")

# Create a bar chart for accuracy comparison
plt.figure(figsize=(6, 6))
plt.bar(['Training', 'Testing'], [train_acc, test_acc], color=['blue', 'green'])
plt.ylim(0, 1)
plt.title('Final Model Accuracy')
plt.ylabel('Accuracy')
plt.savefig('static/ai_reports/accuracy_plot.png')
plt.close()

# Confusion Matrix
y_pred = clf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=le_target.classes_, 
            yticklabels=le_target.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig('static/ai_reports/confusion_matrix.png')
plt.close()

print("Training complete. Reports saved in static/ai_reports/")

# --- 6. Save Model ---
print("Saving model...")
model_data = {
    'model': clf,
    'le_degree': le_degree,
    'le_skill': le_skill,
    'le_job': le_job,
    'le_target': le_target,
    'scaler': scaler
}

with open('static/ai_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print("Model saved to static/ai_model.pkl")
