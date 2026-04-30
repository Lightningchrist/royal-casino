"""
╔══════════════════════════════════════════════════════════════╗
║              ROYAL CASINO - WEBSITE                         ║
║                                                             ║
║  SETUP (one time only):                                     ║
║    pip install flask                                        ║
║                                                             ║
║  RUN:                                                       ║
║    python casino_website.py                                 ║
║                                                             ║
║  OPEN IN BROWSER:                                           ║
║    http://localhost:5000                                    ║
╚══════════════════════════════════════════════════════════════╝
"""

from flask import Flask, request, jsonify, session, redirect
import json, os, random, datetime, hashlib

app = Flask(__name__)
app.secret_key = "royal_casino_secret_2024_change_this"

DATA_FILE = "casino_users.json"

# ============================================================
#  HTML PAGES (embedded)
# ============================================================

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Royal Casino — Enter</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Cormorant+Garamond:wght@300;400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --gold:#C9A84C;--gold-light:#E8C97A;--gold-dark:#8B6914;
  --bg:#0A0A0A;--bg2:#111111;--bg3:#1A1A1A;
  --text:#F0E6CC;--text2:#9A8A6A;
  --red:#8B0000;--green:#1A4A1A;
}
body{
  background:var(--bg);color:var(--text);
  font-family:'Cormorant Garamond',serif;
  min-height:100vh;display:flex;align-items:center;justify-content:center;
  overflow:hidden;position:relative;
}
/* Animated background */
.bg-particles{position:fixed;inset:0;pointer-events:none;z-index:0}
.particle{
  position:absolute;width:2px;height:2px;background:var(--gold);border-radius:50%;
  animation:float linear infinite;opacity:0;
}
@keyframes float{
  0%{transform:translateY(100vh) rotate(0deg);opacity:0}
  10%{opacity:0.6}
  90%{opacity:0.3}
  100%{transform:translateY(-10vh) rotate(720deg);opacity:0}
}
.casino-bg{
  position:fixed;inset:0;z-index:0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(201,168,76,0.08) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 50%, rgba(139,0,0,0.12) 0%, transparent 60%),
    radial-gradient(ellipse at 50% 0%, rgba(201,168,76,0.05) 0%, transparent 50%);
}
/* Grid pattern */
.grid-overlay{
  position:fixed;inset:0;z-index:0;
  background-image:
    linear-gradient(rgba(201,168,76,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(201,168,76,0.03) 1px, transparent 1px);
  background-size:60px 60px;
}
.container{
  position:relative;z-index:10;width:100%;max-width:480px;padding:20px;
}
.logo-section{text-align:center;margin-bottom:40px}
.crown{font-size:60px;display:block;animation:crownFloat 3s ease-in-out infinite}
@keyframes crownFloat{
  0%,100%{transform:translateY(0) rotate(-2deg)}
  50%{transform:translateY(-10px) rotate(2deg)}
}
.casino-name{
  font-family:'Playfair Display',serif;font-size:48px;font-weight:900;
  background:linear-gradient(135deg, var(--gold-dark), var(--gold-light), var(--gold-dark));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;letter-spacing:4px;line-height:1;
}
.casino-sub{
  font-size:13px;letter-spacing:6px;color:var(--text2);margin-top:8px;text-transform:uppercase;
}
.gold-line{
  width:200px;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
  margin:16px auto;
}
/* Card */
.card{
  background:linear-gradient(145deg,#1C1C1C,#141414);
  border:1px solid rgba(201,168,76,0.2);
  border-radius:4px;padding:40px;
  box-shadow:0 20px 60px rgba(0,0,0,0.8),inset 0 1px 0 rgba(201,168,76,0.1);
  position:relative;overflow:hidden;
}
.card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
}
.tabs{display:flex;margin-bottom:30px;border-bottom:1px solid rgba(201,168,76,0.2)}
.tab{
  flex:1;padding:12px;text-align:center;cursor:pointer;
  font-family:'Playfair Display',serif;font-size:16px;
  color:var(--text2);letter-spacing:1px;transition:all 0.3s;
  border-bottom:2px solid transparent;margin-bottom:-1px;
}
.tab.active{color:var(--gold);border-bottom-color:var(--gold)}
.form{display:none}
.form.active{display:block}
.field{margin-bottom:20px}
.field label{
  display:block;font-size:11px;letter-spacing:3px;text-transform:uppercase;
  color:var(--text2);margin-bottom:8px;
}
.field input{
  width:100%;background:#0D0D0D;border:1px solid rgba(201,168,76,0.2);
  border-radius:2px;padding:14px 16px;color:var(--text);
  font-family:'Cormorant Garamond',serif;font-size:16px;
  transition:all 0.3s;outline:none;
}
.field input:focus{border-color:var(--gold);box-shadow:0 0 0 3px rgba(201,168,76,0.1)}
.field input::placeholder{color:#444}
.btn{
  width:100%;padding:16px;
  background:linear-gradient(135deg,var(--gold-dark),var(--gold),var(--gold-dark));
  border:none;border-radius:2px;
  color:#0A0A0A;font-family:'Playfair Display',serif;font-size:18px;
  font-weight:700;letter-spacing:2px;cursor:pointer;
  transition:all 0.3s;position:relative;overflow:hidden;
}
.btn::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,0.1),transparent);
  opacity:0;transition:opacity 0.3s;
}
.btn:hover::after{opacity:1}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(201,168,76,0.4)}
.btn:active{transform:translateY(0)}
.error{
  background:rgba(139,0,0,0.3);border:1px solid rgba(200,0,0,0.4);
  border-radius:2px;padding:12px 16px;margin-bottom:16px;
  color:#FF6B6B;font-size:14px;display:none;
}
.footer-text{
  text-align:center;margin-top:20px;font-size:12px;
  letter-spacing:2px;color:var(--text2);text-transform:uppercase;
}
/* Suit decorations */
.suits{
  position:absolute;font-size:80px;opacity:0.03;pointer-events:none;
  font-family:serif;color:var(--gold);
}
.suits.tl{top:-10px;left:-10px;transform:rotate(-15deg)}
.suits.br{bottom:-10px;right:-10px;transform:rotate(15deg)}
</style>
</head>
<body>
<div class="casino-bg"></div>
<div class="grid-overlay"></div>
<div class="bg-particles" id="particles"></div>

<div class="container">
  <div class="logo-section">
    <span class="crown">👑</span>
    <div class="casino-name">ROYAL</div>
    <div class="casino-sub">Casino & Club</div>
    <div class="gold-line"></div>
  </div>

  <div class="card">
    <div class="suits tl">♠</div>
    <div class="suits br">♦</div>

    <div class="tabs">
      <div class="tab active" onclick="switchTab('login')">Sign In</div>
      <div class="tab" onclick="switchTab('register')">Register</div>
    </div>

    <div class="error" id="error"></div>

    <div class="form active" id="login-form">
      <div class="field">
        <label>Username</label>
        <input type="text" id="login-user" placeholder="Enter your username" autocomplete="username">
      </div>
      <div class="field">
        <label>Password</label>
        <input type="password" id="login-pass" placeholder="Enter your password" autocomplete="current-password">
      </div>
      <button class="btn" onclick="doLogin()">ENTER THE CASINO</button>
    </div>

    <div class="form" id="register-form">
      <div class="field">
        <label>Choose Username</label>
        <input type="text" id="reg-user" placeholder="At least 3 characters" autocomplete="username">
      </div>
      <div class="field">
        <label>Choose Password</label>
        <input type="password" id="reg-pass" placeholder="At least 6 characters" autocomplete="new-password">
      </div>
      <button class="btn" onclick="doRegister()">CREATE ACCOUNT</button>
    </div>

    <div class="footer-text">Every player starts with $10,000</div>
  </div>
</div>

<script>
// Particles
const container = document.getElementById('particles');
for(let i=0;i<40;i++){
  const p = document.createElement('div');
  p.className = 'particle';
  p.style.left = Math.random()*100+'%';
  p.style.animationDuration = (8+Math.random()*15)+'s';
  p.style.animationDelay = (Math.random()*10)+'s';
  p.style.width = p.style.height = (1+Math.random()*3)+'px';
  container.appendChild(p);
}

function switchTab(tab){
  document.querySelectorAll('.tab').forEach((t,i)=>{
    t.classList.toggle('active', (i===0&&tab==='login')||(i===1&&tab==='register'));
  });
  document.getElementById('login-form').classList.toggle('active', tab==='login');
  document.getElementById('register-form').classList.toggle('active', tab==='register');
  showError('');
}

function showError(msg){
  const el = document.getElementById('error');
  el.textContent = msg; el.style.display = msg ? 'block' : 'none';
}

async function doLogin(){
  const username = document.getElementById('login-user').value.trim();
  const password = document.getElementById('login-pass').value.trim();
  if(!username||!password){showError('Please fill in all fields');return}
  const res = await fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})});
  const data = await res.json();
  if(data.error){showError(data.error)}
  else{window.location.href='/dashboard'}
}

async function doRegister(){
  const username = document.getElementById('reg-user').value.trim();
  const password = document.getElementById('reg-pass').value.trim();
  if(!username||!password){showError('Please fill in all fields');return}
  const res = await fetch('/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})});
  const data = await res.json();
  if(data.error){showError(data.error)}
  else{window.location.href='/dashboard'}
}

// Enter key
document.addEventListener('keydown',e=>{
  if(e.key==='Enter'){
    if(document.getElementById('login-form').classList.contains('active')) doLogin();
    else doRegister();
  }
});
</script>
</body>
</html>
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Royal Casino</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Cormorant+Garamond:wght@300;400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --gold:#C9A84C;--gold-light:#E8C97A;--gold-dark:#8B6914;
  --bg:#080808;--bg2:#111;--bg3:#1A1A1A;--bg4:#222;
  --text:#F0E6CC;--text2:#9A8A6A;--text3:#666;
  --red:#CC2200;--green:#1A6A1A;--border:rgba(201,168,76,0.15);
}
body{background:var(--bg);color:var(--text);font-family:'Cormorant Garamond',serif;min-height:100vh}

/* HEADER */
.header{
  background:linear-gradient(180deg,#0D0D0D,#080808);
  border-bottom:1px solid var(--border);
  padding:0 30px;display:flex;align-items:center;justify-content:space-between;
  position:sticky;top:0;z-index:100;height:64px;
}
.logo{font-family:'Playfair Display',serif;font-size:24px;font-weight:900;
  background:linear-gradient(135deg,var(--gold-dark),var(--gold-light));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  letter-spacing:3px;
}
.balance-display{
  display:flex;align-items:center;gap:16px;
  background:rgba(201,168,76,0.05);border:1px solid var(--border);
  border-radius:2px;padding:8px 20px;
}
.balance-label{font-size:10px;letter-spacing:3px;color:var(--text2);text-transform:uppercase}
.balance-amount{font-size:22px;font-weight:700;color:var(--gold-light);font-family:'Playfair Display',serif}
.header-right{display:flex;align-items:center;gap:16px}
.user-badge{font-size:12px;letter-spacing:2px;color:var(--text2)}
.logout-btn{
  background:transparent;border:1px solid rgba(201,168,76,0.2);
  color:var(--text2);padding:6px 16px;border-radius:2px;
  cursor:pointer;font-size:11px;letter-spacing:2px;text-transform:uppercase;
  transition:all 0.3s;font-family:'Cormorant Garamond',serif;
}
.logout-btn:hover{border-color:var(--gold);color:var(--gold)}

/* NAV */
.nav{
  background:#0D0D0D;border-bottom:1px solid var(--border);
  display:flex;padding:0 30px;overflow-x:auto;gap:0;
}
.nav-item{
  padding:14px 20px;font-size:11px;letter-spacing:2px;text-transform:uppercase;
  color:var(--text2);cursor:pointer;white-space:nowrap;transition:all 0.3s;
  border-bottom:2px solid transparent;margin-bottom:-1px;
}
.nav-item:hover{color:var(--text)}
.nav-item.active{color:var(--gold);border-bottom-color:var(--gold)}

/* MAIN */
.main{padding:30px;max-width:1400px;margin:0 auto}
.section{display:none}
.section.active{display:block}

/* CARDS */
.card{
  background:linear-gradient(145deg,#151515,#0F0F0F);
  border:1px solid var(--border);border-radius:3px;
  padding:30px;position:relative;overflow:hidden;
}
.card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
}
.card-title{
  font-family:'Playfair Display',serif;font-size:20px;color:var(--gold);
  margin-bottom:20px;letter-spacing:1px;
}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}

/* GAME CARDS */
.game-card{
  background:linear-gradient(145deg,#1A1A1A,#111);
  border:1px solid var(--border);border-radius:3px;
  padding:24px;cursor:pointer;transition:all 0.3s;text-align:center;
  position:relative;overflow:hidden;
}
.game-card::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(201,168,76,0.05),transparent);
  opacity:0;transition:opacity 0.3s;
}
.game-card:hover::before{opacity:1}
.game-card:hover{border-color:rgba(201,168,76,0.4);transform:translateY(-4px);box-shadow:0 12px 40px rgba(0,0,0,0.6)}
.game-icon{font-size:40px;display:block;margin-bottom:12px}
.game-name{font-family:'Playfair Display',serif;font-size:18px;color:var(--gold);margin-bottom:6px}
.game-desc{font-size:13px;color:var(--text2)}

/* INPUTS */
.field{margin-bottom:16px}
.field label{display:block;font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--text2);margin-bottom:6px}
.field input,.field select{
  width:100%;background:#0A0A0A;border:1px solid var(--border);
  border-radius:2px;padding:12px 14px;color:var(--text);
  font-family:'Cormorant Garamond',serif;font-size:16px;transition:all 0.3s;outline:none;
}
.field input:focus,.field select:focus{border-color:var(--gold)}
.field select option{background:#1A1A1A}
.btn-gold{
  background:linear-gradient(135deg,var(--gold-dark),var(--gold),var(--gold-dark));
  border:none;border-radius:2px;color:#0A0A0A;
  font-family:'Playfair Display',serif;font-size:16px;font-weight:700;
  letter-spacing:1px;cursor:pointer;padding:14px 28px;transition:all 0.3s;
  width:100%;
}
.btn-gold:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(201,168,76,0.4)}
.btn-gold:disabled{opacity:0.4;cursor:not-allowed;transform:none}
.btn-outline{
  background:transparent;border:1px solid var(--border);
  border-radius:2px;color:var(--text2);
  font-family:'Cormorant Garamond',serif;font-size:14px;
  cursor:pointer;padding:10px 20px;transition:all 0.3s;
}
.btn-outline:hover{border-color:var(--gold);color:var(--gold)}
.btn-red{
  background:linear-gradient(135deg,#6A0000,#CC2200);border:none;border-radius:2px;
  color:#FFF;font-family:'Playfair Display',serif;font-size:16px;font-weight:700;
  cursor:pointer;padding:14px 28px;transition:all 0.3s;width:100%;
}
.btn-red:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(200,0,0,0.4)}
.btn-green{
  background:linear-gradient(135deg,#0A3A0A,#1A8A1A);border:none;border-radius:2px;
  color:#FFF;font-family:'Playfair Display',serif;font-size:16px;font-weight:700;
  cursor:pointer;padding:14px 28px;transition:all 0.3s;width:100%;
}
.btn-green:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,150,0,0.3)}

