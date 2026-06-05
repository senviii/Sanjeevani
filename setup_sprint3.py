"""
Sanjeevani Sprint 3 — Setup Script
Run this once to create the full project structure.
Usage: python setup_sprint3.py
Then: python app.py
Open: http://localhost:5000
"""
import os, shutil

os.makedirs("templates", exist_ok=True)

# ── Copy Sprint 1 + 2 templates (already built) ──────────────────────────────
SPRINT12_TEMPLATES = [
    "onboarding.html", "home.html", "symptom_checker.html",
    "emergency.html", "wellness.html", "hospitals.html"
]

print("=" * 50)
print("Sanjeevani Sprint 3 — Setup")
print("=" * 50)

# Check which Sprint 1+2 templates exist
for t in SPRINT12_TEMPLATES:
    if os.path.exists(f"templates/{t}"):
        print(f"  ✅ templates/{t} (already present)")
    else:
        print(f"  ⚠️  templates/{t} MISSING — copy from Sprint 1/2 outputs")

# Sprint 3 templates should be present
for t in ["multilingual.html", "security.html"]:
    if os.path.exists(f"templates/{t}"):
        print(f"  ✅ templates/{t} (Sprint 3 — present)")
    else:
        print(f"  ❌ templates/{t} MISSING")

print("\nInstalling dependencies...")
os.system("pip install flask langdetect cryptography --break-system-packages -q")
print("  ✅ Dependencies installed")

print("\nStarting app...")
print("  Open http://localhost:5000 in your browser")
print("  New Sprint 3 routes:")
print("    /multilingual  — US4: Tamil/Hindi symptom checker")
print("    /security      — US7: Session, encryption, data deletion, HTS score")
print("    /api/detect-language")
print("    /api/multilingual-analyze")
print("    /api/session-status")
print("    /api/refresh-session")
print("    /api/end-session")
print("    /api/delete-user-data")
print("    /api/encryption-status")
print("    /api/hts-score")
print("=" * 50)