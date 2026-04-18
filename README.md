---
title: Resume Coach
emoji: 📄
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
---

# ResumeIQ — AI Resume Coach

An AI-powered resume coaching tool that analyzes resumes against job descriptions and provides actionable, personalized feedback in seconds.

**Live demo:** [nic79cy-resume-coach.hf.space](https://nic79cy-resume-coach.hf.space)

---

## What it does

Paste a job description and your resume (or upload a PDF) and ResumeIQ will:

- **Score your resume** — an overall match score from 0–100 based on how well you fit the role
- **Break down the score** — individual scores for Skills Match, Experience, Keywords, Presentation, and Culture Fit
- **Identify strengths and gaps** — what's working and what's missing
- **Flag missing keywords** — ATS-critical terms from the job description that aren't in your resume
- **Rewrite weak bullet points** — Claude rewrites vague bullets into strong, metric-driven ones
- **Generate a cover letter** — a personalized, tone-matched cover letter ready to send

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI | Anthropic Claude API (claude-opus-4-5) |
| PDF parsing | pdfplumber |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| Deployment | Docker, Hugging Face Spaces |

---

## How it works

1. User pastes a job description and resume (or uploads a PDF)
2. The resume text is extracted and sent to Claude along with a structured prompt
3. Claude returns a JSON object with scores, strengths, gaps, and missing keywords
4. A second Claude call rewrites weak bullet points using impact-driven language
5. A third call generates a personalized cover letter matched to the role's tone
6. Results are rendered in a clean dashboard with an animated score circle and Chart.js breakdown

---

## Running locally

```bash
git clone https://github.com/Nictheprogrammer/resume-coach.git
cd resume-coach
pip install -r requirements.txt
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
```

Run the app:
```bash
python app.py
```

Open `http://localhost:5000`

---

## Project structure

```
resume-coach/
├── app.py              # Flask backend + Claude API calls
├── templates/
│   └── index.html      # Frontend UI
├── requirements.txt
├── Dockerfile
└── .env                # API key (not committed)
```

---

## Related projects

- [Sign Language Translator](https://github.com/Nictheprogrammer/sign-language-translator) — real-time ASL detection using MediaPipe and a custom MLPClassifier
- [NewsLens](https://github.com/Nictheprogrammer/news-analyzer) — AI-powered news bias and sentiment analyzer with Chrome extension