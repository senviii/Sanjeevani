import os

os.makedirs("templates", exist_ok=True)

# ── onboarding.html ──────────────────────────────────────────────────────────
with open("templates/onboarding.html", "w", encoding="utf-8") as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sanjeevani</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--green:#1a6b4a;--green-light:#2d9b6f;--cream:#fdf8f0;--red:#d63031;--text:#1a1a2e;--muted:#6b7280}
body{font-family:"DM Sans",sans-serif;background:var(--cream);min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden}
.bg-circle{position:fixed;border-radius:50%;opacity:.07;background:var(--green);animation:pulse 6s ease-in-out infinite}
.bg-circle:nth-child(1){width:600px;height:600px;top:-200px;right:-200px}
.bg-circle:nth-child(2){width:400px;height:400px;bottom:-150px;left:-100px;animation-delay:2s}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
.container{position:relative;z-index:1;text-align:center;padding:2rem;max-width:480px;animation:fadeUp .8s ease forwards}
@keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.logo{font-family:"Playfair Display",serif;font-size:3.2rem;color:var(--green);letter-spacing:-1px;margin-bottom:.3rem}
.logo span{color:var(--red)}
.tagline{font-size:1rem;color:var(--muted);margin-bottom:3rem;font-weight:300;letter-spacing:.05em}
.onboard-card{background:white;border-radius:24px;padding:2.5rem 2rem;box-shadow:0 20px 60px rgba(26,107,74,.12);margin-bottom:2rem}
.step{display:flex;align-items:flex-start;gap:1rem;margin-bottom:1.5rem;text-align:left;opacity:0;animation:fadeUp .6s ease forwards}
.step:nth-child(1){animation-delay:.3s}.step:nth-child(2){animation-delay:.5s}.step:nth-child(3){animation-delay:.7s}
.step-icon{width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,var(--green),var(--green-light));display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0}
.step-text h3{font-size:.95rem;font-weight:500;color:var(--text);margin-bottom:.2rem}
.step-text p{font-size:.82rem;color:var(--muted);line-height:1.5}
.btn-primary{display:block;width:100%;padding:1rem;background:linear-gradient(135deg,var(--green),var(--green-light));color:white;border:none;border-radius:14px;font-size:1rem;font-weight:500;font-family:"DM Sans",sans-serif;cursor:pointer;text-decoration:none;transition:transform .2s,box-shadow .2s;box-shadow:0 6px 20px rgba(26,107,74,.3);animation:fadeUp .6s .9s ease forwards;opacity:0}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 10px 28px rgba(26,107,74,.4)}
.disclaimer{font-size:.75rem;color:var(--muted);margin-top:1rem;line-height:1.6}
</style>
</head>
<body>
<div class="bg-circle"></div><div class="bg-circle"></div>
<div class="container">
  <div class="logo">Sanje<span>e</span>vani</div>
  <div class="tagline">Your intelligent health companion</div>
  <div class="onboard-card">
    <div class="step"><div class="step-icon">&#x1F9BA;</div><div class="step-text"><h3>Describe your symptoms</h3><p>Enter what you are experiencing and we will map it to the right specialist instantly.</p></div></div>
    <div class="step"><div class="step-icon">&#x26A1;</div><div class="step-text"><h3>Urgency detection</h3><p>Our system automatically detects critical symptoms and escalates emergencies.</p></div></div>
    <div class="step"><div class="step-icon">&#x1F6A8;</div><div class="step-text"><h3>Emergency support</h3><p>One-tap emergency button connects you to ambulance services instantly.</p></div></div>
  </div>
  <a href="/home" class="btn-primary">Get Started &rarr;</a>
  <p class="disclaimer">Sanjeevani is an AI-assisted triage tool and does not replace professional medical advice.</p>
