# Creative Resume Builder with AI Integration

An interactive web application that helps users analyze and improve their resumes using various AI providers (Nebius AI, OpenAI, Google Gemini, or custom providers).

## Features

- 🤖 Multiple AI Provider Support
  - Nebius AI Studio
  - OpenAI
  - Google Gemini
  - Custom Provider option
- 📄 Resume Analysis
  - Strengths and weaknesses analysis
  - Improvement suggestions
  - Skills recommendations
  - Project ideas
- 📝 Input Methods
  - File upload (.docx format)
  - Text paste
- 🌓 Dark/Light Mode
- 💡 Additional Features
  - Field of Interest analysis
  - Job Description matching
  - Real-time processing
  - Interactive UI

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Resume_Builder_AI.git
cd Resume_Builder_AI
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python main.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

3. In the web interface:
   - Select your preferred AI provider
   - Enter your API key
   - Choose additional options (Field of Interest/Job Description) if needed
   - Upload or paste your resume
   - Click Submit to get the analysis

## Supported AI Providers

### Nebius AI Studio
- Default Model: meta-llama/Llama-3.3-70B-Instruct-fast
- Endpoint: https://api.studio.nebius.ai/v1

### OpenAI
- Default Model: gpt-3.5-turbo
- Endpoint: https://api.openai.com/v1

### Google Gemini
- Default Model: gemini-1.5-pro
- Endpoint: https://generativelanguage.googleapis.com/v1beta/models

### Custom Provider
- Allows configuration of custom endpoints and models

## API Keys

You'll need to obtain API keys from your chosen provider:
- For Nebius AI: [Nebius AI Studio](https://studio.nebius.ai/)
- For OpenAI: [OpenAI Platform](https://platform.openai.com/)
- For Google Gemini: [Google AI Studio](https://makersuite.google.com/app/apikey)

## File Support

- Currently supports .docx files for resume uploads
- Plain text can be pasted directly into the interface

## Contributing

Feel free to open issues or submit pull requests for any improvements.


## Security Note

- API keys are handled securely and are not stored
- All processing is done server-side
- HTTPS is recommended for production deployment

## Troubleshooting

Common issues and solutions:
1. **API Key Error**: Ensure your API key is valid and has necessary permissions
2. **File Upload Issues**: Check if the file is in .docx format
3. **Model Errors**: Verify the model name is correct for your chosen provider
4. **Connection Issues**: Check your internet connection and API endpoint accessibility 