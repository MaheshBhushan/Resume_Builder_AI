from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import markdown
from docx import Document

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

def get_openai_client(api_key, api_endpoint):
    # Special handling for Gemini API
    if "generativelanguage.googleapis.com" in api_endpoint:
        return OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/",
            api_key=api_key,
            default_headers={"x-goog-api-key": api_key}
        )
    return OpenAI(
        base_url=api_endpoint,
        api_key=api_key,
    )

class ResumeAnalysisAgent:
    def analyze_resume(self, resume_text, client, model):
        prompt = f"Analyze the following resume and provide an strong analysis of strengths and weaknesses along with pointers on which aspect needs improvement(Note: Makes sure to mention in points and only top 5 among them but dont mention they are top 5):\n\n{resume_text}"
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content

class EditSuggestionAgent:
    def suggest_edits(self, resume_text, client, model):
        prompt = f"Suggest edits for the following resume to make it more polished and effective:\n\n{resume_text}"
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content

class SkillRecommendationAgent:
    def recommend_skills(self, field_of_interest, client, model):
        prompt = f"What are some additional skills you might want to learn to improve your job profile in the {field_of_interest} field?"
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content

class ProjectRecommendationAgent:
    def recommend_projects(self, field_of_interest, client, model):
        prompt = f"What are some projects you can build to improve your profile in the {field_of_interest} field?"
        completion = client.chat.completions.create(
            model=model,
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
    # Validate API configuration first
    api_key = request.form.get('api_key')
    model = request.form.get('model')
    api_endpoint = request.form.get('api_endpoint')

    if not api_key:
        return jsonify({'error': 'Please enter your API key.'}), 400
    if not model:
        return jsonify({'error': 'Please enter the model name.'}), 400
    if not api_endpoint:
        return jsonify({'error': 'Please enter the API endpoint.'}), 400

    # Get other form data
    resume_text = ""
    option = request.form.get('option')
    field_of_interest = request.form.get('field_of_interest', '')

    # Validate resume input
    if 'resume_file' in request.files:
        file = request.files['resume_file']
        if file.filename:
            resume_text = read_docx_file(file)
    else:
        resume_text = request.form.get('resume_text')

    if not resume_text:
        return jsonify({'error': 'Please fill in the resume text or upload a valid resume file.'}), 400

    # Validate field of interest if that option is selected
    if option == 'field_of_interest':
        if not field_of_interest:
            return jsonify({'error': 'Please fill in the Field of Interest.'}), 400

    try:
        # Initialize API client
        client = get_openai_client(api_key, api_endpoint)

        # Initialize agents
        resume_analysis_agent = ResumeAnalysisAgent()
        edit_suggestion_agent = EditSuggestionAgent()
        skill_recommendation_agent = SkillRecommendationAgent()
        project_recommendation_agent = ProjectRecommendationAgent()

        # Process resume analysis and edit suggestions
        analysis_feedback = resume_analysis_agent.analyze_resume(resume_text, client, model)
        edit_suggestions = edit_suggestion_agent.suggest_edits(resume_text, client, model)

        skills_to_learn = ''
        projects_to_build = ''

        # Process additional recommendations if field of interest is provided
        if option == 'field_of_interest' and field_of_interest:
            skills_to_learn = skill_recommendation_agent.recommend_skills(field_of_interest, client, model)
            projects_to_build = project_recommendation_agent.recommend_projects(field_of_interest, client, model)

        # Convert responses to HTML
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
    except Exception as e:
        error_message = str(e)
        if "API key" in error_message.lower():
            return jsonify({'error': 'Invalid API key. Please check your API key and try again.'}), 400
        elif "model" in error_message.lower():
            return jsonify({'error': 'Invalid model name. Please check the model name and try again.'}), 400
        elif "endpoint" in error_message.lower():
            return jsonify({'error': 'Invalid API endpoint. Please check the endpoint URL and try again.'}), 400
        else:
            return jsonify({'error': f'An error occurred: {error_message}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
