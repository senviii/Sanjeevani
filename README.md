# Sanjeevani 🌿
### A Transparent, Multilingual AI Health Transparency Platform


Sanjeevani is a Flask-based healthcare web application that prioritizes **explainability and user trust** in AI-driven health tools. It combines NLP-powered symptom checking, multilingual support, and encrypted health record management — with full transparency into how AI decisions are made.

---

## Features

- **Symptom Checker** — NLP-based symptom analysis with explainable AI output (VADER sentiment + classification)
- **Multilingual Support** — Auto-detects and supports multiple languages via `langdetect`
- **Encrypted Health Logs** — User health records encrypted with Fernet symmetric encryption
- **Secure Authentication** — Session management with HTTPONLY cookies, SAMESITE policy, and hashed credentials
- **Hospital Finder** — Nearby hospital locator interface
- **Wellness Dashboard** — Personalized wellness tracking and recommendations
- **Onboarding Flow** — Guided user setup with profile configuration
- **Emergency Module** — Quick-access emergency information page

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask 2.3 |
| Frontend | HTML5, CSS3, Jinja2 Templates |
| Database | SQLite (via SQLAlchemy) |
| NLP | VADER Sentiment, scikit-learn, NLTK |
| Security | Cryptography (Fernet), Hashlib, Secrets |
| Language Detection | langdetect |

---

## Project Structure

```
sanjeevani/
├── app.py                  # Main Flask application
├── setup.py                # Database initialization
├── setup_sprint3.py        # Sprint 3 schema migrations
├── requirements.txt        # Python dependencies
├── templates/
│   ├── home.html
│   ├── onboarding.html
│   ├── symptom_checker.html
│   ├── health_log.html
│   ├── hospitals.html
│   ├── wellness.html
│   ├── multilingual.html
│   ├── profile.html
│   ├── security.html
│   └── emergency.html
└── static/                 # CSS, JS, assets
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/senviii/sanjeevani.git
cd sanjeevani
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```
SECRET_KEY=your_secret_key_here
```
> ⚠️ Never commit `.env` or `secret.key` to version control.

### 5. Initialize the database
```bash
python setup.py
python setup_sprint3.py
```

### 6. Run the application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## Security Design

- Passwords stored as SHA-256 hashes
- Health records encrypted with Fernet symmetric encryption
- Session cookies set with `HTTPONLY=True` and `SAMESITE=Lax`
- Session lifetime capped at 15 minutes
- Secret key loaded from environment variable (never hardcoded)

---

## Research

This project was submitted to **CEECT 2026** (IEEE Conference on Emerging Engineering and Computing Technologies) as a paper on AI transparency in healthcare NLP systems.

---

## Author

**Saanvi** — B.Tech CSE, SRMIST Chennai  
GitHub: [@senviii](https://github.com/senviii)

---

## License

This project is licensed under the MIT License.