</div>
</body>
</html>''')

# ── home.html ────────────────────────────────────────────────────────────────
with open("templates/home.html", "w", encoding="utf-8") as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sanjeevani - Home</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--green:#1a6b4a;--green-light:#2d9b6f;--cream:#fdf8f0;--red:#d63031;--text:#1a1a2e;--muted:#6b7280}
body{font-family:"DM Sans",sans-serif;background:var(--cream);min-height:100vh}
header{background:white;padding:1.2rem 1.5rem;display:flex;align-items:center;justify-content:space-between;box-shadow:0 2px 12px rgba(0,0,0,.06);position:sticky;top:0;z-index:10}
.logo{font-family:"Playfair Display",serif;font-size:1.6rem;color:var(--green)}
.logo span{color:var(--red)}
.user-greeting{font-size:.85rem;color:var(--muted)}
.main{padding:1.5rem;max-width:480px;margin:0 auto}
.emergency-btn{width:100%;padding:1.3rem;background:linear-gradient(135deg,var(--red),#c0392b);color:white;border:none;border-radius:18px;font-size:1.1rem;font-weight:500;font-family:"DM Sans",sans-serif;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:.7rem;box-shadow:0 8px 24px rgba(214,48,49,.4);animation:emergPulse 2s infinite;margin-bottom:1.5rem;text-decoration:none}
@keyframes emergPulse{0%,100%{box-shadow:0 8px 24px rgba(214,48,49,.4)}50%{box-shadow:0 8px 40px rgba(214,48,49,.7)}}
.section-title{font-size:.78rem;font-weight:500;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:.8rem}
.card-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem}
.card{background:white;border-radius:16px;padding:1.3rem 1rem;box-shadow:0 4px 16px rgba(0,0,0,.06);text-align:center;cursor:pointer;text-decoration:none;color:var(--text);transition:transform .2s,box-shadow .2s;display:flex;flex-direction:column;align-items:center;gap:.5rem}
.card:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,.1)}
.card .icon{font-size:2rem}
.card h3{font-size:.88rem;font-weight:500}
.card p{font-size:.75rem;color:var(--muted)}
.tip-card{background:linear-gradient(135deg,var(--green),var(--green-light));border-radius:16px;padding:1.3rem;color:white;margin-bottom:1.5rem}
.tip-card h3{font-size:.9rem;font-weight:500;margin-bottom:.4rem;opacity:.85}
.tip-card p{font-size:.82rem;line-height:1.6;opacity:.9}
.bottom-nav{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:.8rem;box-shadow:0 -4px 16px rgba(0,0,0,.08)}
.nav-item{display:flex;flex-direction:column;align-items:center;gap:.2rem;font-size:.7rem;color:var(--muted);text-decoration:none}
.nav-item.active{color:var(--green)}
.nav-icon{font-size:1.3rem}
</style>
</head>
<body>
<header>
  <div class="logo">Sanje<span>e</span>vani</div>
  <div class="user-greeting">Good day, User &#x1F64F;</div>
</header>
<div class="main">
  <a href="/emergency" class="emergency-btn">&#x1F6A8; &nbsp; EMERGENCY &mdash; Call 108</a>
  <div class="section-title">Quick Actions</div>
  <div class="card-grid">
    <a href="/symptom-checker" class="card"><div class="icon">&#x1F9BA;</div><h3>Check Symptoms</h3><p>AI-powered triage</p></a>
    <a href="/emergency" class="card"><div class="icon">&#x1F3E5;</div><h3>Find Hospital</h3><p>Nearby care centers</p></a>
    <a href="#" class="card"><div class="icon">&#x1F48A;</div><h3>Medications</h3><p>Track your meds</p></a>
    <a href="#" class="card"><div class="icon">&#x1F4CB;</div><h3>Health Log</h3><p>Past check-ins</p></a>
  </div>
  <div class="tip-card">
    <h3>&#x1F4A1; Health Tip of the Day</h3>
    <p>Staying hydrated helps maintain blood pressure and reduces fatigue. Aim for 8 glasses of water daily.</p>
  </div>
</div>
<div style="height:80px"></div>
<nav class="bottom-nav">
  <a href="/home" class="nav-item active"><span class="nav-icon">&#x1F3E0;</span>Home</a>
  <a href="/symptom-checker" class="nav-item"><span class="nav-icon">&#x1F9BA;</span>Symptoms</a>
  <a href="/emergency" class="nav-item"><span class="nav-icon">&#x1F6A8;</span>Emergency</a>
  <a href="#" class="nav-item"><span class="nav-icon">&#x1F464;</span>Profile</a>
</nav>
</body>
</html>''')