/* RESULT */
.result{
  border-radius:2px;padding:20px;margin-top:16px;text-align:center;
  display:none;animation:fadeIn 0.4s ease;
}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.result.win{background:rgba(26,106,26,0.3);border:1px solid rgba(26,200,26,0.3)}
.result.loss{background:rgba(106,0,0,0.3);border:1px solid rgba(200,26,26,0.3)}
.result.neutral{background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.3)}
.result-amount{font-family:'Playfair Display',serif;font-size:28px;font-weight:700}
.result.win .result-amount{color:#4AFF4A}
.result.loss .result-amount{color:#FF4A4A}
.result.neutral .result-amount{color:var(--gold)}

/* SLOTS */
.slot-machine{
  background:#0A0A0A;border:2px solid var(--gold-dark);border-radius:4px;
  padding:30px;text-align:center;margin:20px 0;
}
.reels{display:flex;justify-content:center;gap:16px;margin-bottom:20px}
.reel{
  width:80px;height:80px;background:#111;border:1px solid var(--border);
  border-radius:4px;display:flex;align-items:center;justify-content:center;
  font-size:40px;transition:all 0.3s;
}
.reel.spinning{animation:spin 0.1s linear infinite}
@keyframes spin{0%{transform:rotateX(0)}100%{transform:rotateX(360deg)}}
.reel.jackpot{border-color:var(--gold);box-shadow:0 0 20px rgba(201,168,76,0.5);animation:jackpotGlow 0.5s ease infinite alternate}
@keyframes jackpotGlow{from{box-shadow:0 0 10px rgba(201,168,76,0.3)}to{box-shadow:0 0 30px rgba(201,168,76,0.8)}}

/* BLACKJACK */
.bj-table{
  background:radial-gradient(ellipse,#1A3A1A,#0A1A0A);
  border:3px solid var(--gold-dark);border-radius:120px;
  padding:40px;text-align:center;margin:20px 0;min-height:300px;
  position:relative;
}
.bj-label{font-size:11px;letter-spacing:3px;color:var(--text2);text-transform:uppercase;margin-bottom:12px}
.cards-row{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;min-height:80px;margin-bottom:16px}
.playing-card{
  width:56px;height:80px;background:#FFF;border-radius:6px;
  display:flex;align-items:center;justify-content:center;
  font-size:16px;font-weight:700;color:#111;
  box-shadow:2px 4px 12px rgba(0,0,0,0.6);
  animation:dealCard 0.3s ease;
}
@keyframes dealCard{from{transform:translateY(-20px) rotate(-5deg);opacity:0}to{transform:none;opacity:1}}
.playing-card.red-card{color:#CC2200}
.playing-card.hidden{background:#1A3A8A;color:#FFF;font-size:24px}
.hand-value{font-family:'Playfair Display',serif;font-size:18px;color:var(--gold);margin-top:8px}
.bj-actions{display:flex;gap:12px;margin-top:16px}
.bj-actions .btn-gold,.bj-actions .btn-red{flex:1}

/* ROULETTE */
.roulette-wheel{
  width:200px;height:200px;border-radius:50%;margin:0 auto 20px;
  background:conic-gradient(
    #CC2200 0deg 10deg,#111 10deg 20deg,#CC2200 20deg 30deg,#111 30deg 40deg,
    #CC2200 40deg 50deg,#111 50deg 60deg,#CC2200 60deg 70deg,#111 70deg 80deg,
    #CC2200 80deg 90deg,#111 90deg 100deg,#CC2200 100deg 110deg,#111 110deg 120deg,
    #CC2200 120deg 130deg,#111 130deg 140deg,#CC2200 140deg 150deg,#111 150deg 160deg,
    #CC2200 160deg 170deg,#111 170deg 180deg,#2A8A00 180deg 190deg,
    #CC2200 190deg 200deg,#111 200deg 210deg,#CC2200 210deg 220deg,#111 220deg 230deg,
    #CC2200 230deg 240deg,#111 240deg 250deg,#CC2200 250deg 260deg,#111 260deg 270deg,
    #CC2200 270deg 280deg,#111 280deg 290deg,#CC2200 290deg 300deg,#111 300deg 310deg,
    #CC2200 310deg 320deg,#111 320deg 330deg,#CC2200 330deg 340deg,#111 340deg 350deg,
    #CC2200 350deg 360deg
  );
  border:4px solid var(--gold);box-shadow:0 0 30px rgba(201,168,76,0.3);
  position:relative;transition:transform 3s cubic-bezier(0.17,0.67,0.12,0.99);
}
.roulette-ball{
  position:absolute;width:12px;height:12px;background:#FFF;border-radius:50%;
  top:10px;left:50%;transform:translateX(-50%);
  box-shadow:0 0 6px rgba(255,255,255,0.8);transition:all 3s cubic-bezier(0.17,0.67,0.12,0.99);
}
.roulette-center{
  position:absolute;inset:30%;border-radius:50%;
  background:radial-gradient(#1A1A1A,#0A0A0A);border:3px solid var(--gold-dark);
}
.bet-types{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:16px 0}
.bet-type{
  padding:10px;text-align:center;border:1px solid var(--border);border-radius:2px;
  cursor:pointer;transition:all 0.3s;font-size:14px;letter-spacing:1px;
}
.bet-type:hover,.bet-type.selected{border-color:var(--gold);color:var(--gold);background:rgba(201,168,76,0.1)}
.bet-type.red-bet{border-color:rgba(200,0,0,0.3)}
.bet-type.red-bet:hover,.bet-type.red-bet.selected{border-color:#CC2200;background:rgba(200,0,0,0.2);color:#FF6B6B}
.bet-type.black-bet{border-color:rgba(100,100,100,0.3)}
.bet-type.black-bet:hover,.bet-type.black-bet.selected{border-color:#888;background:rgba(100,100,100,0.2);color:#CCC}

/* CRASH */
.crash-display{
  background:#0A0A0A;border:1px solid var(--border);border-radius:4px;
  padding:40px;text-align:center;position:relative;overflow:hidden;margin:20px 0;
}
.crash-multiplier{
  font-family:'Playfair Display',serif;font-size:72px;font-weight:900;
  color:var(--gold);transition:color 0.2s;line-height:1;
}
.crash-multiplier.danger{color:#FF4A4A;animation:shake 0.1s linear infinite}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-2px)}75%{transform:translateX(2px)}}
.crash-graph{
  height:100px;margin:16px 0;position:relative;
  border-left:1px solid var(--border);border-bottom:1px solid var(--border);
}
.crash-graph canvas{width:100%;height:100%}
.crash-status{font-size:14px;letter-spacing:2px;color:var(--text2);margin-top:8px}
.crash-rocket{font-size:40px;animation:rocketFloat 0.5s ease-in-out infinite alternate}
@keyframes rocketFloat{from{transform:translateY(0)}to{transform:translateY(-10px)}}

/* BANK HEIST */
.heist-scene{
  background:#0A0A0A;border:1px solid var(--border);border-radius:4px;
  padding:30px;text-align:center;margin:20px 0;position:relative;overflow:hidden;
}
.vault-door{
  font-size:100px;display:block;transition:all 1s cubic-bezier(0.68,-0.55,0.265,1.55);
  transform-origin:left center;cursor:pointer;
}
.vault-door.open{transform:perspective(400px) rotateY(-60deg)}
.vault-door.shake{animation:vaultShake 0.4s linear}
@keyframes vaultShake{
  0%,100%{transform:translateX(0)}
  20%{transform:translateX(-8px) rotate(-2deg)}
  40%{transform:translateX(8px) rotate(2deg)}
  60%{transform:translateX(-6px) rotate(-1deg)}
  80%{transform:translateX(6px) rotate(1deg)}
}
.police-chase{
  display:none;position:absolute;inset:0;background:rgba(0,0,0,0.85);
  align-items:center;justify-content:center;flex-direction:column;gap:16px;
  animation:policeFlash 0.3s linear infinite;
}
@keyframes policeFlash{
  0%,49%{background:rgba(0,0,100,0.7)}
  50%,100%{background:rgba(100,0,0,0.7)}
}
.police-chase.show{display:flex}
.heist-types{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}
.heist-type{
  padding:16px;border:1px solid var(--border);border-radius:2px;
  cursor:pointer;text-align:center;transition:all 0.3s;
}
.heist-type:hover,.heist-type.selected{border-color:var(--gold);background:rgba(201,168,76,0.05)}
.heist-type .reward{color:var(--gold);font-family:'Playfair Display',serif;font-size:16px}
.heist-type .chance{color:var(--text2);font-size:12px;margin-top:4px}

/* MARKET */
.market-table{width:100%;border-collapse:collapse}
.market-table th{
  text-align:left;padding:10px 14px;font-size:10px;letter-spacing:3px;
  text-transform:uppercase;color:var(--text2);border-bottom:1px solid var(--border);
}
.market-table td{padding:10px 14px;border-bottom:1px solid rgba(201,168,76,0.05);font-size:15px}
.market-table tr:hover td{background:rgba(201,168,76,0.03)}
.chg-up{color:#4AFF4A}
.chg-down{color:#FF4A4A}
.trade-input{display:flex;gap:8px;margin-top:16px}
.trade-input input{flex:1;background:#0A0A0A;border:1px solid var(--border);
  border-radius:2px;padding:10px 14px;color:var(--text);font-family:'Cormorant Garamond',serif;
  font-size:15px;outline:none}
.trade-input input:focus{border-color:var(--gold)}
.trade-input button{padding:10px 20px;white-space:nowrap}

/* PORTFOLIO */
.portfolio-item{
  display:flex;justify-content:space-between;align-items:center;
  padding:12px 0;border-bottom:1px solid rgba(201,168,76,0.05);
}
.portfolio-sym{font-family:'Playfair Display',serif;font-size:16px;color:var(--gold)}
.portfolio-val{font-size:15px}

/* LEADERBOARD */
.lb-item{
  display:flex;align-items:center;gap:16px;
  padding:14px;border-bottom:1px solid rgba(201,168,76,0.05);
}
.lb-rank{font-family:'Playfair Display',serif;font-size:24px;color:var(--text3);width:40px}
.lb-rank.top{color:var(--gold)}
.lb-name{flex:1;font-size:18px}
.lb-balance{font-family:'Playfair Display',serif;font-size:18px;color:var(--gold-light)}

/* HISTORY */
.hist-item{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(201,168,76,0.05);font-size:14px}
.hist-plus{color:#4AFF4A}
.hist-minus{color:#FF4A4A}

/* TOAST */
.toast{
  position:fixed;bottom:30px;right:30px;z-index:1000;
  background:linear-gradient(135deg,#1C1C1C,#141414);border:1px solid var(--border);
  border-radius:3px;padding:16px 24px;font-size:15px;
  animation:toastIn 0.4s ease;box-shadow:0 8px 30px rgba(0,0,0,0.6);
  max-width:300px;
}
@keyframes toastIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}
.toast.success{border-left:3px solid #4AFF4A}
.toast.error{border-left:3px solid #FF4A4A}
.toast.info{border-left:3px solid var(--gold)}

/* DICE */
.dice-display{display:flex;justify-content:center;gap:40px;margin:30px 0}
.die{
  width:80px;height:80px;background:#111;border:2px solid var(--border);
  border-radius:12px;display:flex;align-items:center;justify-content:center;
  font-family:'Playfair Display',serif;font-size:36px;color:var(--gold);
  transition:all 0.5s;box-shadow:4px 4px 12px rgba(0,0,0,0.6);
}
.die.rolling{animation:dieRoll 0.1s linear infinite}
@keyframes dieRoll{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}

/* POKER */
.poker-table{
  background:radial-gradient(ellipse,#1A3A1A,#0A1A0A);
  border:3px solid var(--gold-dark);border-radius:80px;
  padding:30px;text-align:center;margin:20px 0;
}
.hand-label{font-size:11px;letter-spacing:3px;color:rgba(255,255,255,0.5);text-transform:uppercase;margin-bottom:8px}
.hand-name{
  display:inline-block;background:rgba(201,168,76,0.15);border:1px solid var(--gold-dark);
  border-radius:2px;padding:4px 12px;font-size:13px;color:var(--gold);letter-spacing:1px;
  margin-top:8px;
}

/* MYSTERY BOX */
.box-display{
  text-align:center;padding:40px;
}
.mystery-box{
  font-size:100px;display:inline-block;cursor:pointer;
  animation:boxFloat 2s ease-in-out infinite;transition:all 0.3s;
}
.mystery-box:hover{transform:scale(1.1)}
@keyframes boxFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
.box-shine{animation:shine 0.6s ease forwards}
@keyframes shine{
  0%{transform:scale(1) rotate(0)}
  50%{transform:scale(1.3) rotate(180deg)}
  100%{transform:scale(1) rotate(360deg)}
}

/* QUICK BETS */
.quick-bets{display:flex;gap:8px;margin:8px 0}
.quick-bet{
  padding:6px 14px;border:1px solid var(--border);border-radius:2px;
  cursor:pointer;font-size:13px;color:var(--text2);transition:all 0.3s;
}
.quick-bet:hover{border-color:var(--gold);color:var(--gold)}

/* SCROLLBAR */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:#0A0A0A}
::-webkit-scrollbar-thumb{background:var(--gold-dark);border-radius:3px}

/* RESPONSIVE */
@media(max-width:768px){
  .grid-2,.grid-3,.grid-4{grid-template-columns:1fr}
  .heist-types{grid-template-columns:repeat(2,1fr)}
  .bet-types{grid-template-columns:repeat(2,1fr)}
  .main{padding:16px}
  .header{padding:0 16px}
  .balance-amount{font-size:18px}
}

.gold-divider{height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:20px 0}
.section-title{
  font-family:'Playfair Display',serif;font-size:28px;color:var(--gold);
  margin-bottom:24px;letter-spacing:2px;
}
.badge{
  display:inline-block;padding:2px 8px;border-radius:2px;font-size:10px;letter-spacing:1px;
  text-transform:uppercase;background:rgba(201,168,76,0.1);border:1px solid var(--gold-dark);
  color:var(--gold);margin-left:8px;
}
</style>
</head>
<body>

<div class="header">
  <div class="logo">👑 ROYAL</div>
  <div class="balance-display">
    <div>
      <div class="balance-label">Balance</div>
      <div class="balance-amount" id="header-balance">$0</div>
    </div>
  </div>
  <div class="header-right">
    <span class="user-badge" id="header-user"></span>
    <button class="logout-btn" onclick="window.location='/logout'">Exit</button>
  </div>
</div>

<div class="nav">
  <div class="nav-item active" onclick="showSection('lobby')">🎰 Lobby</div>
  <div class="nav-item" onclick="showSection('slots')">🎰 Slots</div>
  <div class="nav-item" onclick="showSection('blackjack')">🃏 Blackjack</div>
  <div class="nav-item" onclick="showSection('roulette')">🎡 Roulette</div>
  <div class="nav-item" onclick="showSection('crash')">🚀 Crash</div>
  <div class="nav-item" onclick="showSection('dice')">🎲 Dice</div>
  <div class="nav-item" onclick="showSection('poker')">♠️ Poker</div>
  <div class="nav-item" onclick="showSection('coinflip')">🪙 Coin Flip</div>
  <div class="nav-item" onclick="showSection('heist')">🏦 Bank Heist</div>
  <div class="nav-item" onclick="showSection('market')">📈 Markets</div>
  <div class="nav-item" onclick="showSection('bots')">🤖 Bots</div>
  <div class="nav-item" onclick="showSection('business')">🏢 Business</div>
  <div class="nav-item" onclick="showSection('daily')">🎁 Bonuses</div>
  <div class="nav-item" onclick="showSection('account')">👤 Account</div>
</div>

<div class="main">

<!-- LOBBY -->
<div class="section active" id="section-lobby">
  <div class="section-title">Welcome to the Royal Casino</div>
  <div class="grid-4" style="margin-bottom:24px">
    <div class="game-card" onclick="showSection('slots')">
      <span class="game-icon">🎰</span>
      <div class="game-name">Slots</div>
      <div class="game-desc">Spin to win up to 50x</div>
    </div>
    <div class="game-card" onclick="showSection('blackjack')">
      <span class="game-icon">🃏</span>
      <div class="game-name">Blackjack</div>
      <div class="game-desc">Beat the dealer to 21</div>
    </div>
    <div class="game-card" onclick="showSection('roulette')">
      <span class="game-icon">🎡</span>
      <div class="game-name">Roulette</div>
      <div class="game-desc">Red, black or a number</div>
    </div>
    <div class="game-card" onclick="showSection('crash')">
      <span class="game-icon">🚀</span>
      <div class="game-name">Crash</div>
      <div class="game-desc">Cash out before it crashes</div>
    </div>
    <div class="game-card" onclick="showSection('dice')">
      <span class="game-icon">🎲</span>
      <div class="game-name">Dice</div>
      <div class="game-desc">Roll higher than the dealer</div>
    </div>
    <div class="game-card" onclick="showSection('poker')">
      <span class="game-icon">♠️</span>
      <div class="game-name">Poker</div>
      <div class="game-desc">Best hand wins up to 25x</div>
    </div>
    <div class="game-card" onclick="showSection('coinflip')">
      <span class="game-icon">🪙</span>
      <div class="game-name">Coin Flip</div>
      <div class="game-desc">50/50 double or nothing</div>
    </div>
    <div class="game-card" onclick="showSection('heist')">
      <span class="game-icon">🏦</span>
      <div class="game-name">Bank Heist</div>
      <div class="game-desc">Rob a bank for millions</div>
    </div>
  </div>

  <div class="grid-2">
    <div class="card">
      <div class="card-title">🏆 Leaderboard</div>
      <div id="lobby-leaderboard">Loading...</div>
    </div>
    <div class="card">
      <div class="card-title">📜 Recent Activity</div>
      <div id="lobby-history">Loading...</div>
    </div>
  </div>
</div>

<!-- SLOTS -->
<div class="section" id="section-slots">
  <div class="section-title">🎰 Slot Machine</div>
  <div class="grid-2">
    <div class="card">
      <div class="slot-machine">
        <div class="reels">
          <div class="reel" id="reel-0">🎰</div>
          <div class="reel" id="reel-1">🎰</div>
          <div class="reel" id="reel-2">🎰</div>
        </div>
        <div style="font-size:12px;letter-spacing:2px;color:var(--text2)">💎=50x  7️⃣=20x  🎰=15x  ⭐=10x  Other=5x</div>
      </div>
      <div class="field">
        <label>Bet Amount</label>
        <input type="number" id="slots-bet" placeholder="Enter bet" min="1">
        <div class="quick-bets">
          <span class="quick-bet" onclick="setBet('slots-bet',100)">$100</span>
          <span class="quick-bet" onclick="setBet('slots-bet',500)">$500</span>
          <span class="quick-bet" onclick="setBet('slots-bet',1000)">$1K</span>
          <span class="quick-bet" onclick="setBet('slots-bet',5000)">$5K</span>
          <span class="quick-bet" onclick="setBet('slots-bet',10000)">$10K</span>
        </div>
      </div>
      <button class="btn-gold" id="slots-btn" onclick="playSlots()">SPIN THE REELS</button>
      <div class="result" id="slots-result"></div>
    </div>
    <div class="card">
      <div class="card-title">How to Play</div>
      <p style="color:var(--text2);line-height:1.8;font-size:15px">
        Spin the reels and match symbols to win.<br><br>
        <strong style="color:var(--gold)">Three of a kind:</strong> Major win!<br>
        <strong style="color:var(--text)">Two of a kind:</strong> 1.5x your bet back<br>
        <strong style="color:var(--text2)">No match:</strong> Lose your bet<br><br>
        <strong style="color:var(--gold)">💎 Diamonds:</strong> 50x your bet<br>
        <strong style="color:var(--gold)">7️⃣ Sevens:</strong> 20x your bet<br>
        <strong style="color:var(--gold)">🎰 Casino:</strong> 15x your bet
      </p>
    </div>
  </div>
</div>

<!-- BLACKJACK -->
<div class="section" id="section-blackjack">
  <div class="section-title">🃏 Blackjack</div>
  <div class="grid-2">
    <div class="card">
      <div class="bj-table">
        <div class="bj-label">Dealer's Hand</div>
        <div class="cards-row" id="bj-dealer-cards"></div>
        <div class="hand-value" id="bj-dealer-val"></div>
        <div class="gold-divider"></div>
        <div class="bj-label">Your Hand</div>
        <div class="cards-row" id="bj-player-cards"></div>
        <div class="hand-value" id="bj-player-val"></div>
      </div>
      <div id="bj-start-area">
        <div class="field">
          <label>Bet Amount</label>
          <input type="number" id="bj-bet" placeholder="Enter bet" min="1">
          <div class="quick-bets">
            <span class="quick-bet" onclick="setBet('bj-bet',100)">$100</span>
            <span class="quick-bet" onclick="setBet('bj-bet',500)">$500</span>
            <span class="quick-bet" onclick="setBet('bj-bet',1000)">$1K</span>
            <span class="quick-bet" onclick="setBet('bj-bet',5000)">$5K</span>
          </div>
        </div>
        <button class="btn-gold" onclick="bjStart()">DEAL CARDS</button>
      </div>
      <div id="bj-actions" style="display:none">
        <div class="bj-actions">
          <button class="btn-green" onclick="bjHit()">👊 HIT</button>
          <button class="btn-red" onclick="bjStand()">🛑 STAND</button>
        </div>
      </div>
      <div class="result" id="bj-result"></div>
    </div>
    <div class="card">
      <div class="card-title">How to Play</div>
      <p style="color:var(--text2);line-height:1.8;font-size:15px">
        Get closer to 21 than the dealer without going over.<br><br>
        <strong style="color:var(--gold)">Hit:</strong> Take another card<br>
        <strong style="color:var(--gold)">Stand:</strong> Keep your current hand<br><br>
        <strong style="color:var(--text)">Blackjack (21):</strong> Pays 2.5x<br>
        <strong style="color:var(--text)">Win:</strong> Pays 2x your bet<br>
        <strong style="color:var(--text)">Push (tie):</strong> Get your bet back<br>
        <strong style="color:var(--text2)">Bust (over 21):</strong> Lose your bet
      </p>
    </div>
  </div>
</div>

<!-- ROULETTE -->
<div class="section" id="section-roulette">
  <div class="section-title">🎡 Roulette</div>
  <div class="grid-2">
    <div class="card">
      <div style="text-align:center">
        <div class="roulette-wheel" id="roulette-wheel">
          <div class="roulette-center"></div>
          <div class="roulette-ball" id="roulette-ball"></div>
        </div>
        <div id="roulette-spin-result" style="font-family:'Playfair Display',serif;font-size:24px;color:var(--gold);margin:10px 0"></div>
      </div>
      <div class="bet-types" id="roulette-bet-types">
        <div class="bet-type red-bet" onclick="selectBetType('red',this)">🔴 Red</div>
        <div class="bet-type black-bet" onclick="selectBetType('black',this)">⚫ Black</div>
        <div class="bet-type" onclick="selectBetType('odd',this)">Odd</div>
        <div class="bet-type" onclick="selectBetType('even',this)">Even</div>
        <div class="bet-type" onclick="selectBetType('0',this)">0 (36x)</div>
        <div class="bet-type" onclick="showNumberPicker()">Pick Number</div>
      </div>
      <div id="number-picker" style="display:none;margin:8px 0">
        <input type="number" id="roulette-number" placeholder="0-36" min="0" max="36"
          style="width:100%;background:#0A0A0A;border:1px solid var(--border);border-radius:2px;padding:10px;color:var(--text);font-size:16px;outline:none">
        <button class="btn-outline" style="margin-top:8px;width:100%" onclick="selectNumber()">Confirm Number</button>
      </div>
      <div class="field" style="margin-top:12px">
        <label>Bet Amount</label>
        <input type="number" id="roulette-bet" placeholder="Enter bet" min="1">
        <div class="quick-bets">
          <span class="quick-bet" onclick="setBet('roulette-bet',100)">$100</span>
          <span class="quick-bet" onclick="setBet('roulette-bet',500)">$500</span>
          <span class="quick-bet" onclick="setBet('roulette-bet',1000)">$1K</span>
        </div>
      </div>
      <button class="btn-gold" onclick="playRoulette()">SPIN THE WHEEL</button>
      <div class="result" id="roulette-result"></div>
    </div>
    <div class="card">
      <div class="card-title">Payouts</div>
      <div style="color:var(--text2);font-size:15px;line-height:2">
        <div style="display:flex;justify-content:space-between"><span>🔴 Red / ⚫ Black</span><span style="color:var(--gold)">2x</span></div>
        <div style="display:flex;justify-content:space-between"><span>Odd / Even</span><span style="color:var(--gold)">2x</span></div>
        <div style="display:flex;justify-content:space-between"><span>Single Number</span><span style="color:var(--gold)">36x</span></div>
        <div style="display:flex;justify-content:space-between"><span>Zero (0)</span><span style="color:var(--gold)">36x</span></div>
      </div>
    </div>
  </div>
</div>

<!-- CRASH -->
<div class="section" id="section-crash">
  <div class="section-title">🚀 Crash</div>
  <div class="grid-2">
    <div class="card">
      <div class="crash-display" id="crash-display">
        <div class="crash-rocket" id="crash-rocket">🚀</div>
        <div class="crash-multiplier" id="crash-mult">1.00x</div>
        <div class="crash-status" id="crash-status">Place your bet to start</div>
        <canvas id="crash-canvas" style="width:100%;height:80px;display:block;margin-top:16px"></canvas>
      </div>
      <div id="crash-start-area">
        <div class="field">
          <label>Bet Amount</label>
          <input type="number" id="crash-bet" placeholder="Enter bet" min="1">
          <div class="quick-bets">
            <span class="quick-bet" onclick="setBet('crash-bet',100)">$100</span>
            <span class="quick-bet" onclick="setBet('crash-bet',500)">$500</span>
            <span class="quick-bet" onclick="setBet('crash-bet',1000)">$1K</span>
          </div>
        </div>
        <button class="btn-gold" id="crash-start-btn" onclick="crashStart()">LAUNCH 🚀</button>
      </div>
      <div id="crash-cashout-area" style="display:none">
        <button class="btn-green" style="font-size:24px;padding:20px" onclick="crashCashout()">💰 CASH OUT</button>
      </div>
      <div class="result" id="crash-result"></div>
    </div>
    <div class="card">
      <div class="card-title">How to Play</div>
      <p style="color:var(--text2);line-height:1.8;font-size:15px">
        The multiplier starts at 1x and keeps rising.<br><br>
        Press <strong style="color:var(--green)">CASH OUT</strong> at any moment to lock in your winnings.<br><br>
        Wait too long and it <strong style="color:var(--red)">CRASHES</strong> — you lose everything.<br><br>
        The crash point is random — it could crash at 1.2x or fly to 100x!
      </p>
    </div>
  </div>
</div>

<!-- DICE -->
<div class="section" id="section-dice">
  <div class="section-title">🎲 Dice Roll</div>
  <div class="grid-2">
    <div class="card">
      <div class="dice-display">
        <div>
          <div style="font-size:11px;letter-spacing:3px;color:var(--text2);text-align:center;margin-bottom:8px">YOU</div>
          <div class="die" id="dice-player">?</div>
        </div>
        <div style="display:flex;align-items:center;font-family:'Playfair Display',serif;font-size:24px;color:var(--text2)">VS</div>
        <div>
          <div style="font-size:11px;letter-spacing:3px;color:var(--text2);text-align:center;margin-bottom:8px">DEALER</div>
          <div class="die" id="dice-dealer">?</div>
        </div>
      </div>
      <div class="field">
        <label>Bet Amount</label>
        <input type="number" id="dice-bet" placeholder="Enter bet" min="1">
        <div class="quick-bets">
          <span class="quick-bet" onclick="setBet('dice-bet',100)">$100</span>
          <span class="quick-bet" onclick="setBet('dice-bet',500)">$500</span>
          <span class="quick-bet" onclick="setBet('dice-bet',1000)">$1K</span>
          <span class="quick-bet" onclick="setBet('dice-bet',5000)">$5K</span>
        </div>
      </div>
      <button class="btn-gold" id="dice-btn" onclick="playDice()">ROLL THE DICE</button>
      <div class="result" id="dice-result"></div>
    </div>
    <div class="card">
      <div class="card-title">How to Play</div>
      <p style="color:var(--text2);line-height:1.8;font-size:15px">
        You and the dealer each roll a dice (1–6).<br><br>
        <strong style="color:var(--gold)">Higher number wins</strong> — pays 2x your bet<br>
        <strong style="color:var(--text)">Same number</strong> — push, get your bet back<br>
        <strong style="color:var(--text2)">Lower number</strong> — lose your bet
      </p>
    </div>
  </div>
</div>

<!-- POKER -->
<div class="section" id="section-poker">
  <div class="section-title">♠️ Poker</div>
  <div class="grid-2">
    <div class="card">
      <div class="poker-table">
        <div class="hand-label">Dealer</div>
        <div class="cards-row" id="poker-dealer-cards"></div>
        <div id="poker-dealer-name" class="hand-name" style="display:none"></div>
        <div class="gold-divider"></div>
        <div class="hand-label">Your Hand</div>
        <div class="cards-row" id="poker-player-cards"></div>
        <div id="poker-player-name" class="hand-name" style="display:none"></div>
      </div>
      <div class="field">
        <label>Bet Amount</label>
        <input type="number" id="poker-bet" placeholder="Enter bet" min="1">
        <div class="quick-bets">
          <span class="quick-bet" onclick="setBet('poker-bet',500)">$500</span>
          <span class="quick-bet" onclick="setBet('poker-bet',1000)">$1K</span>
          <span class="quick-bet" onclick="setBet('poker-bet',5000)">$5K</span>
        </div>
      </div>
      <button class="btn-gold" onclick="playPoker()">DEAL CARDS</button>
      <div class="result" id="poker-result"></div>
    </div>
    <div class="card">
      <div class="card-title">Hand Rankings</div>
      <div style="color:var(--text2);font-size:14px;line-height:2.2">
        <div style="display:flex;justify-content:space-between"><span>Straight Flush</span><span style="color:var(--gold)">25x</span></div>
        <div style="display:flex;justify-content:space-between"><span>Four of a Kind</span><span style="color:var(--gold)">15x</span></div>
        <div style="display:flex;justify-content:space-between"><span>Full House</span><span style="color:var(--gold)">10x</span></div>
        <div style="display:flex;justify-content:space-between"><span>Flush</span><span style="color:var(--gold)">8x</span></div>
        <div style="display:flex;justify-content:space-between"><span>Straight</span><span style="color:var(--gold)">6x</span></div>
        <div style="display:flex;justify-content:space-between"><span>Three of a Kind</span><span style="color:var(--gold)">4x</span></div>
        <div style="display:flex;justify-content:space-between"><span>Two Pair</span><span style="color:var(--gold)">3x</span></div>
        <div style="display:flex;justify-content:space-between"><span>One Pair</span><span style="color:var(--gold)">2x</span></div>
      </div>
    </div>
  </div>
</div>

<!-- COIN FLIP -->
<div class="section" id="section-coinflip">
  <div class="section-title">🪙 Coin Flip</div>
  <div class="grid-2">
    <div class="card" style="text-align:center">
      <div id="coin-display" style="font-size:120px;margin:20px 0;transition:all 0.5s">🪙</div>
      <div id="coin-side-display" style="font-family:'Playfair Display',serif;font-size:24px;color:var(--gold);margin-bottom:20px"></div>
      <div style="display:flex;gap:12px;margin-bottom:20px">
        <button class="btn-gold" style="flex:1" onclick="selectCoin('heads')" id="btn-heads">HEADS</button>
        <button class="btn-outline" style="flex:1" onclick="selectCoin('tails')" id="btn-tails">TAILS</button>
      </div>
      <div class="field">
        <label>Bet Amount</label>
        <input type="number" id="coin-bet" placeholder="Enter bet" min="1">
        <div class="quick-bets">
          <span class="quick-bet" onclick="setBet('coin-bet',100)">$100</span>
          <span class="quick-bet" onclick="setBet('coin-bet',500)">$500</span>
          <span class="quick-bet" onclick="setBet('coin-bet',1000)">$1K</span>
          <span class="quick-bet" onclick="setBet('coin-bet',5000)">$5K</span>
        </div>
      </div>
      <button class="btn-gold" onclick="playCoin()">FLIP THE COIN</button>
      <div class="result" id="coin-result"></div>
    </div>
    <div class="card">
      <div class="card-title">50/50 Chance</div>
      <p style="color:var(--text2);line-height:1.8;font-size:15px">
        Pick heads or tails, then flip.<br><br>
        <strong style="color:var(--gold)">Correct guess:</strong> Win 2x your bet<br>
        <strong style="color:var(--text2)">Wrong guess:</strong> Lose your bet<br><br>
        Pure luck. 50/50. No strategy needed.
      </p>
    </div>
  </div>
</div>

<!-- BANK HEIST -->
<div class="section" id="section-heist">
  <div class="section-title">🏦 Bank Heist</div>
  <div class="grid-2">
    <div class="card">
      <div class="heist-scene" id="heist-scene">
        <span class="vault-door" id="vault-door">🏛️</span>
        <div class="police-chase" id="police-chase">
          <div style="font-size:60px">🚔</div>
          <div style="font-family:'Playfair Display',serif;font-size:24px;color:#FFF">BUSTED!</div>
          <div style="font-size:13px;color:rgba(255,255,255,0.7)">The police caught you!</div>
        </div>
      </div>
      <div class="heist-types" id="heist-types">
        <div class="heist-type selected" onclick="selectHeist('small',this)">
          <div style="font-size:24px">🏪</div>
          <div style="font-size:13px">Small Bank</div>
          <div class="reward">$500K</div>
          <div class="chance">60% success</div>
        </div>
        <div class="heist-type" onclick="selectHeist('medium',this)">
          <div style="font-size:24px">🏦</div>
          <div style="font-size:13px">City Bank</div>
          <div class="reward">$2M</div>
          <div class="chance">40% success</div>
        </div>
        <div class="heist-type" onclick="selectHeist('large',this)">
          <div style="font-size:24px">🏛️</div>
          <div style="font-size:13px">National Bank</div>
          <div class="reward">$10M</div>
          <div class="chance">25% success</div>
        </div>
        <div class="heist-type" onclick="selectHeist('mega',this)">
          <div style="font-size:24px">🏰</div>
          <div style="font-size:13px">Fed Reserve</div>
          <div class="reward">$50M</div>
          <div class="chance">10% success</div>
        </div>
      </div>
      <div style="color:var(--text2);font-size:13px;margin-bottom:16px;letter-spacing:1px">
        Crew fee: 10% of reward paid upfront. Once every 12 hours.
      </div>
      <button class="btn-gold" onclick="playHeist()">🎭 START THE HEIST</button>
      <div class="result" id="heist-result"></div>
    </div>
    <div class="card">
      <div class="card-title">Mission Briefing</div>
      <p style="color:var(--text2);line-height:1.8;font-size:15px">
        Choose your target bank carefully.<br><br>
        You pay a <strong style="color:var(--gold)">crew fee upfront</strong> (10% of reward). This is your risk.<br><br>
        <strong style="color:var(--green)">Success:</strong> Walk away with the full reward<br>
        <strong style="color:var(--red)">Caught:</strong> Lose your crew fee, cops take you in<br><br>
        Higher reward = higher risk. Are you feeling lucky?<br><br>
        <strong style="color:var(--gold)">Cooldown:</strong> 12 hours between heists
      </p>
    </div>
  </div>
</div>

<!-- MARKET -->
<div class="section" id="section-market">
  <div class="section-title">📈 Markets</div>
  <div style="display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap">
    <button class="btn-outline" onclick="showMarketTab('stocks')" id="mtab-stocks" style="border-color:var(--gold);color:var(--gold)">Stocks</button>
    <button class="btn-outline" onclick="showMarketTab('crypto')" id="mtab-crypto">Crypto</button>
    <button class="btn-outline" onclick="showMarketTab('forex')" id="mtab-forex">Commodities</button>
    <button class="btn-outline" onclick="showMarketTab('portfolio')" id="mtab-portfolio">My Portfolio</button>
  </div>

  <div id="market-stocks">
    <div class="card">
      <div class="card-title">Stock Market</div>
      <table class="market-table" id="stocks-table">
        <thead><tr><th>Symbol</th><th>Price</th><th>Change</th><th>Trade</th></tr></thead>
        <tbody id="stocks-tbody"></tbody>
      </table>
    </div>
  </div>

  <div id="market-crypto" style="display:none">
    <div class="card">
      <div class="card-title">Crypto Market</div>
      <table class="market-table">
        <thead><tr><th>Symbol</th><th>Price</th><th>Change</th><th>Trade</th></tr></thead>
        <tbody id="crypto-tbody"></tbody>
      </table>
    </div>
  </div>

  <div id="market-forex" style="display:none">
    <div class="card">
      <div class="card-title">Commodities & Forex</div>
      <table class="market-table">
        <thead><tr><th>Commodity</th><th>Price</th><th>Change</th><th>Unit</th><th>Trade</th></tr></thead>
        <tbody id="forex-tbody"></tbody>
      </table>
    </div>
  </div>

  <div id="market-portfolio" style="display:none">
    <div class="grid-3">
      <div class="card">
        <div class="card-title">📈 Stocks</div>
        <div id="portfolio-stocks"></div>
      </div>
      <div class="card">
        <div class="card-title">🪙 Crypto</div>
        <div id="portfolio-crypto"></div>
      </div>
      <div class="card">
        <div class="card-title">🥇 Commodities</div>
        <div id="portfolio-forex"></div>
      </div>
    </div>
  </div>
</div>

<!-- BOTS -->
<div class="section" id="section-bots">
  <div class="section-title">🤖 Bot Shop</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">Today's Shop <span class="badge" id="shop-refresh"></span></div>
      <div id="shop-bots"></div>
    </div>
    <div class="card">
      <div class="card-title">Your Bots</div>
      <div id="my-bots"></div>
      <div style="margin-top:16px;display:flex;gap:12px">
        <button class="btn-gold" onclick="claimBots()" style="flex:1">CLAIM EARNINGS</button>
      </div>
      <div class="result" id="bots-result"></div>
    </div>
  </div>
</div>

<!-- BUSINESS -->
<div class="section" id="section-business">
  <div class="section-title">🏢 Businesses</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">Available Businesses</div>
      <div id="businesses-list"></div>
    </div>
    <div class="card">
      <div class="card-title">Your Empire</div>
      <div id="my-businesses"></div>
      <div style="margin-top:16px">
        <button class="btn-gold" onclick="claimBusiness()">COLLECT EARNINGS</button>
      </div>
      <div class="result" id="business-result"></div>
    </div>
  </div>
</div>

<!-- DAILY -->
<div class="section" id="section-daily">
  <div class="section-title">🎁 Bonuses</div>
  <div class="grid-2">
    <div class="card" style="text-align:center">
      <div class="card-title">Daily Bonus</div>
      <div style="font-size:80px;margin:20px 0;animation:boxFloat 2s ease-in-out infinite">🎁</div>
      <p style="color:var(--text2);margin-bottom:20px;font-size:15px">Claim between $10,000 and $100,000 every 24 hours</p>
      <button class="btn-gold" onclick="claimDaily()">CLAIM DAILY BONUS</button>
      <div class="result" id="daily-result"></div>
    </div>
    <div class="card" style="text-align:center">
      <div class="card-title">Mystery Box</div>
      <div class="mystery-box" id="mystery-box-icon" onclick="openMysteryBox()">📦</div>
      <p style="color:var(--text2);margin:16px 0;font-size:15px">$100,000 to open • Once per day<br>Could contain cash, bots, or legendary rewards</p>
      <button class="btn-gold" onclick="openMysteryBox()">OPEN THE BOX — $100K</button>
      <div class="result" id="mystery-result"></div>
    </div>
  </div>
</div>

<!-- ACCOUNT -->
<div class="section" id="section-account">
  <div class="section-title">👤 Account</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">Profile</div>
      <div id="account-info" style="font-size:16px;line-height:2.5;color:var(--text2)">Loading...</div>
    </div>
    <div class="card">
      <div class="card-title">🏆 Leaderboard</div>
      <div id="account-leaderboard">Loading...</div>
    </div>
  </div>
  <div style="margin-top:20px" class="card">
    <div class="card-title">💳 Loan</div>
    <div class="grid-2">
      <div>
        <div id="loan-info" style="color:var(--text2);margin-bottom:16px;font-size:15px"></div>
        <div class="field">
          <label>Loan Amount</label>
          <input type="number" id="loan-amount" placeholder="Enter amount">
        </div>
        <button class="btn-gold" onclick="takeLoan()">TAKE LOAN</button>
      </div>
      <div>
        <div class="field">
          <label>Pay Back Amount</label>
          <input type="number" id="payloan-amount" placeholder="Enter amount">
        </div>
        <button class="btn-outline" style="width:100%" onclick="payLoan()">PAY BACK LOAN</button>
        <div class="result" id="loan-result" style="margin-top:12px"></div>
      </div>
    </div>
  </div>
  <div style="margin-top:20px" class="card">
    <div class="card-title">📜 Transaction History</div>
    <div id="account-history">Loading...</div>
  </div>
</div>

</div><!-- end main -->

<!-- TRADE MODAL -->
<div id="trade-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.8);z-index:500;align-items:center;justify-content:center">
  <div style="background:linear-gradient(145deg,#1C1C1C,#141414);border:1px solid var(--border);border-radius:3px;padding:30px;width:400px;position:relative">
    <div style="font-family:'Playfair Display',serif;font-size:20px;color:var(--gold);margin-bottom:20px" id="trade-title">Trade</div>
    <div class="field">
      <label>Amount</label>
      <input type="number" id="trade-amount" placeholder="Enter amount" min="0.0001" step="any">
    </div>
    <div style="display:flex;gap:12px">
      <button class="btn-green" onclick="executeTrade('buy')" style="flex:1">BUY</button>
      <button class="btn-red" onclick="executeTrade('sell')" style="flex:1">SELL</button>
    </div>
    <button class="btn-outline" style="width:100%;margin-top:12px" onclick="closeTrade()">Cancel</button>
    <div class="result" id="trade-result" style="margin-top:12px"></div>
  </div>
</div>

<script>
let currentUser = null;
let selectedCoin = 'heads';
let selectedHeist = 'small';
let selectedBetType = 'red';
let selectedTradeSymbol = '';
let selectedTradeMarket = '';
let currentMarket = null;
let crashRunning = false;
let crashMultiplier = 1.0;
let crashInterval = null;
let crashPoints = [];

// ============================================================
// INIT
// ============================================================
async function init(){
  const r = await api('/api/me');
  if(r.error){ window.location='/'; return; }
  currentUser = r;
  document.getElementById('header-user').textContent = '@' + r.username;
  updateBalance(r.balance);
  loadLeaderboard();
  loadShop();
  loadMyBots();
  loadBusinesses();
  loadAccountInfo();
  loadMarket();
}

function updateBalance(bal){
  document.getElementById('header-balance').textContent = fmtMoney(bal);
}

function fmtMoney(n){
  n = parseFloat(n);
  if(n>=1e9) return '$'+(n/1e9).toFixed(2)+'B';
  if(n>=1e6) return '$'+(n/1e6).toFixed(2)+'M';
  if(n>=1e3) return '$'+n.toLocaleString('en-US',{maximumFractionDigits:0});
  return '$'+n.toFixed(2);
}

async function api(url, method='GET', body=null){
  const opts = {method, headers:{'Content-Type':'application/json'}};
  if(body) opts.body = JSON.stringify(body);
  const r = await fetch(url, opts);
  return r.json();
}

function showSection(name){
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  document.getElementById('section-'+name).classList.add('active');
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(n=>{ if(n.textContent.toLowerCase().includes(name.toLowerCase().replace('-',' '))) n.classList.add('active'); });
  if(name==='market') loadMarket();
  if(name==='account'){ loadAccountInfo(); loadLeaderboard('account-leaderboard'); }
  if(name==='bots'){ loadShop(); loadMyBots(); }
  if(name==='business'){ loadBusinesses(); loadMyBusinesses(); }
}

function setBet(id, val){
  document.getElementById(id).value = val;
}

function showResult(id, type, msg, amount){
  const el = document.getElementById(id);
  el.className = 'result ' + type;
  el.innerHTML = `<div class="result-amount">${amount ? fmtMoney(amount) : ''}</div><div>${msg}</div>`;
  el.style.display = 'block';
}

function showToast(msg, type='info'){
  const t = document.createElement('div');
  t.className = 'toast '+type;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(()=>{ t.style.animation='toastIn 0.4s ease reverse'; setTimeout(()=>t.remove(),400); }, 3000);
}

// ============================================================
// LEADERBOARD
// ============================================================
async function loadLeaderboard(targetId='lobby-leaderboard'){
  const data = await api('/api/leaderboard');
  const medals = ['🥇','🥈','🥉','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'];
  const vipEmoji = ['','🥉','🥈','🥇'];
  const el = document.getElementById(targetId);
  if(!el) return;
  el.innerHTML = data.map((p,i)=>`
    <div class="lb-item">
      <div class="lb-rank ${i<3?'top':''}">${medals[i]}</div>
      <div class="lb-name">${p.username} ${p.vip>0?vipEmoji[p.vip]:''}</div>
      <div class="lb-balance">${fmtMoney(p.balance)}</div>
    </div>
  `).join('');
  // Also update lobby history from user
  const me = await api('/api/me');
  const hist = document.getElementById('lobby-history');
  if(hist && me.history){
    hist.innerHTML = me.history.slice(0,8).map(h=>`
      <div class="hist-item">
        <span>${h.desc}</span>
        <span class="${h.amount>=0?'hist-plus':'hist-minus'}">${h.amount>=0?'+':''}${fmtMoney(h.amount)}</span>
      </div>
    `).join('') || '<div style="color:var(--text2)">No transactions yet</div>';
  }
}

// ============================================================
// SLOTS
// ============================================================
async function playSlots(){
  const bet = parseInt(document.getElementById('slots-bet').value);
  if(!bet||bet<1){showToast('Enter a valid bet','error');return}
  const btn = document.getElementById('slots-btn');
  btn.disabled = true; btn.textContent = 'SPINNING...';
  const icons = ['🍒','🍋','🍊','🍇','⭐','💎','7️⃣','🔔','🍀','🎰'];
  // Spin animation
  for(let i=0;i<3;i++) document.getElementById('reel-'+i).classList.add('spinning');
  await sleep(1000);
  const data = await api('/api/slots','POST',{bet});
  if(data.error){showToast(data.error,'error'); btn.disabled=false; btn.textContent='SPIN THE REELS'; for(let i=0;i<3;i++) document.getElementById('reel-'+i).classList.remove('spinning'); return;}
  for(let i=0;i<3;i++){
    const reel = document.getElementById('reel-'+i);
    reel.classList.remove('spinning');
    reel.textContent = data.reels[i];
    if(data.type==='jackpot') reel.classList.add('jackpot');
    else reel.classList.remove('jackpot');
  }
  if(data.type==='jackpot'){
    showResult('slots-result','win',`JACKPOT x${data.mult}! 🎉${data.cut?` ($${data.cut.toLocaleString()} to loan)`:''}`,data.win);
    showToast(`JACKPOT! Won ${fmtMoney(data.win)}`,'success');
  } else if(data.type==='partial'){
    showResult('slots-result','win','Two of a kind!',data.win);
  } else {
    showResult('slots-result','loss','No match. Better luck next time!',null);
  }
  updateBalance(data.balance);
  btn.disabled=false; btn.textContent='SPIN THE REELS';
}

// ============================================================
// BLACKJACK
// ============================================================
function makeCard(card){
  const suits = {'S':'♠','H':'♥','D':'♦','C':'♣'};
  const isRed = card.endsWith('H') || card.endsWith('D');
  const rank = card.slice(0,-1);
  const suit = suits[card.slice(-1)] || card.slice(-1);
  return `<div class="playing-card ${isRed?'red-card':''}">${rank}${suit}</div>`;
}

async function bjStart(){
  const bet = parseInt(document.getElementById('bj-bet').value);
  if(!bet||bet<1){showToast('Enter a valid bet','error');return}
  const data = await api('/api/blackjack/start','POST',{bet});
  if(data.error){showToast(data.error,'error');return}
  document.getElementById('bj-player-cards').innerHTML = data.player.map(makeCard).join('');
  document.getElementById('bj-dealer-cards').innerHTML = makeCard(data.dealer_show) + '<div class="playing-card hidden">🂠</div>';
  document.getElementById('bj-player-val').textContent = 'Value: ' + data.player_val;
  document.getElementById('bj-dealer-val').textContent = 'Showing: ?';
  document.getElementById('bj-start-area').style.display='none';
  document.getElementById('bj-result').style.display='none';
  updateBalance(data.balance);
  if(data.blackjack){
    document.getElementById('bj-actions').style.display='none';
    showResult('bj-result','win','BLACKJACK! Natural 21! 🎉',data.win);
    showToast('BLACKJACK! Won '+fmtMoney(data.win),'success');
    setTimeout(bjReset, 3000);
    return;
  }
  document.getElementById('bj-actions').style.display='block';
}

async function bjHit(){
  const data = await api('/api/blackjack/hit','POST');
  if(data.error){showToast(data.error,'error');return}
  document.getElementById('bj-player-cards').innerHTML = data.player.map(makeCard).join('');
  document.getElementById('bj-player-val').textContent = 'Value: ' + data.player_val;
  if(data.bust){
    document.getElementById('bj-actions').style.display='none';
    showResult('bj-result','loss','Bust! You went over 21.',null);
    updateBalance(data.balance);
    setTimeout(bjReset, 3000);
  }
}

async function bjStand(){
  const data = await api('/api/blackjack/stand','POST');
  if(data.error){showToast(data.error,'error');return}
  document.getElementById('bj-dealer-cards').innerHTML = data.dealer.map(makeCard).join('');
  document.getElementById('bj-dealer-val').textContent = 'Value: ' + data.dealer_val;
  document.getElementById('bj-player-val').textContent = 'Value: ' + data.player_val;
  document.getElementById('bj-actions').style.display='none';
  if(data.won){
    showResult('bj-result','win','You win! 🎉'+(data.cut?` ($${data.cut.toLocaleString()} to loan)`:''),data.win);
    showToast('Won '+fmtMoney(data.win),'success');
  } else if(data.push){
    showResult('bj-result','neutral','Push — bet returned.',null);
  } else {
    showResult('bj-result','loss','Dealer wins.',null);
  }
  updateBalance(data.balance);
  setTimeout(bjReset, 3500);
}

function bjReset(){
  document.getElementById('bj-start-area').style.display='block';
  document.getElementById('bj-actions').style.display='none';
  document.getElementById('bj-result').style.display='none';
  document.getElementById('bj-player-cards').innerHTML='';
  document.getElementById('bj-dealer-cards').innerHTML='';
  document.getElementById('bj-player-val').textContent='';
  document.getElementById('bj-dealer-val').textContent='';
}

// ============================================================
// ROULETTE
// ============================================================
function selectBetType(type, el){
  document.querySelectorAll('.bet-type').forEach(b=>b.classList.remove('selected'));
  el.classList.add('selected');
  selectedBetType = type;
  document.getElementById('number-picker').style.display='none';
}

function showNumberPicker(){
  document.getElementById('number-picker').style.display='block';
}

function selectNumber(){
  const n = document.getElementById('roulette-number').value;
  if(n>=0&&n<=36){ selectedBetType=n.toString(); showToast('Betting on number '+n,'info'); }
}

async function playRoulette(){
  const bet = parseInt(document.getElementById('roulette-bet').value);
  if(!bet||bet<1){showToast('Enter a valid bet','error');return}
  // Spin wheel animation
  const wheel = document.getElementById('roulette-wheel');
  const deg = 1440 + Math.random()*360;
  wheel.style.transform = `rotate(${deg}deg)`;
  document.getElementById('roulette-spin-result').textContent = '...';
  await sleep(3000);
  const data = await api('/api/roulette','POST',{bet,bet_type:selectedBetType});
  if(data.error){showToast(data.error,'error');wheel.style.transform='';return}
  const colorMap = {red:'🔴',black:'⚫',green:'🟢'};
  document.getElementById('roulette-spin-result').textContent = `${colorMap[data.color]||''} ${data.spin}`;
  if(data.won){
    showResult('roulette-result','win','Winner! 🎉',data.win);
    showToast('Won '+fmtMoney(data.win),'success');
  } else {
    showResult('roulette-result','loss','Not this time.',null);
  }
  updateBalance(data.balance);
}

// ============================================================
// CRASH
// ============================================================
let crashCanvas, crashCtx;
function initCrashCanvas(){
  crashCanvas = document.getElementById('crash-canvas');
  crashCtx = crashCanvas.getContext('2d');
  crashCanvas.width = crashCanvas.offsetWidth;
  crashCanvas.height = 80;
}

function drawCrashGraph(){
  if(!crashCtx) return;
  crashCtx.clearRect(0,0,crashCanvas.width,crashCanvas.height);
  if(crashPoints.length<2) return;
  const maxM = Math.max(...crashPoints, 2);
  crashCtx.beginPath();
  crashCtx.strokeStyle = '#C9A84C';
  crashCtx.lineWidth = 2;
  crashPoints.forEach((m,i)=>{
    const x = (i/(crashPoints.length-1||1))*crashCanvas.width;
    const y = crashCanvas.height - ((m-1)/(maxM-1||1))*crashCanvas.height;
    if(i===0) crashCtx.moveTo(x,y); else crashCtx.lineTo(x,y);
  });
  crashCtx.stroke();
  // Fill
  crashCtx.lineTo(crashCanvas.width, crashCanvas.height);
  crashCtx.lineTo(0, crashCanvas.height);
  crashCtx.fillStyle = 'rgba(201,168,76,0.1)';
  crashCtx.fill();
}

async function crashStart(){
  const bet = parseInt(document.getElementById('crash-bet').value);
  if(!bet||bet<1){showToast('Enter a valid bet','error');return}
  const data = await api('/api/crash/start','POST',{bet});
  if(data.error){showToast(data.error,'error');return}
  crashRunning = true; crashMultiplier = 1.0; crashPoints = [1.0];
  initCrashCanvas();
  document.getElementById('crash-start-area').style.display='none';
  document.getElementById('crash-cashout-area').style.display='block';
  document.getElementById('crash-result').style.display='none';
  document.getElementById('crash-status').textContent = 'Flying! Press CASH OUT to stop!';
  updateBalance(data.balance);
  crashInterval = setInterval(async ()=>{
    if(!crashRunning) return;
    crashMultiplier = Math.round((crashMultiplier + 0.1 + Math.random()*0.2)*100)/100;
    crashPoints.push(crashMultiplier);
    const multEl = document.getElementById('crash-mult');
    multEl.textContent = crashMultiplier.toFixed(2)+'x';
    if(crashMultiplier > 5) multEl.classList.add('danger');
    drawCrashGraph();
    // Check if crashed
    const tick = await api('/api/crash/tick','POST',{current:crashMultiplier});
    if(tick.crashed){
      clearInterval(crashInterval);
      crashRunning = false;
      document.getElementById('crash-mult').textContent = '💥 CRASHED';
      document.getElementById('crash-mult').classList.add('danger');
      document.getElementById('crash-status').textContent = 'Crashed at '+tick.crash_at+'x!';
      document.getElementById('crash-cashout-area').style.display='none';
      showResult('crash-result','loss','Crashed! You lost your bet.',null);
      setTimeout(crashReset, 3000);
    }
  }, 500);
}

async function crashCashout(){
  if(!crashRunning) return;
  clearInterval(crashInterval);
  crashRunning = false;
  const data = await api('/api/crash/cashout','POST',{current:crashMultiplier});
  document.getElementById('crash-cashout-area').style.display='none';
  if(data.crashed){
    showResult('crash-result','loss','Too late! Crashed.',null);
  } else {
    showResult('crash-result','win',`Cashed out at ${crashMultiplier.toFixed(2)}x! 🎉`,data.win);
    showToast('Won '+fmtMoney(data.win),'success');
    updateBalance(data.balance);
  }
  setTimeout(crashReset, 3000);
}

function crashReset(){
  document.getElementById('crash-start-area').style.display='block';
  document.getElementById('crash-cashout-area').style.display='none';
  document.getElementById('crash-result').style.display='none';
  document.getElementById('crash-mult').textContent='1.00x';
  document.getElementById('crash-mult').classList.remove('danger');
  document.getElementById('crash-status').textContent='Place your bet to start';
  crashPoints=[]; if(crashCtx) crashCtx.clearRect(0,0,crashCanvas.width,crashCanvas.height);
}

// ============================================================
// DICE
// ============================================================
async function playDice(){
  const bet = parseInt(document.getElementById('dice-bet').value);
  if(!bet||bet<1){showToast('Enter a valid bet','error');return}
  const btn = document.getElementById('dice-btn'); btn.disabled=true;
  const p = document.getElementById('dice-player'); const d = document.getElementById('dice-dealer');
  p.classList.add('rolling'); d.classList.add('rolling');
  await sleep(800);
  const data = await api('/api/dice','POST',{bet});
  if(data.error){showToast(data.error,'error');btn.disabled=false;p.classList.remove('rolling');d.classList.remove('rolling');return}
  p.classList.remove('rolling'); d.classList.remove('rolling');
  p.textContent = data.player; d.textContent = data.dealer;
  if(data.won){
    showResult('dice-result','win','Your number is higher! 🎉',data.win);
    showToast('Won '+fmtMoney(data.win),'success');
  } else if(data.tie){
    showResult('dice-result','neutral','Tie! Bet returned.',null);
  } else {
    showResult('dice-result','loss','Dealer wins.',null);
  }
  updateBalance(data.balance); btn.disabled=false;
}

// ============================================================
// POKER
// ============================================================
async function playPoker(){
  const bet = parseInt(document.getElementById('poker-bet').value);
  if(!bet||bet<1){showToast('Enter a valid bet','error');return}
  const data = await api('/api/poker','POST',{bet});
  if(data.error){showToast(data.error,'error');return}
  document.getElementById('poker-player-cards').innerHTML = data.hand.map(c=>`<div class="playing-card ${c.includes('♥')||c.includes('♦')?'red-card':''}">${c}</div>`).join('');
  document.getElementById('poker-dealer-cards').innerHTML = data.d_hand.map(c=>`<div class="playing-card ${c.includes('♥')||c.includes('♦')?'red-card':''}">${c}</div>`).join('');
  document.getElementById('poker-player-name').textContent = data.hand_name; document.getElementById('poker-player-name').style.display='inline-block';
  document.getElementById('poker-dealer-name').textContent = data.d_hand_name; document.getElementById('poker-dealer-name').style.display='inline-block';
  if(data.won){
    showResult('poker-result','win',`${data.hand_name} — x${data.mult} 🎉`,data.win);
    showToast('Won '+fmtMoney(data.win),'success');
  } else if(data.tie){
    showResult('poker-result','neutral','Tie! Bet returned.',null);
  } else {
    showResult('poker-result','loss',`Dealer wins with ${data.d_hand_name}`,null);
  }
  updateBalance(data.balance);
}

// ============================================================
// COIN FLIP
// ============================================================
function selectCoin(side){
  selectedCoin = side;
  document.getElementById('btn-heads').className = side==='heads'?'btn-gold':'btn-outline';
  document.getElementById('btn-tails').className = side==='tails'?'btn-gold':'btn-outline';
  document.getElementById('btn-heads').style.flex='1'; document.getElementById('btn-tails').style.flex='1';
}

async function playCoin(){
  const bet = parseInt(document.getElementById('coin-bet').value);
  if(!bet||bet<1){showToast('Enter a valid bet','error');return}
  document.getElementById('coin-display').style.animation='coinFlip 0.5s linear';
  await sleep(600);
  document.getElementById('coin-display').style.animation='';
  const data = await api('/api/coinflip','POST',{bet,choice:selectedCoin});
  if(data.error){showToast(data.error,'error');return}
  document.getElementById('coin-display').textContent = data.result==='heads'?'🟡':'⚪';
  document.getElementById('coin-side-display').textContent = data.result.toUpperCase();
  if(data.won){
    showResult('coin-result','win','Correct! 🎉',data.win);
    showToast('Won '+fmtMoney(data.win),'success');
  } else {
    showResult('coin-result','loss','Wrong side. Better luck next time!',null);
  }
  updateBalance(data.balance);
}

// ============================================================
// BANK HEIST
// ============================================================
function selectHeist(type, el){
  document.querySelectorAll('.heist-type').forEach(h=>h.classList.remove('selected'));
  el.classList.add('selected'); selectedHeist = type;
}

async function playHeist(){
  const vault = document.getElementById('vault-door');
  const police = document.getElementById('police-chase');
  vault.classList.add('shake'); police.classList.remove('show');
  await sleep(500); vault.classList.remove('shake');
  const data = await api('/api/robbank','POST',{type:selectedHeist});
  if(data.error){showToast(data.error,'error');return}
  if(data.success){
    vault.classList.add('open');
    setTimeout(()=>{ vault.classList.remove('open'); },3000);
    showResult('heist-result','win',`${data.bank} robbed! Crew fee: ${fmtMoney(data.crew_fee)}`,data.win);
    showToast('Heist success! Won '+fmtMoney(data.win),'success');
  } else {
    police.classList.add('show');
    setTimeout(()=>{ police.classList.remove('show'); },2500);
    showResult('heist-result','loss',`Caught at ${data.bank}! Lost crew fee: ${fmtMoney(data.crew_fee)}`,null);
    showToast('Busted! Lost '+fmtMoney(data.crew_fee),'error');
  }
  updateBalance(data.balance);
}

// ============================================================
// MARKET
// ============================================================
async function loadMarket(){
  const data = await api('/api/market');
  currentMarket = data;
  // Stocks
  const sb = document.getElementById('stocks-tbody');
  if(sb) sb.innerHTML = Object.entries(data.stocks).map(([sym,s])=>`
    <tr>
      <td><strong>${sym}</strong></td>
      <td>$${s.price.toFixed(2)}</td>
      <td class="${s.chg>=0?'chg-up':'chg-down'}">${s.chg>=0?'+':''}${s.chg.toFixed(2)}%</td>
      <td><button class="btn-outline" onclick="openTrade('${sym}','stocks')" style="padding:4px 12px;font-size:12px">Trade</button></td>
    </tr>
  `).join('');
  // Crypto
  const cb = document.getElementById('crypto-tbody');
  if(cb) cb.innerHTML = Object.entries(data.crypto).map(([sym,s])=>`
    <tr>
      <td><strong>${sym}</strong></td>
      <td>$${s.price.toFixed(6)}</td>
      <td class="${s.chg>=0?'chg-up':'chg-down'}">${s.chg>=0?'+':''}${s.chg.toFixed(2)}%</td>
      <td><button class="btn-outline" onclick="openTrade('${sym}','crypto')" style="padding:4px 12px;font-size:12px">Trade</button></td>
    </tr>
  `).join('');
  // Forex
  const fb = document.getElementById('forex-tbody');
  if(fb) fb.innerHTML = Object.entries(data.forex).map(([sym,s])=>`
    <tr>
      <td><strong>${s.name||sym}</strong></td>
      <td>$${s.price.toFixed(2)}</td>
      <td class="${s.chg>=0?'chg-up':'chg-down'}">${s.chg>=0?'+':''}${s.chg.toFixed(2)}%</td>
      <td style="color:var(--text2);font-size:12px">${s.unit||''}</td>
      <td><button class="btn-outline" onclick="openTrade('${sym}','forex')" style="padding:4px 12px;font-size:12px">Trade</button></td>
    </tr>
  `).join('');
  // Portfolio
  loadPortfolio();
}

function showMarketTab(tab){
  ['stocks','crypto','forex','portfolio'].forEach(t=>{
    document.getElementById('market-'+t).style.display = t===tab?'block':'none';
    const btn = document.getElementById('mtab-'+t);
    if(btn){ btn.style.borderColor = t===tab?'var(--gold)':''; btn.style.color = t===tab?'var(--gold)':''; }
  });
  if(tab==='portfolio') loadPortfolio();
}

async function loadPortfolio(){
  const data = await api('/api/portfolio');
  const fmtItem = (items, priceKey) => items.length ? items.map(i=>`
    <div class="portfolio-item">
      <div><div class="portfolio-sym">${i.sym}</div><div style="font-size:13px;color:var(--text2)">${i.shares||i.amount} units</div></div>
      <div class="portfolio-val">${fmtMoney(i.value)}</div>
    </div>
  `).join('') : '<div style="color:var(--text2);padding:16px">Empty</div>';
  document.getElementById('portfolio-stocks').innerHTML = fmtItem(data.stocks);
  document.getElementById('portfolio-crypto').innerHTML = fmtItem(data.crypto);
  document.getElementById('portfolio-forex').innerHTML = fmtItem(data.forex);
}

function openTrade(sym, market){
  selectedTradeSymbol = sym; selectedTradeMarket = market;
  document.getElementById('trade-title').textContent = `Trade ${sym}`;
  document.getElementById('trade-amount').value = '';
  document.getElementById('trade-result').style.display='none';
  document.getElementById('trade-modal').style.display='flex';
}

function closeTrade(){ document.getElementById('trade-modal').style.display='none'; }

async function executeTrade(action){
  const amount = parseFloat(document.getElementById('trade-amount').value);
  if(!amount||amount<=0){showToast('Enter a valid amount','error');return}
  let url, body;
  if(action==='buy'){
    url = '/api/buy'+selectedTradeMarket; body = {symbol:selectedTradeSymbol, shares:Math.floor(amount), amount};
  } else {
    url = '/api/sell'+selectedTradeMarket; body = {symbol:selectedTradeSymbol, shares:Math.floor(amount), amount};
  }
  const data = await api(url,'POST',body);
  if(data.error){
    const r = document.getElementById('trade-result');
    r.className='result loss'; r.innerHTML=`<div>${data.error}</div>`; r.style.display='block'; return;
  }
  updateBalance(data.balance);
  const r = document.getElementById('trade-result');
  r.className='result win'; r.innerHTML=`<div>${action==='buy'?'Bought':'Sold'} ${amount} ${selectedTradeSymbol} — ${fmtMoney(action==='buy'?data.cost:data.revenue)}</div>`; r.style.display='block';
  showToast(`${action==='buy'?'Bought':'Sold'} ${selectedTradeSymbol}`,'success');
  setTimeout(closeTrade,1500);
}

// ============================================================
// BOTS
// ============================================================
async function loadShop(){
  const data = await api('/api/shop');
  document.getElementById('shop-refresh').textContent = 'Refreshes in '+data.refresh_in;
  document.getElementById('shop-bots').innerHTML = data.bots.map(b=>`
    <div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid rgba(201,168,76,0.05)">
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:16px;color:var(--gold)">${b.name}</div>
        <div style="font-size:13px;color:var(--text2)">ID: ${b.id} · Earns ${fmtMoney(b.earn)}/6h</div>
      </div>
      <div style="text-align:right">
        <div style="font-size:15px;color:var(--text)">${fmtMoney(b.price)}</div>
        <button class="btn-outline" style="margin-top:4px;padding:4px 12px;font-size:12px" onclick="buyBot('${b.id}')">Buy</button>
      </div>
    </div>
  `).join('');
}

async function buyBot(id){
  const data = await api('/api/buybot','POST',{id});
  if(data.error){showToast(data.error,'error');return}
  showToast(`Bot purchased! You own ${data.owned}.`,'success');
  updateBalance(data.balance); loadShop(); loadMyBots();
}

async function loadMyBots(){
  const data = await api('/api/mybots');
  if(!data.bots||!data.bots.length){
    document.getElementById('my-bots').innerHTML='<div style="color:var(--text2);padding:16px">No bots yet. Buy from the shop!</div>'; return;
  }
  document.getElementById('my-bots').innerHTML = `
    <div style="color:var(--text2);font-size:13px;margin-bottom:12px">Total: ${data.total} bots${data.nuked?' — ⚠️ NUKED':''}</div>
    ${data.bots.map(b=>`
      <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(201,168,76,0.05)">
        <span style="color:var(--text)">${b.name} ×${b.count}</span>
        <span style="color:var(--gold)">${fmtMoney(b.earn_per_cycle)}/6h</span>
      </div>
    `).join('')}
  `;
}

async function claimBots(){
  const data = await api('/api/claimbots','POST');
  if(data.error){showResult('bots-result','loss',data.error,null);return}
  showResult('bots-result','win','Bot earnings collected! 🤖',data.total);
  showToast('Collected '+fmtMoney(data.total),'success');
  updateBalance(data.balance);
}

// ============================================================
// BUSINESSES
// ============================================================
async function loadBusinesses(){
  const data = await api('/api/businesses');
  document.getElementById('businesses-list').innerHTML = Object.entries(data).map(([key,b])=>`
    <div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid rgba(201,168,76,0.05)">
      <div>
        <div style="font-size:16px;color:var(--text)">${b.emoji} ${b.name}</div>
        <div style="font-size:13px;color:var(--text2)">Base: ${fmtMoney(b.base_earn)}/6h · +${(b.synergy*100).toFixed(0)}% synergy/extra</div>
      </div>
      <div style="text-align:right">
        <div style="font-size:15px;color:var(--gold)">${fmtMoney(b.price)}</div>
        <button class="btn-outline" style="margin-top:4px;padding:4px 12px;font-size:12px" onclick="buyBusiness('${key}')">Buy</button>
      </div>
    </div>
  `).join('');
}

async function buyBusiness(type){
  const data = await api('/api/buybusiness','POST',{type});
  if(data.error){showToast(data.error,'error');return}
  showToast(`Purchased! You own ${data.owned}.`,'success');
  updateBalance(data.balance); loadBusinesses(); loadMyBusinesses();
}

async function loadMyBusinesses(){
  const r = await api('/api/me');
  // We'll just show the account info
}

async function claimBusiness(){
  const data = await api('/api/claimbusiness','POST');
  if(data.error){showResult('business-result','loss',data.error,null);return}
  showResult('business-result','win','Business earnings collected! 🏢',data.total);
  showToast('Collected '+fmtMoney(data.total),'success');
  updateBalance(data.balance);
}

// ============================================================
// BONUSES
// ============================================================
async function claimDaily(){
  const data = await api('/api/daily','POST');
  if(data.error){showResult('daily-result','neutral',data.error,null);return}
  showResult('daily-result','win','Daily bonus claimed! 🎁',data.bonus);
  showToast('Daily bonus: '+fmtMoney(data.bonus),'success');
  updateBalance(data.balance);
}

async function openMysteryBox(){
  const box = document.getElementById('mystery-box-icon');
  box.style.animation='shine 0.6s ease forwards';
  await sleep(600);
  const data = await api('/api/mysterybox','POST');
  box.style.animation='boxFloat 2s ease-in-out infinite';
  if(data.error){showResult('mystery-result','neutral',data.error,null);return}
  const msgs = {
    'empty':'The box was empty... 📭',
    'cash':`Cash reward! 💵`,
    'big_cash':'Big cash prize! 💰',
    'bot':`You got a bot: ${data.bot_name}! 🤖`,
    'mega':'MEGA reward! 💎',
    'legendary':`LEGENDARY bot: ${data.bot_name}! 👑`
  };
  const types = {empty:'loss',cash:'win',big_cash:'win',bot:'win',mega:'win',legendary:'win'};
  showResult('mystery-result', types[data.type]||'win', msgs[data.type]||'', data.amount||null);
  if(data.amount) showToast('Won '+fmtMoney(data.amount),'success');
  updateBalance(data.balance);
}

// ============================================================
// ACCOUNT
// ============================================================
async function loadAccountInfo(){
  const data = await api('/api/me');
  currentUser = data;
  document.getElementById('account-info').innerHTML = `
    <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(201,168,76,0.1);padding:8px 0"><span>Username</span><span style="color:var(--text)">@${data.username}</span></div>
    <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(201,168,76,0.1);padding:8px 0"><span>Balance</span><span style="color:var(--gold)">${fmtMoney(data.balance)}</span></div>
    <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(201,168,76,0.1);padding:8px 0"><span>VIP Status</span><span style="color:var(--gold)">${['None','🥉 Bronze','🥈 Silver','🥇 Gold'][data.vip]||'None'}</span></div>
    <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(201,168,76,0.1);padding:8px 0"><span>Multiplier</span><span style="color:var(--text)">×${data.multiplier}</span></div>
    <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(201,168,76,0.1);padding:8px 0"><span>Total Bots</span><span style="color:var(--text)">${data.bots_count}</span></div>
    <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(201,168,76,0.1);padding:8px 0"><span>Achievements</span><span style="color:var(--text)">${data.achievements_count}/${15}</span></div>
    <div style="display:flex;justify-content:space-between;padding:8px 0"><span>Active Loan</span><span style="color:${data.loan>0?'#FF4A4A':'#4AFF4A'}">${data.loan>0?fmtMoney(data.loan):'None'}</span></div>
  `;
  document.getElementById('loan-info').textContent = data.loan>0 ? `Active loan: ${fmtMoney(data.loan)}` : 'No active loan';
  document.getElementById('account-history').innerHTML = data.history.map(h=>`
    <div class="hist-item">
      <span>${h.ts}</span>
      <span>${h.desc}</span>
      <span class="${h.amount>=0?'hist-plus':'hist-minus'}">${h.amount>=0?'+':''}${fmtMoney(h.amount)}</span>
    </div>
  `).join('') || '<div style="color:var(--text2)">No transactions yet</div>';
  loadLeaderboard('account-leaderboard');
}

async function takeLoan(){
  const amount = parseInt(document.getElementById('loan-amount').value);
  if(!amount||amount<1){showToast('Enter a valid amount','error');return}
  const data = await api('/api/loan','POST',{amount});
  if(data.error){showResult('loan-result','loss',data.error,null);return}
  showResult('loan-result','win',`Loan approved! Repay ${fmtMoney(data.due)} in 24h`,data.amount);
  showToast('Loan approved!','success');
  updateBalance(data.balance); loadAccountInfo();
}

async function payLoan(){
  const amount = parseInt(document.getElementById('payloan-amount').value);
  if(!amount||amount<1){showToast('Enter a valid amount','error');return}
  const data = await api('/api/payloan','POST',{amount});
  if(data.error){showResult('loan-result','loss',data.error,null);return}
  const msg = data.remaining>0?`Paid ${fmtMoney(data.paid)}. Remaining: ${fmtMoney(data.remaining)}`:`Loan fully paid! ✅`;
  showResult('loan-result','win',msg,data.paid);
  updateBalance(data.balance); loadAccountInfo();
}

// ============================================================
// UTILS
// ============================================================
function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }

// Close modal on outside click
document.getElementById('trade-modal').addEventListener('click',function(e){
  if(e.target===this) closeTrade();
});

// Init
init();
</script>
</body>
</html>
"""



DATA_FILE = "casino_users.json"

# ============================================================
#  DATA
# ============================================================

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
    except:
        pass
    return {"users": {}, "market": init_market(), "lottery": {"jackpot": 1000000, "tickets": {}, "last_draw": ""}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def init_market():
    return {
        "stocks": {
            "AAPL":{"price":185.0,"chg":0.0}, "TSLA":{"price":210.0,"chg":0.0},
            "NVDA":{"price":450.0,"chg":0.0}, "MSFT":{"price":310.0,"chg":0.0},
            "AMZN":{"price":175.0,"chg":0.0}, "GOOGL":{"price":140.0,"chg":0.0},
            "META":{"price":330.0,"chg":0.0}, "NFLX":{"price":490.0,"chg":0.0},
            "AMD":{"price":160.0,"chg":0.0},  "INTC":{"price":38.0,"chg":0.0},
            "DIS":{"price":100.0,"chg":0.0},  "PYPL":{"price":63.0,"chg":0.0},
            "UBER":{"price":70.0,"chg":0.0},  "SPOT":{"price":230.0,"chg":0.0},
            "COIN":{"price":175.0,"chg":0.0},
        },
        "crypto": {
            "BTC":{"price":67000.0,"chg":0.0}, "ETH":{"price":3500.0,"chg":0.0},
            "BNB":{"price":590.0,"chg":0.0},   "SOL":{"price":180.0,"chg":0.0},
            "XRP":{"price":0.52,"chg":0.0},    "DOGE":{"price":0.15,"chg":0.0},
            "ADA":{"price":0.45,"chg":0.0},    "AVAX":{"price":37.0,"chg":0.0},
            "DOT":{"price":7.5,"chg":0.0},     "MATIC":{"price":0.72,"chg":0.0},
            "LTC":{"price":85.0,"chg":0.0},    "LINK":{"price":14.0,"chg":0.0},
            "UNI":{"price":10.0,"chg":0.0},    "ATOM":{"price":8.5,"chg":0.0},
            "SHIB":{"price":0.000025,"chg":0.0},
        },
        "forex": {
            "GOLD":{"price":2330.0,"chg":0.0,"name":"Gold","unit":"per oz"},
            "SILVER":{"price":27.5,"chg":0.0,"name":"Silver","unit":"per oz"},
            "OIL":{"price":83.0,"chg":0.0,"name":"Crude Oil","unit":"per barrel"},
            "NATGAS":{"price":2.10,"chg":0.0,"name":"Natural Gas","unit":"per MMBtu"},
            "COPPER":{"price":4.20,"chg":0.0,"name":"Copper","unit":"per lb"},
            "PLATINUM":{"price":980.0,"chg":0.0,"name":"Platinum","unit":"per oz"},
        }
    }

def default_user(username):
    return {
        "username": username,
        "balance": 10000,
        "history": [],
        "loan": 0, "loan_due": None, "loan_penalty": False,
        "bots": {}, "bot_last_claim": {},
        "daily_last": None, "multiplier": 1,
        "vip": 0, "vip_renewal": None,
        "mysterybox_last": None,
        "rob_last": None,
        "portfolio": {}, "crypto_portfolio": {}, "forex_portfolio": {},
        "real_estate": [], "rent_collected": {},
        "businesses": {}, "business_last_claim": {},
        "achievements": [],
        "win_streak": 0, "nuked": False,
        "clan": None,
        "created": datetime.datetime.utcnow().isoformat(),
        "last_active": datetime.datetime.utcnow().isoformat(),
    }

def add_history(user, desc, amount):
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    user["history"].insert(0, {"ts": ts, "desc": desc, "amount": amount})
    user["history"] = user["history"][:50]

def fmt(n):
    try:
        n = float(n)
        if n >= 1e9: return "${:.2f}B".format(n/1e9)
        if n >= 1e6: return "${:.2f}M".format(n/1e6)
        if n >= 1e3: return "${:,.0f}".format(n)
        return "${:.2f}".format(n)
    except:
        return str(n)

def get_loan_limit(user):
    vip = user.get("vip", 0)
    return [1000000, 2000000, 5000000, 10000000][min(vip, 3)]

def apply_loan_cut(user, winnings):
    if user.get("loan_penalty") and user["loan"] > 0:
        cut = min(int(winnings * 0.5), user["loan"])
        user["loan"] -= cut
        if user["loan"] <= 0:
            user["loan"] = 0; user["loan_due"] = None; user["loan_penalty"] = False
        return cut
    return 0

def apply_mult(user, amount):
    return int(amount * user.get("multiplier", 1))

# ============================================================
#  SHOP BOTS
# ============================================================

BOT_NAMES = [
    "Nano","Micro","Mini","Basic","Starter","Junior","Rookie","Cadet","Scout","Recruit",
    "Worker","Builder","Maker","Coder","Hacker","Miner","Smart","Clever","Bright","Sharp",
    "Turbo","Swift","Flash","Bolt","Blaze","Power","Force","Iron","Steel","Armor",
    "Cyber","Digital","Quantum","Plasma","Fusion","Alpha","Beta","Gamma","Delta","Sigma",
    "Gold","Diamond","Ruby","Emerald","Crystal","Solar","Lunar","Nova","Pulsar","Galaxy",
    "Hyper","Ultra","Super","Mega","Giga","Storm","Thunder","Lightning","Phoenix","Dragon",
    "Ninja","Warrior","Knight","Hunter","Shadow","Atomic","Laser","Sonic","Pulse","Matrix",
    "Apex","Zenith","Summit","Crown","Empire","Titan X","Mega Pro","Ultra X","Hyper Z","God",
    "King","Lord","Emperor","Overlord","Supreme","Infinite","Eternal","Immortal","Legend","Ultimate",
]

SHOP_BOTS = {}
for _i in range(len(BOT_NAMES)):
    _bid = str(_i + 1)
    _price = int(1000 * (1.075 ** _i))
    SHOP_BOTS[_bid] = {"name": BOT_NAMES[_i] + " Bot", "price": _price, "earn_pct": 0.125}

BUSINESSES = {
    "foodstall":   {"name":"Food Stall",   "emoji":"🍔","price":100000,     "base_earn":8000,      "synergy":0.02,"max":10},
    "taxi":        {"name":"Taxi Fleet",   "emoji":"🚕","price":500000,     "base_earn":45000,     "synergy":0.03,"max":10},
    "nightclub":   {"name":"Night Club",   "emoji":"🎵","price":2000000,    "base_earn":200000,    "synergy":0.04,"max":10},
    "casino":      {"name":"Casino",       "emoji":"🎰","price":10000000,   "base_earn":1100000,   "synergy":0.05,"max":10},
    "techstartup": {"name":"Tech Startup", "emoji":"💻","price":50000000,   "base_earn":6000000,   "synergy":0.06,"max":10},
    "oilrig":      {"name":"Oil Rig",      "emoji":"🛢️","price":200000000,  "base_earn":25000000,  "synergy":0.07,"max":10},
    "spaceagency": {"name":"Space Agency", "emoji":"🚀","price":1000000000, "base_earn":130000000, "synergy":0.08,"max":10},
}

# ============================================================
#  AUTH ROUTES
# ============================================================

@app.route("/")
def index():
    if "username" in session:
        return redirect("/dashboard")
    return INDEX_HTML

@app.route("/register", methods=["POST"])
def register():
    data = load_data()
    username = request.json.get("username","").strip()
    password = request.json.get("password","").strip()
    if not username or not password:
        return jsonify({"error":"Username and password required"})
    if len(username) < 3:
        return jsonify({"error":"Username must be at least 3 characters"})
    if len(password) < 6:
        return jsonify({"error":"Password must be at least 6 characters"})
    if username.lower() in [u.lower() for u in data["users"]]:
        return jsonify({"error":"Username already taken"})
    data["users"][username] = default_user(username)
    data["users"][username]["password"] = hash_pw(password)
    save_data(data)
    session["username"] = username
    return jsonify({"success": True})

@app.route("/login", methods=["POST"])
def login():
    data = load_data()
    username = request.json.get("username","").strip()
    password = request.json.get("password","").strip()
    # Find user case-insensitive
    found = None
    for u in data["users"]:
        if u.lower() == username.lower():
            found = u; break
    if not found or data["users"][found].get("password") != hash_pw(password):
        return jsonify({"error":"Invalid username or password"})
    session["username"] = found
    return jsonify({"success": True})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return DASHBOARD_HTML

# ============================================================
#  API - USER DATA
# ============================================================

@app.route("/api/me")
def api_me():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data()
    user = data["users"].get(session["username"])
    if not user: return jsonify({"error":"user not found"}), 404
    return jsonify({
        "username": user["username"],
        "balance": user["balance"],
        "vip": user["vip"],
        "multiplier": user.get("multiplier",1),
        "loan": user["loan"],
        "loan_penalty": user.get("loan_penalty",False),
        "bots_count": sum(user["bots"].values()),
        "achievements_count": len(user.get("achievements",[])),
        "history": user["history"][:10],
    })

@app.route("/api/leaderboard")
def api_leaderboard():
    data = load_data()
    players = sorted(
        [{"username":u["username"],"balance":u["balance"],"vip":u.get("vip",0)}
         for u in data["users"].values()],
        key=lambda x: -x["balance"]
    )
    return jsonify(players[:10])

# ============================================================
#  API - GAMES
# ============================================================

@app.route("/api/slots", methods=["POST"])
def api_slots():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    bet = int(request.json.get("bet", 0))
    if bet <= 0 or user["balance"] < bet:
        return jsonify({"error":"Invalid bet or insufficient funds"})
    user["balance"] -= bet
    icons = ["🍒","🍋","🍊","🍇","⭐","💎","7️⃣","🔔","🍀","🎰"]
    reels = [random.choice(icons) for _ in range(3)]
    if reels[0] == reels[1] == reels[2]:
        m = {"💎":50,"7️⃣":20,"🎰":15,"⭐":10}.get(reels[0],5)
        win = apply_mult(user, bet*m); user["balance"] += win
        cut = apply_loan_cut(user, win)
        add_history(user, "Slots JACKPOT x{}".format(m), win-bet)
        result = {"type":"jackpot","mult":m,"win":win,"cut":cut,"reels":reels}
    elif reels[0]==reels[1] or reels[1]==reels[2]:
        win = apply_mult(user, int(bet*1.5)); user["balance"] += win
        add_history(user, "Slots partial win", win-bet)
        result = {"type":"partial","win":win,"reels":reels}
    else:
        add_history(user, "Slots loss", -bet)
        result = {"type":"loss","reels":reels}
    result["balance"] = user["balance"]
    save_data(data); return jsonify(result)

@app.route("/api/coinflip", methods=["POST"])
def api_coinflip():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    bet    = int(request.json.get("bet", 0))
    choice = request.json.get("choice","heads")
    if bet <= 0 or user["balance"] < bet:
        return jsonify({"error":"Invalid bet or insufficient funds"})
    user["balance"] -= bet
    result_side = random.choice(["heads","tails"])
    if result_side == choice:
        win = apply_mult(user, bet*2); user["balance"] += win
        cut = apply_loan_cut(user, win)
        add_history(user, "Coin flip win", win-bet)
        save_data(data)
        return jsonify({"result":result_side,"won":True,"win":win,"cut":cut,"balance":user["balance"]})
    else:
        add_history(user, "Coin flip loss", -bet)
        save_data(data)
        return jsonify({"result":result_side,"won":False,"balance":user["balance"]})

@app.route("/api/blackjack/start", methods=["POST"])
def api_bj_start():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    bet = int(request.json.get("bet", 0))
    if bet <= 0 or user["balance"] < bet:
        return jsonify({"error":"Invalid bet or insufficient funds"})
    user["balance"] -= bet
    deck = new_deck(); player = [deck.pop(),deck.pop()]; dealer = [deck.pop(),deck.pop()]
    session["bj"] = {"deck":deck,"player":player,"dealer":dealer,"bet":bet}
    pv = hand_val(player)
    save_data(data)
    resp = {"player":player,"dealer_show":dealer[0],"player_val":pv,"bet":bet,"balance":user["balance"]}
    if pv == 21:
        win = apply_mult(user, int(bet*2.5)); user["balance"] += win
        add_history(user, "Blackjack Natural 21", win-bet); save_data(data)
        resp["blackjack"] = True; resp["win"] = win; resp["balance"] = user["balance"]
        session.pop("bj", None)
    return jsonify(resp)

@app.route("/api/blackjack/hit", methods=["POST"])
def api_bj_hit():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    if "bj" not in session: return jsonify({"error":"No active game"})
    s = session["bj"]
    s["player"].append(s["deck"].pop())
    session["bj"] = s
    pv = hand_val(s["player"])
    if pv > 21:
        data = load_data(); user = data["users"][session["username"]]
        add_history(user, "Blackjack bust", -s["bet"]); save_data(data)
        session.pop("bj",None)
        return jsonify({"player":s["player"],"player_val":pv,"bust":True,"balance":user["balance"]})
    return jsonify({"player":s["player"],"player_val":pv,"bust":False})

@app.route("/api/blackjack/stand", methods=["POST"])
def api_bj_stand():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    if "bj" not in session: return jsonify({"error":"No active game"})
    s = session["bj"]; session.pop("bj",None)
    dealer = s["dealer"]; deck = s["deck"]
    while hand_val(dealer) < 17: dealer.append(deck.pop())
    pv = hand_val(s["player"]); dv = hand_val(dealer); bet = s["bet"]
    data = load_data(); user = data["users"][session["username"]]
    if dv > 21 or pv > dv:
        win = apply_mult(user, bet*2); user["balance"] += win
        cut = apply_loan_cut(user, win)
        add_history(user, "Blackjack win", win-bet)
        res = {"won":True,"win":win,"cut":cut}
    elif pv == dv:
        user["balance"] += bet; add_history(user,"Blackjack push",0)
        res = {"push":True}
    else:
        add_history(user,"Blackjack loss",-bet)
        res = {"won":False}
    res["player"] = s["player"]; res["dealer"] = dealer
    res["player_val"] = pv; res["dealer_val"] = dv
    res["balance"] = user["balance"]
    save_data(data); return jsonify(res)

@app.route("/api/roulette", methods=["POST"])
def api_roulette():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    bet  = int(request.json.get("bet",0))
    bt   = request.json.get("bet_type","red")
    if bet <= 0 or user["balance"] < bet:
        return jsonify({"error":"Invalid bet or insufficient funds"})
    reds = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    spin = random.randint(0,36)
    user["balance"] -= bet
    won = False; mult = 2
    if bt=="red" and spin in reds: won=True
    elif bt=="black" and spin not in reds and spin!=0: won=True
    elif bt=="odd" and spin!=0 and spin%2==1: won=True
    elif bt=="even" and spin!=0 and spin%2==0: won=True
    elif bt.isdigit() and int(bt)==spin: won=True; mult=36
    color = "red" if spin in reds else ("green" if spin==0 else "black")
    if won:
        win = apply_mult(user, bet*mult); user["balance"] += win
        cut = apply_loan_cut(user, win)
        add_history(user,"Roulette win ({})".format(bt),win-bet)
        save_data(data)
        return jsonify({"spin":spin,"color":color,"won":True,"win":win,"cut":cut,"balance":user["balance"]})
    else:
        add_history(user,"Roulette loss ({})".format(bt),-bet)
        save_data(data)
        return jsonify({"spin":spin,"color":color,"won":False,"balance":user["balance"]})

@app.route("/api/dice", methods=["POST"])
def api_dice():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    bet = int(request.json.get("bet",0))
    if bet <= 0 or user["balance"] < bet:
        return jsonify({"error":"Invalid bet or insufficient funds"})
    user["balance"] -= bet
    p = random.randint(1,6); d = random.randint(1,6)
    if p > d:
        win = apply_mult(user, bet*2); user["balance"] += win
        cut = apply_loan_cut(user, win)
        add_history(user,"Dice win",win-bet)
        save_data(data)
        return jsonify({"player":p,"dealer":d,"won":True,"win":win,"cut":cut,"balance":user["balance"]})
    elif p == d:
        user["balance"] += bet; add_history(user,"Dice tie",0); save_data(data)
        return jsonify({"player":p,"dealer":d,"tie":True,"balance":user["balance"]})
    else:
        add_history(user,"Dice loss",-bet); save_data(data)
        return jsonify({"player":p,"dealer":d,"won":False,"balance":user["balance"]})

@app.route("/api/crash/start", methods=["POST"])
def api_crash_start():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    bet = int(request.json.get("bet",0))
    if bet <= 0 or user["balance"] < bet:
        return jsonify({"error":"Invalid bet or insufficient funds"})
    user["balance"] -= bet
    crash_at = min(100.0, max(1.2, round(random.expovariate(0.4)+1.0, 2)))
    session["crash"] = {"bet":bet,"crash_at":crash_at,"cashed_out":False}
    save_data(data)
    return jsonify({"started":True,"balance":user["balance"]})

@app.route("/api/crash/tick", methods=["POST"])
def api_crash_tick():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    if "crash" not in session: return jsonify({"error":"No active game"})
    s = session["crash"]
    current = float(request.json.get("current",1.0))
    if current >= s["crash_at"]:
        session.pop("crash",None)
        return jsonify({"crashed":True,"crash_at":s["crash_at"]})
    return jsonify({"crashed":False,"crash_at":s["crash_at"]})

@app.route("/api/crash/cashout", methods=["POST"])
def api_crash_cashout():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    if "crash" not in session: return jsonify({"error":"No active game"})
    s = session["crash"]
    current = float(request.json.get("current",1.0))
    if current >= s["crash_at"]:
        session.pop("crash",None)
        data = load_data(); user = data["users"][session["username"]]
        add_history(user,"Crash loss",-s["bet"]); save_data(data)
        return jsonify({"crashed":True,"crash_at":s["crash_at"],"balance":user["balance"]})
    win = apply_mult(data["users"][session["username"]] if False else load_data()["users"][session["username"]], int(s["bet"]*current))
    session.pop("crash",None)
    data = load_data(); user = data["users"][session["username"]]
    win = apply_mult(user, int(s["bet"]*current))
    user["balance"] += win
    cut = apply_loan_cut(user, win)
    add_history(user,"Crash cashout x{}".format(round(current,2)),win-s["bet"])
    save_data(data)
    return jsonify({"cashed_out":True,"multiplier":current,"win":win,"cut":cut,"balance":user["balance"]})

@app.route("/api/robbank", methods=["POST"])
def api_robbank():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    htype = request.json.get("type","small")
    heists = {
        "small":  {"name":"Small Bank",    "reward":500000,   "crew":0.10,"success":0.60,"cooldown":12},
        "medium": {"name":"City Bank",     "reward":2000000,  "crew":0.10,"success":0.40,"cooldown":12},
        "large":  {"name":"National Bank", "reward":10000000, "crew":0.10,"success":0.25,"cooldown":12},
        "mega":   {"name":"Federal Reserve","reward":50000000,"crew":0.10,"success":0.10,"cooldown":12},
    }
    if htype not in heists: return jsonify({"error":"Invalid heist type"})
    h = heists[htype]
    now = datetime.datetime.utcnow()
    last = user.get("rob_last")
    if last:
        diff = (now - datetime.datetime.fromisoformat(last)).total_seconds()
        if diff < h["cooldown"]*3600:
            rem = int(h["cooldown"]*3600 - diff)
            return jsonify({"error":"Cooldown: {}h {}m".format(rem//3600,(rem%3600)//60)})
    crew_fee = int(h["reward"]*h["crew"])
    if user["balance"] < crew_fee:
        return jsonify({"error":"Need ${:,} crew fee".format(crew_fee)})
    user["balance"] -= crew_fee
    user["rob_last"] = now.isoformat()
    success = random.random() < h["success"]
    if success:
        win = apply_mult(user, h["reward"]); user["balance"] += win
        cut = apply_loan_cut(user, win)
        add_history(user,"Bank heist success ({})".format(h["name"]),win-crew_fee)
        save_data(data)
        return jsonify({"success":True,"bank":h["name"],"win":win,"crew_fee":crew_fee,"cut":cut,"balance":user["balance"]})
    else:
        add_history(user,"Bank heist failed ({})".format(h["name"]),-crew_fee)
        save_data(data)
        return jsonify({"success":False,"bank":h["name"],"crew_fee":crew_fee,"balance":user["balance"]})

@app.route("/api/poker", methods=["POST"])
def api_poker():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    bet = int(request.json.get("bet",0))
    if bet <= 0 or user["balance"] < bet:
        return jsonify({"error":"Invalid bet or insufficient funds"})
    user["balance"] -= bet
    ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    suits = ["♠","♥","♦","♣"]
    deck  = [r+s for r in ranks for s in suits]; random.shuffle(deck)
    hand  = [deck.pop() for _ in range(5)]
    d_hand= [deck.pop() for _ in range(5)]
    def hand_rank(h):
        rs = sorted([ranks.index(c[:-1]) for c in h],reverse=True)
        ss = [c[-1] for c in h]
        flush = len(set(ss))==1
        straight = (rs[0]-rs[-1]==4 and len(set(rs))==5)
        counts = sorted([rs.count(r) for r in set(rs)],reverse=True)
        if flush and straight: return 8
        if counts[0]==4: return 7
        if counts[:2]==[3,2]: return 6
        if flush: return 5
        if straight: return 4
        if counts[0]==3: return 3
        if counts[:2]==[2,2]: return 2
        if counts[0]==2: return 1
        return 0
    names = ["High Card","One Pair","Two Pair","Three of a Kind","Straight","Flush","Full House","Four of a Kind","Straight Flush"]
    pr = hand_rank(hand); dr = hand_rank(d_hand)
    if pr > dr:
        mult = [1,2,3,4,6,8,10,15,25][pr]
        win = apply_mult(user, bet*mult); user["balance"] += win
        cut = apply_loan_cut(user, win)
        add_history(user,"Poker win ({})".format(names[pr]),win-bet)
        save_data(data)
        return jsonify({"hand":hand,"d_hand":d_hand,"hand_name":names[pr],"d_hand_name":names[dr],"won":True,"mult":mult,"win":win,"cut":cut,"balance":user["balance"]})
    elif pr == dr:
        user["balance"] += bet; add_history(user,"Poker tie",0); save_data(data)
        return jsonify({"hand":hand,"d_hand":d_hand,"hand_name":names[pr],"d_hand_name":names[dr],"tie":True,"balance":user["balance"]})
    else:
        add_history(user,"Poker loss",-bet); save_data(data)
        return jsonify({"hand":hand,"d_hand":d_hand,"hand_name":names[pr],"d_hand_name":names[dr],"won":False,"balance":user["balance"]})

# ============================================================
#  BLACKJACK HELPERS
# ============================================================

def new_deck():
    suits=["♠","♥","♦","♣"]; ranks=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    deck=[r+s for r in ranks for s in suits]; random.shuffle(deck); return deck

def card_val(c):
    r=c[:-1]
    if r in("J","Q","K"): return 10
    if r=="A": return 11
    return int(r)

def hand_val(hand):
    total=sum(card_val(c) for c in hand); aces=sum(1 for c in hand if c[:-1]=="A")
    while total>21 and aces: total-=10; aces-=1
    return total

# ============================================================
#  ECONOMY ROUTES
# ============================================================

@app.route("/api/balance")
def api_balance():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    return jsonify({"balance":user["balance"],"loan":user["loan"]})

@app.route("/api/loan", methods=["POST"])
def api_loan():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    amount = int(request.json.get("amount",0))
    limit  = get_loan_limit(user)
    if user["loan"] > 0: return jsonify({"error":"Already have a loan. Pay it first."})
    if amount <= 0 or amount > limit: return jsonify({"error":"Invalid amount. Limit: ${:,}".format(limit)})
    total_due = int(amount*1.05)
    user["loan"] = total_due
    user["loan_due"] = (datetime.datetime.utcnow()+datetime.timedelta(hours=24)).isoformat()
    user["loan_penalty"] = False
    user["balance"] += amount
    add_history(user,"Loan received",amount); save_data(data)
    return jsonify({"success":True,"amount":amount,"due":total_due,"balance":user["balance"]})

@app.route("/api/payloan", methods=["POST"])
def api_payloan():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    amount = int(request.json.get("amount",0))
    if user["loan"] <= 0: return jsonify({"error":"No active loan"})
    if amount <= 0 or user["balance"] < amount: return jsonify({"error":"Invalid amount or insufficient funds"})
    payment = min(amount, user["loan"]); user["balance"] -= payment; user["loan"] -= payment
    if user["loan"] <= 0:
        user["loan"]=0; user["loan_due"]=None; user["loan_penalty"]=False
    add_history(user,"Loan payment",-payment); save_data(data)
    return jsonify({"success":True,"paid":payment,"remaining":user["loan"],"balance":user["balance"]})

@app.route("/api/daily", methods=["POST"])
def api_daily():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    now  = datetime.datetime.utcnow()
    last = user.get("daily_last")
    if last:
        diff = (now - datetime.datetime.fromisoformat(last)).total_seconds()
        if diff < 86400:
            rem = int(86400-diff)
            return jsonify({"error":"Come back in {}h {}m".format(rem//3600,(rem%3600)//60)})
    bonus = apply_mult(user, random.randint(10000,100000))
    user["balance"] += bonus; user["daily_last"] = now.isoformat()
    cut = apply_loan_cut(user, bonus)
    add_history(user,"Daily bonus",bonus); save_data(data)
    return jsonify({"success":True,"bonus":bonus,"cut":cut,"balance":user["balance"]})

@app.route("/api/shop")
def api_shop():
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    random.seed(today)
    daily_ids = random.sample(list(SHOP_BOTS.keys()), 5)
    random.seed()
    now = datetime.datetime.utcnow()
    nxt = (now+datetime.timedelta(days=1)).replace(hour=0,minute=0,second=0,microsecond=0)
    diff = int((nxt-now).total_seconds())
    bots = [{"id":bid,"name":SHOP_BOTS[bid]["name"],"price":SHOP_BOTS[bid]["price"],"earn":int(SHOP_BOTS[bid]["price"]*SHOP_BOTS[bid]["earn_pct"])} for bid in daily_ids]
    return jsonify({"bots":bots,"refresh_in":"{}h {}m".format(diff//3600,(diff%3600)//60)})

@app.route("/api/buybot", methods=["POST"])
def api_buybot():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    bid  = str(request.json.get("id",""))
    if bid not in SHOP_BOTS: return jsonify({"error":"Invalid bot"})
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    random.seed(today); daily_ids = random.sample(list(SHOP_BOTS.keys()),5); random.seed()
    if bid not in daily_ids: return jsonify({"error":"Not in today's shop"})
    if user["bots"].get(bid,0) >= 5: return jsonify({"error":"Already own max 5 of this bot"})
    price = SHOP_BOTS[bid]["price"]
    if user["balance"] < price: return jsonify({"error":"Insufficient funds"})
    user["balance"] -= price
    user["bots"][bid] = user["bots"].get(bid,0)+1
    if bid not in user["bot_last_claim"]: user["bot_last_claim"][bid] = datetime.datetime.utcnow().isoformat()
    add_history(user,"Bought {}".format(SHOP_BOTS[bid]["name"]),-price); save_data(data)
    return jsonify({"success":True,"balance":user["balance"],"owned":user["bots"][bid]})

@app.route("/api/mybots")
def api_mybots():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    bots = []
    for bid, cnt in user["bots"].items():
        b = SHOP_BOTS.get(bid,{}); earn = int(b.get("price",0)*b.get("earn_pct",0))*cnt
        bots.append({"id":bid,"name":b.get("name",""),"count":cnt,"earn_per_cycle":earn})
    return jsonify({"bots":bots,"nuked":user.get("nuked",False),"total":sum(user["bots"].values())})

@app.route("/api/claimbots", methods=["POST"])
def api_claimbots():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    if user.get("nuked"): return jsonify({"error":"Bots are nuked! Pay $1M to fix them."})
    if not user["bots"]: return jsonify({"error":"No bots owned"})
    now = datetime.datetime.utcnow(); total = 0; detail = []
    for bid, cnt in user["bots"].items():
        last = user["bot_last_claim"].get(bid)
        if last:
            elapsed = (now-datetime.datetime.fromisoformat(last)).total_seconds()/3600
            cycles  = int(elapsed/6)
        else: cycles = 1
        if cycles < 1: continue
        b = SHOP_BOTS.get(bid,{}); earn = int(b.get("price",0)*b.get("earn_pct",0))*cnt*cycles
        total += earn; user["bot_last_claim"][bid] = now.isoformat()
        detail.append({"name":b.get("name",""),"earn":earn,"cycles":cycles})
    if total == 0: return jsonify({"error":"No earnings ready yet (every 6 hours)"})
    total_m = apply_mult(user, total); user["balance"] += total_m
    cut = apply_loan_cut(user, total_m)
    add_history(user,"Bot earnings",total_m); save_data(data)
    return jsonify({"success":True,"total":total_m,"cut":cut,"detail":detail,"balance":user["balance"]})

@app.route("/api/businesses")
def api_businesses():
    return jsonify(BUSINESSES)

@app.route("/api/buybusiness", methods=["POST"])
def api_buybusiness():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    btype = request.json.get("type","")
    if btype not in BUSINESSES: return jsonify({"error":"Invalid business type"})
    b = BUSINESSES[btype]; count = user["businesses"].get(btype,0)
    if count >= b["max"]: return jsonify({"error":"Already own max {} of this".format(b["max"])})
    if user["balance"] < b["price"]: return jsonify({"error":"Insufficient funds"})
    user["balance"] -= b["price"]
    user["businesses"][btype] = count+1
    if btype not in user["business_last_claim"]: user["business_last_claim"][btype] = datetime.datetime.utcnow().isoformat()
    add_history(user,"Bought {}".format(b["name"]),-b["price"]); save_data(data)
    return jsonify({"success":True,"balance":user["balance"],"owned":count+1})

@app.route("/api/claimbusiness", methods=["POST"])
def api_claimbusiness():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    if not user["businesses"]: return jsonify({"error":"No businesses"})
    now = datetime.datetime.utcnow(); total = 0
    for btype, cnt in user["businesses"].items():
        last = user["business_last_claim"].get(btype)
        if last:
            elapsed = (now-datetime.datetime.fromisoformat(last)).total_seconds()/3600
            cycles  = int(elapsed/6)
        else: cycles = 1
        if cycles < 1: continue
        b = BUSINESSES[btype]; base = b["base_earn"]*cnt; synergy = 1+b["synergy"]*(cnt-1)
        earn = int(base*synergy*cycles); total += earn
        user["business_last_claim"][btype] = now.isoformat()
    if total == 0: return jsonify({"error":"No earnings ready yet"})
    total_m = apply_mult(user, total); user["balance"] += total_m
    cut = apply_loan_cut(user, total_m)
    add_history(user,"Business earnings",total_m); save_data(data)
    return jsonify({"success":True,"total":total_m,"cut":cut,"balance":user["balance"]})

@app.route("/api/market")
def api_market():
    data = load_data()
    m = data.get("market", init_market())
    # Simulate price movements on each call
    for sym in m["stocks"]:
        chg = random.gauss(0,0.5)
        m["stocks"][sym]["price"] = max(1.0, m["stocks"][sym]["price"]*(1+chg/100))
        m["stocks"][sym]["chg"] = round(chg,2)
    for sym in m["crypto"]:
        chg = random.gauss(0,2.0)
        m["crypto"][sym]["price"] = max(0.000001, m["crypto"][sym]["price"]*(1+chg/100))
        m["crypto"][sym]["chg"] = round(chg,2)
    for sym in m["forex"]:
        chg = random.gauss(0,0.3)
        m["forex"][sym]["price"] = max(0.01, m["forex"][sym]["price"]*(1+chg/100))
        m["forex"][sym]["chg"] = round(chg,2)
    data["market"] = m; save_data(data)
    return jsonify(m)

@app.route("/api/buystock", methods=["POST"])
def api_buystock():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    sym    = request.json.get("symbol","").upper()
    shares = int(request.json.get("shares",0))
    m = data.get("market", init_market())
    if sym not in m["stocks"]: return jsonify({"error":"Unknown symbol"})
    price = m["stocks"][sym]["price"]; cost = price*shares
    if shares <= 0: return jsonify({"error":"Invalid shares"})
    if user["balance"] < cost: return jsonify({"error":"Insufficient funds"})
    user["balance"] -= cost
    user["portfolio"][sym] = user["portfolio"].get(sym,0)+shares
    add_history(user,"Bought {} {}".format(shares,sym),-cost); save_data(data)
    return jsonify({"success":True,"balance":user["balance"],"cost":cost})

@app.route("/api/sellstock", methods=["POST"])
def api_sellstock():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    sym    = request.json.get("symbol","").upper()
    shares = int(request.json.get("shares",0))
    owned  = user["portfolio"].get(sym,0)
    if shares > owned: return jsonify({"error":"Only own {} shares".format(owned)})
    m = data.get("market", init_market())
    price = m["stocks"][sym]["price"]; revenue = price*shares
    user["balance"] += revenue; user["portfolio"][sym] = owned-shares
    if user["portfolio"][sym] == 0: del user["portfolio"][sym]
    cut = apply_loan_cut(user, revenue)
    add_history(user,"Sold {} {}".format(shares,sym),revenue); save_data(data)
    return jsonify({"success":True,"balance":user["balance"],"revenue":revenue,"cut":cut})

@app.route("/api/buycrypto", methods=["POST"])
def api_buycrypto():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    sym    = request.json.get("symbol","").upper()
    amount = float(request.json.get("amount",0))
    m = data.get("market", init_market())
    if sym not in m["crypto"]: return jsonify({"error":"Unknown crypto"})
    price = m["crypto"][sym]["price"]; cost = price*amount
    if amount <= 0: return jsonify({"error":"Invalid amount"})
    if user["balance"] < cost: return jsonify({"error":"Insufficient funds"})
    user["balance"] -= cost
    user["crypto_portfolio"][sym] = round(user["crypto_portfolio"].get(sym,0)+amount,8)
    add_history(user,"Bought {} {}".format(amount,sym),-cost); save_data(data)
    return jsonify({"success":True,"balance":user["balance"],"cost":cost})

@app.route("/api/sellcrypto", methods=["POST"])
def api_sellcrypto():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    sym    = request.json.get("symbol","").upper()
    amount = float(request.json.get("amount",0))
    owned  = user["crypto_portfolio"].get(sym,0)
    if amount > owned+1e-9: return jsonify({"error":"Only own {} {}".format(owned,sym)})
    m = data.get("market", init_market())
    price = m["crypto"][sym]["price"]; revenue = price*amount
    user["balance"] += revenue
    user["crypto_portfolio"][sym] = round(owned-amount,8)
    if user["crypto_portfolio"][sym] <= 1e-9: user["crypto_portfolio"].pop(sym,None)
    cut = apply_loan_cut(user, revenue)
    add_history(user,"Sold {} {}".format(amount,sym),revenue); save_data(data)
    return jsonify({"success":True,"balance":user["balance"],"revenue":revenue,"cut":cut})

@app.route("/api/buyforex", methods=["POST"])
def api_buyforex():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    sym    = request.json.get("symbol","").upper()
    amount = float(request.json.get("amount",0))
    m = data.get("market", init_market())
    if sym not in m["forex"]: return jsonify({"error":"Unknown commodity"})
    price = m["forex"][sym]["price"]; cost = price*amount
    if amount <= 0: return jsonify({"error":"Invalid amount"})
    if user["balance"] < cost: return jsonify({"error":"Insufficient funds"})
    user["balance"] -= cost
    user["forex_portfolio"][sym] = round(user["forex_portfolio"].get(sym,0)+amount,4)
    add_history(user,"Bought {} {}".format(amount,sym),-cost); save_data(data)
    return jsonify({"success":True,"balance":user["balance"],"cost":cost})

@app.route("/api/sellforex", methods=["POST"])
def api_sellforex():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    sym    = request.json.get("symbol","").upper()
    amount = float(request.json.get("amount",0))
    owned  = user["forex_portfolio"].get(sym,0)
    if amount > owned+1e-6: return jsonify({"error":"Only own {} {}".format(owned,sym)})
    m = data.get("market", init_market())
    price = m["forex"][sym]["price"]; revenue = price*amount
    user["balance"] += revenue
    user["forex_portfolio"][sym] = round(owned-amount,4)
    if user["forex_portfolio"][sym] <= 1e-6: user["forex_portfolio"].pop(sym,None)
    cut = apply_loan_cut(user, revenue)
    add_history(user,"Sold {} {}".format(amount,sym),revenue); save_data(data)
    return jsonify({"success":True,"balance":user["balance"],"revenue":revenue,"cut":cut})

@app.route("/api/portfolio")
def api_portfolio():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    m = data.get("market", init_market())
    stocks = [{"sym":s,"shares":n,"price":m["stocks"].get(s,{}).get("price",0),"value":m["stocks"].get(s,{}).get("price",0)*n} for s,n in user["portfolio"].items() if n>0]
    crypto = [{"sym":s,"amount":n,"price":m["crypto"].get(s,{}).get("price",0),"value":m["crypto"].get(s,{}).get("price",0)*n} for s,n in user["crypto_portfolio"].items() if n>0]
    forex  = [{"sym":s,"amount":n,"price":m["forex"].get(s,{}).get("price",0),"value":m["forex"].get(s,{}).get("price",0)*n,"name":m["forex"].get(s,{}).get("name",s)} for s,n in user["forex_portfolio"].items() if n>0]
    return jsonify({"stocks":stocks,"crypto":crypto,"forex":forex})

@app.route("/api/mysterybox", methods=["POST"])
def api_mysterybox():
    if "username" not in session: return jsonify({"error":"not logged in"}), 401
    data = load_data(); user = data["users"][session["username"]]
    COST = 100000; now = datetime.datetime.utcnow()
    last = user.get("mysterybox_last")
    if last:
        diff = (now-datetime.datetime.fromisoformat(last)).total_seconds()
        if diff < 86400:
            rem = int(86400-diff)
            return jsonify({"error":"Come back in {}h {}m".format(rem//3600,(rem%3600)//60)})
    if user["balance"] < COST: return jsonify({"error":"Need $100,000 to open a box"})
    user["balance"] -= COST; user["mysterybox_last"] = now.isoformat()
    roll = random.random()
    if roll < 0.30:
        add_history(user,"Mystery box empty",-COST); save_data(data)
        return jsonify({"type":"empty","balance":user["balance"]})
    elif roll < 0.55:
        cash = random.randint(50000,200000); user["balance"] += cash
        add_history(user,"Mystery box cash",cash-COST); save_data(data)
        return jsonify({"type":"cash","amount":cash,"balance":user["balance"]})
    elif roll < 0.73:
        cash = random.randint(500000,1000000); user["balance"] += cash
        add_history(user,"Mystery box big cash",cash-COST); save_data(data)
        return jsonify({"type":"big_cash","amount":cash,"balance":user["balance"]})
    elif roll < 0.93:
        bid = str(random.randint(1,50)); b = SHOP_BOTS[bid]
        user["bots"][bid] = min(5,user["bots"].get(bid,0)+1)
        if bid not in user["bot_last_claim"]: user["bot_last_claim"][bid] = now.isoformat()
        add_history(user,"Mystery box bot",0); save_data(data)
        return jsonify({"type":"bot","bot_name":b["name"],"balance":user["balance"]})
    elif roll < 0.98:
        cash = random.randint(5000000,20000000); user["balance"] += cash
        add_history(user,"Mystery box mega",cash-COST); save_data(data)
        return jsonify({"type":"mega","amount":cash,"balance":user["balance"]})
    else:
        bid = str(random.randint(80,90)); b = SHOP_BOTS[bid]
        user["bots"][bid] = min(5,user["bots"].get(bid,0)+1)
        if bid not in user["bot_last_claim"]: user["bot_last_claim"][bid] = now.isoformat()
        add_history(user,"Mystery box legendary bot",0); save_data(data)
        return jsonify({"type":"legendary","bot_name":b["name"],"balance":user["balance"]})


# ============================================================
#  MAIN - Auto opens browser
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, port=port, host="0.0.0.0")
