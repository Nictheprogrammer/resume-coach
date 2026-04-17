from flask import Flask, request, jsonify, render_template
from anthropic import Anthropic
from dotenv import load_dotenv
import pdfplumber
import io
import os
import json

load_dotenv()

app = Flask(__name__)
client = Anthropic()

SYSTEM_PROMPT = """You are an expert resume coach and hiring specialist with 15+ years of experience. 
You analyze resumes against job descriptions and provide precise, actionable feedback.
Always respond in valid JSON only — no extra text, no markdown, no code fences."""

def analyze_resume(resume: str, job_description: str) -> dict:
    prompt = f"""Analyze this resume against the job description and return a JSON object with exactly these fields:

{{
  "match_score": <integer 0-100>,
  "summary": "<2 sentence overall assessment>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "gaps": ["<missing skill or experience 1>", "<gap 2>", "<gap 3>"],
  "keywords_missing": ["<important keyword from JD not in resume>", ...],
  "top_suggestion": "<the single most impactful change the candidate should make>",
  "category_scores": {{
    "skills_match": <integer 0-100>,
    "experience": <integer 0-100>,
    "keywords": <integer 0-100>,
    "presentation": <integer 0-100>,
    "culture_fit": <integer 0-100>
  }}
}}

Scoring guide for category_scores:
- skills_match: how well the candidate's technical skills match the job requirements
- experience: how relevant and sufficient their work experience is
- keywords: how many important ATS keywords from the JD appear in the resume
- presentation: clarity, structure, formatting quality of the resume
- culture_fit: how well their background and tone aligns with the company's culture

JOB DESCRIPTION:
{job_description}

RESUME:
{resume}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(message.content[0].text)


def generate_cover_letter(resume: str, job_description: str) -> str:
    prompt = f"""Write a compelling, personalized cover letter for this candidate applying to this role.

Rules:
- 3 paragraphs max
- Match the tone of the job description
- Lead with the most relevant experience
- End with a confident call to action
- Do NOT use generic phrases like "I am writing to express my interest"
- Return only the cover letter text, no subject line or date

JOB DESCRIPTION:
{job_description}

RESUME:
{resume}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="You are an expert cover letter writer. Write naturally and specifically — never generically.",
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def rewrite_bullets(resume: str, job_description: str) -> dict:
    prompt = f"""You are a resume expert. Extract all bullet points from this resume and rewrite the weak ones to be stronger.

Rules for rewriting:
- Start with a strong action verb
- Add metrics or impact where possible (even estimated ones like "reduced X by ~30%")
- Make it relevant to the job description
- Keep it concise (one line)
- Only rewrite bullets that are vague, weak, or missing impact

Return a JSON object with exactly this structure:
{{
  "bullets": [
    {{
      "original": "<exact original bullet point text>",
      "rewritten": "<improved version>",
      "weak": <true if this bullet needed improvement, false if it was already strong>
    }},
    ...
  ]
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(message.content[0].text)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["file"]
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported."}), 400

    text = ""
    with pdfplumber.open(io.BytesIO(file.read())) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        return jsonify({"error": "Could not extract text from this PDF."}), 400

    return jsonify({"text": text.strip()})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    resume = data.get("resume", "").strip()
    job_description = data.get("job_description", "").strip()

    if not resume or not job_description:
        return jsonify({"error": "Both resume and job description are required."}), 400

    if len(resume) < 100:
        return jsonify({"error": "Resume seems too short. Please paste the full text."}), 400

    result = analyze_resume(resume, job_description)
    return jsonify(result)


@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.json
    resume = data.get("resume", "").strip()
    job_description = data.get("job_description", "").strip()

    if not resume or not job_description:
        return jsonify({"error": "Both resume and job description are required."}), 400

    result = rewrite_bullets(resume, job_description)
    return jsonify(result)


@app.route("/cover-letter", methods=["POST"])
def cover_letter():
    data = request.json
    resume = data.get("resume", "").strip()
    job_description = data.get("job_description", "").strip()

    if not resume or not job_description:
        return jsonify({"error": "Both resume and job description are required."}), 400

    letter = generate_cover_letter(resume, job_description)
    return jsonify({"cover_letter": letter})


if __name__ == "__main__":
    app.run(debug=True)