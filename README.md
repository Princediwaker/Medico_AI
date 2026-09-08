# 🩺 AI Health Assistant

A simple Streamlit-based AI Health Assistant for answering general health and wellness questions.

## Features

- Interactive chat interface
- Answers questions about:
  - Sleep
  - BMI
  - Hydration
  - Exercise
  - General wellness
- Uses an LLM through the OpenAI API
- Includes a medical-safety disclaimer
- Collects student's Name and Registration Number
- Ready for Streamlit Community Cloud deployment

## Files

- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your_api_key_here"
```

Do NOT upload your API key to GitHub.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py` and `requirements.txt`.
3. Open Streamlit Community Cloud.
4. Create a new app and select your GitHub repository.
5. Set the main file to `app.py`.
6. In Advanced settings / Secrets, add:

```toml
OPENAI_API_KEY = "your_api_key_here"
```

7. Deploy.
8. Copy the generated `https://....streamlit.app` URL for submission.

## Submission format

Name: YOUR NAME  
Registration No.: YOUR REGISTRATION NUMBER  
Streamlit App Link: YOUR STREAMLIT LINK
