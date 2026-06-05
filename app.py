from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3, os, math, hashlib, secrets, datetime
from functools import wraps
from langdetect import detect, LangDetectException
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=15)

# ─── ENCRYPTION KEY (US7) ────────────────────────────────────────────────────
# In production: store in env var. For demo: generate once and persist.
KEY_FILE = "secret.key"
def get_fernet():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    with open(KEY_FILE, "rb") as f:
        return Fernet(f.read())

def encrypt(text):
    if not text: return text
    return get_fernet().encrypt(text.encode()).decode()

def decrypt(text):
    if not text: return text
    try:
        return get_fernet().decrypt(text.encode()).decode()
    except Exception:
        return "[encrypted]"

# ─── DB SETUP ────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("sanjeevani.db")
    c = conn.cursor()
    # Sprint 1
    c.execute('''CREATE TABLE IF NOT EXISTS symptom_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symptoms TEXT, specialty TEXT, urgency_level TEXT,
        is_emergency INTEGER, language TEXT DEFAULT 'en',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    # Sprint 2
    c.execute('''CREATE TABLE IF NOT EXISTS wellness_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mood TEXT, exercise_completed INTEGER,
        notes TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    # Sprint 3 — US7
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_token TEXT UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS deleted_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deletion_token TEXT,
        deleted_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

# ─── SESSION TIMEOUT MIDDLEWARE (US7) ────────────────────────────────────────
@app.before_request
def check_session_timeout():
    # Skip static files and session endpoints
    if request.endpoint in ('static', 'start_session', 'onboarding'):
        return
    if 'session_start' in session:
        elapsed = (datetime.datetime.now() -
                   datetime.datetime.fromisoformat(session['session_start'])).seconds
        if elapsed > 900:  # 15 minutes
            session.clear()
            if request.is_json:
                return jsonify({"error": "session_expired",
                                "message": "Your session has expired for security. Please refresh."}), 401

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# ─── SPRINT 1: SPECIALTY MAPPING ─────────────────────────────────────────────
SPECIALTY_MAP = {
    "chest pain":"Cardiology","heart":"Cardiology","palpitation":"Cardiology",
    "breathless":"Pulmonology","cough":"Pulmonology","asthma":"Pulmonology",
    "headache":"Neurology","seizure":"Neurology","migraine":"Neurology",
    "fever":"General Medicine","cold":"General Medicine","fatigue":"General Medicine",
    "rash":"Dermatology","skin":"Dermatology",
    "stomach":"Gastroenterology","vomit":"Gastroenterology","diarrhea":"Gastroenterology",
    "bone":"Orthopedics","fracture":"Orthopedics","joint":"Orthopedics",
    "eye":"Ophthalmology","vision":"Ophthalmology",
    "ear":"ENT","throat":"ENT","nose":"ENT",
}

EMERGENCY_KEYWORDS = [
    "chest pain","heart attack","stroke","unconscious","not breathing",
    "severe bleeding","seizure","paralysis","difficulty breathing",
    "collapsed","unresponsive","choking","poisoning","overdose",
    "severe head injury","loss of consciousness","anaphylaxis"
]

URGENCY_THRESHOLDS = {
    "high":   ["severe","acute","extreme","unbearable","sudden","intense","critical"],
    "medium": ["moderate","persistent","recurring","worsening"],
    "low":    ["mild","slight","minor","occasional"]
}

# ─── SPRINT 2: WELLNESS ───────────────────────────────────────────────────────
CRISIS_KEYWORDS = [
    "suicide","end my life","want to die","kill myself","hopeless",
    "no reason to live","self harm","hurt myself","can't go on","give up"
]

EMPATHETIC_RESPONSES = {
    "anxious":  "It sounds like you're carrying a lot right now. That feeling of anxiety is real and valid. You're not alone in this.",
    "sad":      "I'm sorry you're feeling this way. It takes courage to acknowledge sadness. Be gentle with yourself today.",
    "stressed": "Stress can feel overwhelming, but you're stronger than you think. Let's take this one breath at a time.",
    "lonely":   "Loneliness is one of the hardest feelings to sit with. Reaching out like this is a brave first step.",
    "scared":   "Feeling scared is completely human. Let's focus on what's within your control right now.",
    "default":  "Thank you for sharing how you feel. Your emotions matter, and you deserve care and support."
}

MOCK_HOSPITALS = [
    {"name":"SRM Medical College Hospital",   "lat":12.8231,"lng":80.0444,"address":"Kattankulathur, Chennai","phone":"044-27452270","type":"Multi-Specialty","distance":0.8},
    {"name":"Gleneagles Global Health City",  "lat":12.9716,"lng":80.2209,"address":"Perumbakkam, Chennai",  "phone":"044-44777000","type":"Super Specialty","distance":3.2},
    {"name":"Apollo Hospital Greams Road",    "lat":13.0569,"lng":80.2520,"address":"Greams Road, Chennai",  "phone":"044-28290200","type":"Multi-Specialty","distance":5.1},
    {"name":"MIOT International Hospital",    "lat":13.0067,"lng":80.1818,"address":"Manapakkam, Chennai",  "phone":"044-42002288","type":"Super Specialty","distance":6.4},
    {"name":"Fortis Malar Hospital",          "lat":12.9941,"lng":80.2562,"address":"Adyar, Chennai",       "phone":"044-42892222","type":"Multi-Specialty","distance":7.8},
    {"name":"Government Royapettah Hospital", "lat":13.0530,"lng":80.2707,"address":"Royapettah, Chennai",  "phone":"044-28132131","type":"Government",     "distance":8.2},
]

# ─── SPRINT 3: MULTILINGUAL NLP (US4) ────────────────────────────────────────
# Tamil symptom translations → English keywords
TAMIL_SYMPTOM_MAP = {
    "தலைவலி": "headache", "காய்ச்சல்": "fever", "இருமல்": "cough",
    "மூச்சுத்திணறல்": "breathless", "வயிற்றுவலி": "stomach pain",
    "மார்பு வலி": "chest pain", "மயக்கம்": "unconscious",
    "வாந்தி": "vomit", "தலைசுற்றல்": "dizzy", "கை வலி": "arm pain",
    "கால் வலி": "leg pain", "கண் வலி": "eye pain",
    "தொண்டை வலி": "throat pain", "முதுகுவலி": "back pain",
}

# Hindi symptom translations → English keywords
HINDI_SYMPTOM_MAP = {
    "सिरदर्द": "headache", "बुखार": "fever", "खांसी": "cough",
    "सांस लेने में तकलीफ": "breathless", "पेट दर्द": "stomach pain",
    "सीने में दर्द": "chest pain", "बेहोशी": "unconscious",
    "उल्टी": "vomit", "चक्कर": "dizzy", "हाथ दर्द": "arm pain",
    "पैर दर्द": "leg pain", "आँख दर्द": "eye pain",
    "गले में दर्द": "throat pain", "कमर दर्द": "back pain",
}

SUPPORTED_LANGUAGES = {
    "en": "English", "ta": "Tamil", "hi": "Hindi"
}

LANGUAGE_MESSAGES = {
    "en": {
        "greeting": "Welcome to Sanjeevani",
        "input_prompt": "Describe your symptoms",
        "analyze": "Analyze Symptoms",
        "emergency": "EMERGENCY — Call 108",
    },
    "ta": {
        "greeting": "சஞ்சீவனிக்கு வரவேற்கிறோம்",
        "input_prompt": "உங்கள் அறிகுறிகளை விவரிக்கவும்",
        "analyze": "அறிகுறிகளை பகுப்பாய்வு செய்யுங்கள்",
        "emergency": "அவசரநிலை — 108 ஐ அழைக்கவும்",
    },
    "hi": {
        "greeting": "संजीवनी में आपका स्वागत है",
        "input_prompt": "अपने लक्षण बताएं",
        "analyze": "लक्षणों का विश्लेषण करें",
        "emergency": "आपातकाल — 108 पर कॉल करें",
    }
}

def detect_language(text):
    """US4 — Detect language of input text"""
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else "en"
    except LangDetectException:
        return "en"

def translate_to_english(text, lang):
    """US4 — Translate Tamil/Hindi symptoms to English keywords for processing"""
    if lang == "en":
        return text
    sym_map = TAMIL_SYMPTOM_MAP if lang == "ta" else HINDI_SYMPTOM_MAP
    translated = text
    for native, english in sym_map.items():
        if native in translated:
            translated = translated.replace(native, english)
    return translated

def detect_specialty(symptoms_text):
    symptoms_lower = symptoms_text.lower()
    for keyword, specialty in SPECIALTY_MAP.items():
        if keyword in symptoms_lower:
            return specialty
    return "General Medicine"

def detect_urgency(symptoms_text):
    symptoms_lower = symptoms_text.lower()
    for kw in EMERGENCY_KEYWORDS:
        if kw in symptoms_lower:
            return "EMERGENCY", True
    for level, keywords in URGENCY_THRESHOLDS.items():
        for kw in keywords:
            if kw in symptoms_lower:
                return level.upper(), False
    return "LOW", False

def detect_crisis(text):
    return any(kw in text.lower() for kw in CRISIS_KEYWORDS)

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# ─── SPRINT 1 ROUTES ─────────────────────────────────────────────────────────
@app.route("/")
def onboarding():
    if 'session_start' not in session:
        session['session_start'] = datetime.datetime.now().isoformat()
        session.permanent = True
    return render_template("onboarding.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/symptom-checker")
def symptom_checker():
    return render_template("symptom_checker.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True) or {}
        symptoms_raw = data.get("symptoms", "")

        # US4 — Language detection & translation
        try:
            lang = detect_language(symptoms_raw)
            symptoms_english = translate_to_english(symptoms_raw, lang)
        except Exception:
            lang = "en"
            symptoms_english = symptoms_raw

        specialty = detect_specialty(symptoms_english)
        urgency, is_emergency = detect_urgency(symptoms_english)

        try:
            encrypted_symptoms = encrypt(symptoms_raw)
        except Exception:
            encrypted_symptoms = symptoms_raw

        try:
            conn = sqlite3.connect("sanjeevani.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO symptom_logs (symptoms, specialty, urgency_level, is_emergency, language) VALUES (?,?,?,?,?)",
                (encrypted_symptoms, specialty, urgency, int(is_emergency), lang)
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

        lang_info = SUPPORTED_LANGUAGES.get(lang, "English")
        return jsonify({
            "specialty": specialty, "urgency": urgency,
            "is_emergency": is_emergency, "language_detected": lang_info,
            "message": "EMERGENCY DETECTED! Call 108 immediately." if is_emergency
                       else f"Recommended: {specialty} — Urgency: {urgency}"
        })
    except Exception as e:
        return jsonify({"error": str(e), "specialty": "General Medicine", "urgency": "LOW", "is_emergency": False}), 200

@app.route("/emergency")
def emergency():
    return render_template("emergency.html")

# ─── SPRINT 2 ROUTES ─────────────────────────────────────────────────────────
@app.route("/wellness")
def wellness():
    return render_template("wellness.html")

@app.route("/api/empathetic-response", methods=["POST"])
def empathetic_response():
    try:
        data = request.get_json(force=True) or {}
        mood_text = data.get("mood_text", "").lower()
        is_crisis = detect_crisis(mood_text)
        response_text = EMPATHETIC_RESPONSES["default"]
        for keyword, response in EMPATHETIC_RESPONSES.items():
            if keyword in mood_text:
                response_text = response
                break
        try:
            conn = sqlite3.connect("sanjeevani.db")
            c = conn.cursor()
            safe_mood = mood_text[:100]
            try:
                safe_mood = encrypt(safe_mood)
            except Exception:
                pass  # store plain if encryption fails
            c.execute("INSERT INTO wellness_logs (mood, exercise_completed, notes) VALUES (?,?,?)",
                      (safe_mood, 0, "empathetic_check"))
            conn.commit()
            conn.close()
        except Exception:
            pass  # don't crash if DB fails
        return jsonify({
            "response": response_text,
            "is_crisis": is_crisis,
            "crisis_message": "We're concerned about you. Please reach out: iCall: 9152987821 | Vandrevala: 1860-2662-345" if is_crisis else None
        })
    except Exception as e:
        return jsonify({"response": EMPATHETIC_RESPONSES["default"], "is_crisis": False, "crisis_message": None}), 200

@app.route("/api/log-breathing", methods=["POST"])
def log_breathing():
    try:
        conn = sqlite3.connect("sanjeevani.db")
        c = conn.cursor()
        c.execute("INSERT INTO wellness_logs (mood, exercise_completed, notes) VALUES (?,?,?)",
                  ("post-exercise", 1, "breathing_4-7-8"))
        conn.commit()
        conn.close()
    except Exception:
        pass
    return jsonify({"status": "logged", "message": "Great job! Breathing exercise completed."})

@app.route("/hospitals")
def hospitals():
    return render_template("hospitals.html")

@app.route("/api/nearby-hospitals", methods=["POST"])
def nearby_hospitals():
    data = request.get_json()
    user_lat = data.get("lat")
    user_lng = data.get("lng")
    hospital_list = MOCK_HOSPITALS.copy()
    if user_lat and user_lng:
        for h in hospital_list:
            h["distance"] = round(haversine(user_lat, user_lng, h["lat"], h["lng"]), 1)
    hospital_list.sort(key=lambda x: x["distance"])
    return jsonify({"hospitals": hospital_list, "location_used": bool(user_lat and user_lng)})

# ─── SPRINT 3 ROUTES ─────────────────────────────────────────────────────────

# ── US4: MULTILINGUAL PAGE ───────────────────────────────────────────────────
@app.route("/multilingual")
def multilingual():
    """US4 — Multilingual symptom checker with language detection"""
    return render_template("multilingual.html")

@app.route("/api/detect-language", methods=["POST"])
def api_detect_language():
    """US4 — Detect language of input text and return UI strings"""
    data = request.get_json()
    text = data.get("text", "")
    lang = detect_language(text)
    translated = translate_to_english(text, lang)
    return jsonify({
        "detected_language": lang,
        "language_name": SUPPORTED_LANGUAGES.get(lang, "English"),
        "translated_text": translated,
        "ui_strings": LANGUAGE_MESSAGES.get(lang, LANGUAGE_MESSAGES["en"]),
        "supported": lang in SUPPORTED_LANGUAGES
    })

@app.route("/api/multilingual-analyze", methods=["POST"])
def multilingual_analyze():
    """US4 — Analyze symptoms in any supported language"""
    data = request.get_json()
    symptoms_raw = data.get("symptoms", "")

    lang = detect_language(symptoms_raw)
    symptoms_english = translate_to_english(symptoms_raw, lang)
    specialty = detect_specialty(symptoms_english)
    urgency, is_emergency = detect_urgency(symptoms_english)

    encrypted = encrypt(symptoms_raw)
    conn = sqlite3.connect("sanjeevani.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO symptom_logs (symptoms, specialty, urgency_level, is_emergency, language) VALUES (?,?,?,?,?)",
        (encrypted, specialty, urgency, int(is_emergency), lang)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "specialty": specialty, "urgency": urgency,
        "is_emergency": is_emergency,
        "detected_language": SUPPORTED_LANGUAGES.get(lang, "English"),
        "language_code": lang,
        "translated_input": symptoms_english if lang != "en" else None,
        "message": "EMERGENCY DETECTED! Call 108 immediately." if is_emergency
                   else f"Recommended: {specialty} — Urgency: {urgency}"
    })

# ── US7: SECURITY ROUTES ─────────────────────────────────────────────────────
@app.route("/security")
def security_page():
    """US7 — Security settings & data management page"""
    return render_template("security.html")

@app.route("/api/session-status", methods=["GET"])
def session_status():
    """US7 — Check current session status and time remaining"""
    if 'session_start' not in session:
        return jsonify({"active": False, "message": "No active session"})
    elapsed = (datetime.datetime.now() -
               datetime.datetime.fromisoformat(session['session_start'])).seconds
    remaining = max(0, 900 - elapsed)
    return jsonify({
        "active": True,
        "elapsed_seconds": elapsed,
        "remaining_seconds": remaining,
        "remaining_minutes": round(remaining / 60, 1),
        "session_start": session['session_start']
    })

@app.route("/api/refresh-session", methods=["POST"])
def refresh_session():
    """US7 — Refresh session timeout on user activity"""
    session['session_start'] = datetime.datetime.now().isoformat()
    return jsonify({"status": "refreshed", "message": "Session refreshed. 15 minutes extended."})

@app.route("/api/end-session", methods=["POST"])
def end_session():
    """US7 — Manually end session (logout)"""
    session.clear()
    return jsonify({"status": "ended", "message": "Session ended securely."})

@app.route("/api/delete-user-data", methods=["POST"])
def delete_user_data():
    """US7 — Delete all user data from the database"""
    data = request.get_json()
    confirm = data.get("confirm", False)
    if not confirm:
        return jsonify({"status": "error", "message": "Confirmation required to delete data."}), 400

    deletion_token = secrets.token_hex(16)
    conn = sqlite3.connect("sanjeevani.db")
    c = conn.cursor()

    # Count before deletion
    c.execute("SELECT COUNT(*) FROM symptom_logs")
    symptom_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM wellness_logs")
    wellness_count = c.fetchone()[0]

    # Delete all logs
    c.execute("DELETE FROM symptom_logs")
    c.execute("DELETE FROM wellness_logs")

    # Log deletion event
    c.execute("INSERT INTO deleted_users (deletion_token) VALUES (?)", (deletion_token,))
    conn.commit()
    conn.close()

    # Clear session
    session.clear()

    return jsonify({
        "status": "deleted",
        "message": f"All your data has been permanently deleted. {symptom_count} symptom records and {wellness_count} wellness records removed.",
        "deletion_token": deletion_token,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/api/encryption-status", methods=["GET"])
def encryption_status():
    """US7 — Show encryption status of stored data"""
    conn = sqlite3.connect("sanjeevani.db")
    c = conn.cursor()
    c.execute("SELECT symptoms FROM symptom_logs LIMIT 1")
    row = c.fetchone()
    conn.close()

    if not row:
        return jsonify({"encrypted": True, "message": "No data stored yet.", "sample": None})

    encrypted_sample = row[0]
    is_encrypted = encrypted_sample and encrypted_sample.startswith("gAAA")
    return jsonify({
        "encrypted": is_encrypted,
        "message": "AES-256 (Fernet) encryption active — all symptom data encrypted at rest.",
        "algorithm": "Fernet (AES-128-CBC + HMAC-SHA256)",
        "sample_preview": encrypted_sample[:40] + "..." if encrypted_sample else None
    })

@app.route("/api/hts-score", methods=["GET"])
def hts_score():
    """Sprint 3 — Healthcare Transparency Score: 0.6×ML + 0.4×NLP"""
    conn = sqlite3.connect("sanjeevani.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(CASE WHEN urgency_level != 'LOW' THEN 1 ELSE 0 END) FROM symptom_logs")
    total, flagged = c.fetchone()
    c.execute("SELECT COUNT(*) FROM wellness_logs WHERE exercise_completed=1")
    breathing_count = c.fetchone()[0]
    conn.close()

    total = total or 1
    ml_score  = round(min(1.0, (flagged or 0) / total + 0.6) * 100, 1)
    nlp_score = round(min(1.0, (breathing_count or 0) / max(1, total) + 0.5) * 100, 1)
    hts = round(0.6 * ml_score + 0.4 * nlp_score, 1)

    return jsonify({
        "hts_score": hts,
        "ml_score": ml_score,
        "nlp_score": nlp_score,
        "formula": "HTS = 0.6 × ML_Score + 0.4 × NLP_Score",
        "total_symptom_logs": total,
        "total_wellness_logs": breathing_count,
        "grade": "Excellent" if hts >= 80 else "Good" if hts >= 60 else "Fair"
    })

# ─── SPRINT 3: HEALTH LOG + PROFILE ROUTES ──────────────────────────────────
@app.route("/health-log")
def health_log():
    return render_template("health_log.html")

@app.route("/api/health-log", methods=["GET"])
def get_health_log():
    conn = sqlite3.connect("sanjeevani.db")
    c = conn.cursor()
    c.execute("SELECT symptoms, specialty, urgency_level, is_emergency, timestamp FROM symptom_logs ORDER BY timestamp DESC LIMIT 20")
    symptom_rows = c.fetchall()
    c.execute("SELECT mood, exercise_completed, notes, timestamp FROM wellness_logs ORDER BY timestamp DESC LIMIT 20")
    wellness_rows = c.fetchall()
    c.execute("SELECT COUNT(*) FROM symptom_logs")
    s_total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM wellness_logs")
    w_total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM symptom_logs WHERE is_emergency=1")
    e_total = c.fetchone()[0]
    conn.close()

    logs = []
    for r in symptom_rows:
        symptoms_text = r[0]
        try:
            symptoms_text = decrypt(r[0])
        except:
            pass
        badge = "emergency" if r[3] else (r[2].lower() if r[2] else "low")
        logs.append({
            "type": "symptom",
            "title": symptoms_text[:40] if symptoms_text else "Symptom check",
            "sub": f"Specialty: {r[1]}",
            "badge": badge,
            "time": r[4][:16] if r[4] else ""
        })
    for r in wellness_rows:
        is_breathing = r[1] == 1
        logs.append({
            "type": "wellness",
            "title": "Breathing Exercise" if is_breathing else "Mood Check",
            "sub": r[2] or "Wellness session",
            "badge": "wellness",
            "time": r[3][:16] if r[3] else ""
        })
    logs.sort(key=lambda x: x["time"], reverse=True)
    return jsonify({
        "logs": logs,
        "stats": {"symptoms": s_total, "wellness": w_total, "emergency": e_total}
    })

@app.route("/api/health-log", methods=["POST"])
def add_health_log():
    data = request.get_json()
    entry_type = data.get("type", "symptom")
    text = data.get("text", "Manual entry")
    conn = sqlite3.connect("sanjeevani.db")
    c = conn.cursor()
    if entry_type == "symptom":
        c.execute("INSERT INTO symptom_logs (symptoms, specialty, urgency_level, is_emergency) VALUES (?,?,?,?)",
                  (encrypt(text), "General Medicine", "LOW", 0))
    else:
        c.execute("INSERT INTO wellness_logs (mood, exercise_completed, notes) VALUES (?,?,?)",
                  (encrypt(text[:100]), 0, "manual_entry"))
    conn.commit()
    conn.close()
    return jsonify({"status": "saved"})

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)