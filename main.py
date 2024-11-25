from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import markdown
from docx import Document

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with Open Router AI
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv('GEMINI_API_KEY'),
)

class ResumeAnalysisAgent:
    def analyze_resume(self, resume_text):
        prompt = f"Analyze the following resume and provide an strong analysis of strengths and weaknesses along with pointers on which aspect needs improvement(Note: Makes sure to mention in points and only top 5 among them but dont mention they are top 5):\n\n{resume_text}"
        completion = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content

class EditSuggestionAgent:
    def suggest_edits(self, resume_text):
        prompt = f"Suggest edits for the following resume to make it more polished and effective:\n\n{resume_text}"
        completion = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content

class SkillRecommendationAgent:
    def recommend_skills(self, field_of_interest):
        prompt = f"What are some additional skills you might want to learn to improve your job profile in the {field_of_interest} field?"
        completion = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content

class ProjectRecommendationAgent:
    def recommend_projects(self, field_of_interest):
        prompt = f"What are some projects you can build to improve your profile in the {field_of_interest} field?"
        completion = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content

def read_docx_file(file):
    try:
        document = Document(file)
        full_text = []
        for paragraph in document.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_resume', methods=['POST'])
def process_resume():
    resume_text = ""
    option = request.form.get('option')
    field_of_interest = request.form.get('field_of_interest', '')

    if 'resume_file' in request.files:
        file = request.files['resume_file']
        if file.filename:
            resume_text = read_docx_file(file)
    else:
        resume_text = request.form.get('resume_text')

    if not resume_text:
        return jsonify({'error': 'Please fill in the resume text or upload a valid resume file.'}), 400

    if option == 'field_of_interest' and not field_of_interest:
        return jsonify({'error': 'Please fill in the Field of Interest.'}), 400

    resume_analysis_agent = ResumeAnalysisAgent()
    edit_suggestion_agent = EditSuggestionAgent()
    skill_recommendation_agent = SkillRecommendationAgent()
    project_recommendation_agent = ProjectRecommendationAgent()

    analysis_feedback = resume_analysis_agent.analyze_resume(resume_text)
    edit_suggestions = edit_suggestion_agent.suggest_edits(resume_text)

    skills_to_learn = ''
    projects_to_build = ''

    if option == 'field_of_interest' and field_of_interest:
        skills_to_learn = skill_recommendation_agent.recommend_skills(field_of_interest)
        projects_to_build = project_recommendation_agent.recommend_projects(field_of_interest)

    # Convert Markdown to HTML
    analysis_feedback_html = markdown.markdown(analysis_feedback)
    edit_suggestions_html = markdown.markdown(edit_suggestions)
    skills_to_learn_html = markdown.markdown(skills_to_learn)
    projects_to_build_html = markdown.markdown(projects_to_build)

    return jsonify({
        'analysis_feedback': analysis_feedback_html,
        'edit_suggestions': edit_suggestions_html,
        'skills_to_learn': skills_to_learn_html,
        'projects_to_build': projects_to_build_html
    })

if __name__ == '__main__':
    app.run(debug=True)