# ── symptom_checker.html ─────────────────────────────────────────────────────
with open("templates/symptom_checker.html", "w", encoding="utf-8") as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sanjeevani - Symptom Checker</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--green:#1a6b4a;--green-light:#2d9b6f;--cream:#fdf8f0;--red:#d63031;--text:#1a1a2e;--muted:#6b7280}
body{font-family:"DM Sans",sans-serif;background:var(--cream);min-height:100vh}
header{background:white;padding:1.2rem 1.5rem;display:flex;align-items:center;gap:1rem;box-shadow:0 2px 12px rgba(0,0,0,.06)}
.back{font-size:1.3rem;text-decoration:none;color:var(--text)}
.logo{font-family:"Playfair Display",serif;font-size:1.4rem;color:var(--green)}
.main{padding:1.5rem;max-width:480px;margin:0 auto}
.page-title{font-size:1.5rem;font-weight:500;color:var(--text);margin-bottom:.3rem}
.subtitle{font-size:.85rem;color:var(--muted);margin-bottom:1.5rem}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1.2rem}
.chip{padding:.4rem .9rem;border-radius:50px;background:white;border:1.5px solid #e5e7eb;font-size:.8rem;cursor:pointer;transition:all .2s;color:var(--text);font-family:"DM Sans",sans-serif}
.chip:hover,.chip.active{background:var(--green);color:white;border-color:var(--green)}
textarea{width:100%;min-height:120px;padding:1rem;border:1.5px solid #e5e7eb;border-radius:14px;font-size:.9rem;font-family:"DM Sans",sans-serif;resize:vertical;outline:none;background:white;color:var(--text);transition:border .2s;margin-bottom:.5rem}
textarea:focus{border-color:var(--green)}
.hint{font-size:.75rem;color:var(--muted);margin-bottom:1.2rem}
.analyze-btn{width:100%;padding:1rem;background:linear-gradient(135deg,var(--green),var(--green-light));color:white;border:none;border-radius:14px;font-size:1rem;font-weight:500;font-family:"DM Sans",sans-serif;cursor:pointer;transition:transform .2s;box-shadow:0 6px 20px rgba(26,107,74,.3)}
.analyze-btn:hover{transform:translateY(-2px)}
.analyze-btn:disabled{opacity:.6;cursor:not-allowed;transform:none}
#result{margin-top:1.5rem;display:none}
.result-card{background:white;border-radius:18px;padding:1.5rem;box-shadow:0 8px 30px rgba(0,0,0,.1);animation:slideIn .4s ease}
@keyframes slideIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.result-header{display:flex;align-items:center;gap:.8rem;margin-bottom:1rem}
.result-icon{font-size:2rem}
.result-title{font-size:1.1rem;font-weight:500}
.result-sub{font-size:.8rem;color:var(--muted)}
.badge{display:inline-block;padding:.3rem .8rem;border-radius:50px;font-size:.78rem;font-weight:500;margin-bottom:.8rem}
.badge-green{background:#d1fae5;color:#065f46}
.badge-yellow{background:#fef3c7;color:#92400e}
.badge-orange{background:#ffedd5;color:#9a3412}
.badge-red{background:#fee2e2;color:#991b1b}
.info-row{display:flex;justify-content:space-between;align-items:center;padding:.7rem 0;border-bottom:1px solid #f3f4f6}
.info-row:last-child{border-bottom:none}
.info-label{font-size:.82rem;color:var(--muted)}
.info-val{font-size:.9rem;font-weight:500;color:var(--text)}
.emergency-alert{background:linear-gradient(135deg,#d63031,#c0392b);color:white;border-radius:18px;padding:1.5rem;text-align:center;animation:slideIn .4s ease,shake .5s .4s ease}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-8px)}75%{transform:translateX(8px)}}
.emergency-alert h2{font-size:1.3rem;margin-bottom:.5rem}
.emergency-alert p{font-size:.9rem;opacity:.9;margin-bottom:1.2rem}
.call-btn{display:block;background:white;color:var(--red);font-weight:700;font-size:1.1rem;padding:.9rem;border-radius:12px;text-decoration:none;font-family:"DM Sans",sans-serif}
.loading{text-align:center;padding:1rem;color:var(--muted);font-size:.9rem}
.spinner{display:inline-block;width:20px;height:20px;border:2px solid #e5e7eb;border-top-color:var(--green);border-radius:50%;animation:spin .8s linear infinite;margin-right:.5rem;vertical-align:middle}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<header>
  <a href="/home" class="back">&larr;</a>
  <div class="logo">Symptom Checker</div>
</header>
<div class="main">
  <div class="page-title">How are you feeling? &#x1F9BA;</div>
  <div class="subtitle">Describe your symptoms and we will help you find the right care.</div>
  <div class="chips">
    <button class="chip" onclick="addChip(this,\'chest pain\')">Chest pain</button>
    <button class="chip" onclick="addChip(this,\'headache\')">Headache</button>
    <button class="chip" onclick="addChip(this,\'fever\')">Fever</button>
    <button class="chip" onclick="addChip(this,\'cough\')">Cough</button>
    <button class="chip" onclick="addChip(this,\'stomach pain\')">Stomach pain</button>
    <button class="chip" onclick="addChip(this,\'joint pain\')">Joint pain</button>
    <button class="chip" onclick="addChip(this,\'rash\')">Skin rash</button>
    <button class="chip" onclick="addChip(this,\'breathless\')">Breathlessness</button>
    <button class="chip" onclick="addChip(this,\'severe bleeding\')">Severe bleeding</button>
  </div>
  <textarea id="symptomInput" placeholder="e.g. I have severe chest pain and difficulty breathing since morning..."></textarea>
  <div class="hint">&#x1F4A1; Tip: Be specific about duration, severity (mild/moderate/severe), and location of pain.</div>
  <button class="analyze-btn" onclick="analyzeSymptoms()" id="analyzeBtn">Analyze Symptoms &rarr;</button>
  <div id="result"></div>
</div>
<script>
function addChip(el,text){
  el.classList.toggle("active");
  var ta=document.getElementById("symptomInput");
  var existing=ta.value.trim();
  if(el.classList.contains("active")){ta.value=existing?existing+", "+text:text;}
  else{ta.value=ta.value.replace(", "+text,"").replace(text+", ","").replace(text,"").trim();}
}
async function analyzeSymptoms(){
  var symptoms=document.getElementById("symptomInput").value.trim();
  if(!symptoms){alert("Please describe your symptoms first.");return;}
  var btn=document.getElementById("analyzeBtn");
  var resultDiv=document.getElementById("result");
  btn.disabled=true;
  resultDiv.style.display="block";
  resultDiv.innerHTML="<div class=\'loading\'><span class=\'spinner\'></span> Analyzing your symptoms...</div>";
  try{
    var res=await fetch("/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({symptoms:symptoms})});
    var data=await res.json();
    renderResult(data);
  }catch(e){resultDiv.innerHTML="<div class=\'result-card\'><p>Something went wrong. Please try again.</p></div>";}
  btn.disabled=false;
}
function renderResult(data){
  var resultDiv=document.getElementById("result");
  if(data.is_emergency){
    resultDiv.innerHTML="<div class=\'emergency-alert\'><h2>&#x1F6A8; EMERGENCY DETECTED</h2><p>Your symptoms indicate a critical condition requiring immediate medical attention.</p><a href=\'tel:108\' class=\'call-btn\'>&#x1F4DE; Call 108 &mdash; Ambulance</a></div>";
    return;
  }
  var cfg={HIGH:{badge:"badge-orange",label:"&#x26A0;&#xFE0F; High Urgency"},MEDIUM:{badge:"badge-yellow",label:"&#x1F536; Moderate"},LOW:{badge:"badge-green",label:"&#x2705; Low Urgency"}};
  var c=cfg[data.urgency]||cfg["LOW"];
  resultDiv.innerHTML="<div class=\'result-card\'><div class=\'result-header\'><div class=\'result-icon\'>&#x1F3E5;</div><div><div class=\'result-title\'>Analysis Complete</div><div class=\'result-sub\'>Based on your described symptoms</div></div></div><span class=\'badge "+c.badge+"\'>"+ c.label +"</span><div class=\'info-row\'><span class=\'info-label\'>Recommended Specialty</span><span class=\'info-val\'>&#x1F9BA; "+data.specialty+"</span></div><div class=\'info-row\'><span class=\'info-label\'>Urgency Level</span><span class=\'info-val\'>"+data.urgency+"</span></div><div class=\'info-row\'><span class=\'info-label\'>Next Step</span><span class=\'info-val\'>Book appointment with "+data.specialty+"</span></div></div>";
}
</script>
</body>
</html>''')

# ── emergency.html ───────────────────────────────────────────────────────────
with open("templates/emergency.html", "w", encoding="utf-8") as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sanjeevani - Emergency</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--red:#d63031;--green:#1a6b4a;--cream:#fdf8f0;--text:#1a1a2e;--muted:#6b7280}
body{font-family:"DM Sans",sans-serif;background:#fff5f5;min-height:100vh}
header{background:var(--red);padding:1.2rem 1.5rem;display:flex;align-items:center;gap:1rem;color:white}
.back{font-size:1.3rem;text-decoration:none;color:white}
.header-title{font-size:1.2rem;font-weight:500}
.main{padding:1.5rem;max-width:480px;margin:0 auto}
.alert-banner{background:var(--red);color:white;border-radius:16px;padding:1.5rem;text-align:center;margin-bottom:1.5rem;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.85}}
.alert-banner h2{font-size:1.4rem;margin-bottom:.4rem}
.alert-banner p{font-size:.85rem;opacity:.9}
.emergency-numbers{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem}
.num-card{background:white;border-radius:16px;padding:1.2rem;text-align:center;box-shadow:0 4px 16px rgba(214,48,49,.1);text-decoration:none;color:var(--text);border:2px solid transparent;transition:border .2s}
.num-card:hover{border-color:var(--red)}
.num-card .num-icon{font-size:2rem;margin-bottom:.4rem}
.num-card h3{font-size:1.3rem;font-weight:700;color:var(--red)}
.num-card p{font-size:.75rem;color:var(--muted)}
.section-title{font-size:.78rem;font-weight:500;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.8rem}
.tips{background:white;border-radius:16px;padding:1.2rem;box-shadow:0 4px 16px rgba(0,0,0,.06);margin-bottom:1.5rem}
.tip-item{display:flex;gap:.8rem;padding:.7rem 0;border-bottom:1px solid #f3f4f6;align-items:flex-start}
.tip-item:last-child{border-bottom:none}
.tip-num{width:24px;height:24px;background:var(--red);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;flex-shrink:0;margin-top:2px}
.tip-text{font-size:.85rem;line-height:1.5;color:var(--text)}
.go-home{display:block;width:100%;padding:1rem;background:var(--green);color:white;border:none;border-radius:14px;text-align:center;font-size:.95rem;font-weight:500;font-family:"DM Sans",sans-serif;text-decoration:none;box-shadow:0 6px 20px rgba(26,107,74,.3)}
</style>
</head>
<body>
<header>
  <a href="/home" class="back">&larr;</a>
  <div class="header-title">&#x1F6A8; Emergency Response</div>
</header>
<div class="main">
  <div class="alert-banner"><h2>&#x1F198; Stay Calm</h2><p>Help is available. Call emergency services immediately.</p></div>
  <div class="section-title">Emergency Numbers &ndash; India</div>
  <div class="emergency-numbers">
    <a href="tel:108" class="num-card"><div class="num-icon">&#x1F691;</div><h3>108</h3><p>Ambulance</p></a>
    <a href="tel:102" class="num-card"><div class="num-icon">&#x1F3E5;</div><h3>102</h3><p>Medical Helpline</p></a>
    <a href="tel:100" class="num-card"><div class="num-icon">&#x1F694;</div><h3>100</h3><p>Police</p></a>
    <a href="tel:101" class="num-card"><div class="num-icon">&#x1F692;</div><h3>101</h3><p>Fire Brigade</p></a>
  </div>
  <div class="section-title">First Aid While Waiting</div>
  <div class="tips">
    <div class="tip-item"><div class="tip-num">1</div><div class="tip-text">Keep the patient calm and still. Do not move them if a spinal injury is suspected.</div></div>
    <div class="tip-item"><div class="tip-num">2</div><div class="tip-text">If unconscious and not breathing, start CPR: 30 chest compressions, 2 rescue breaths.</div></div>
    <div class="tip-item"><div class="tip-num">3</div><div class="tip-text">For bleeding: apply firm pressure with a clean cloth. Do not remove it.</div></div>
    <div class="tip-item"><div class="tip-num">4</div><div class="tip-text">Keep the person warm. Loosen tight clothing. Do not give food or water.</div></div>
    <div class="tip-item"><div class="tip-num">5</div><div class="tip-text">Stay on the line with emergency services and follow their instructions.</div></div>
  </div>
  <a href="/home" class="go-home">&larr; Return to Home</a>
</div>
</body>
</html>''')

print("All 4 HTML templates created successfully in templates/ folder!")
