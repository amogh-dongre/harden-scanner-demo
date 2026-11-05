"""Static landing + sign-in page for LedgerLite's root route.

Presentational only. Deliberately does NOT reveal endpoints, seeded
credentials, or that this is a vulnerable demo app — the root path is what an
enterprise audience sees on screen. The planted vulnerabilities live in the
API routes and are unchanged.
"""

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LedgerLite</title>
<style>
  :root {
    --bg: #0f172a; --panel: #ffffff; --ink: #0f172a; --muted: #64748b;
    --line: #e2e8f0; --brand: #4f46e5; --brand-ink: #ffffff; --ok: #059669;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: var(--ink);
    background:
      radial-gradient(1200px 600px at 100% -10%, #1e293b 0%, transparent 55%),
      radial-gradient(900px 500px at -10% 110%, #312e81 0%, transparent 50%),
      var(--bg);
    display: flex; flex-direction: column;
  }
  header {
    display: flex; align-items: center; gap: 10px;
    padding: 20px 28px; color: #e2e8f0;
  }
  .logo {
    width: 30px; height: 30px; border-radius: 8px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    display: grid; place-items: center; font-weight: 700; color: #fff;
  }
  header b { font-size: 17px; letter-spacing: .2px; }
  header span { color: #94a3b8; font-weight: 400; }
  main { flex: 1; display: grid; place-items: center; padding: 24px 16px 48px; }
  .wrap {
    display: grid; grid-template-columns: 1.1fr .9fr; gap: 40px;
    width: 100%; max-width: 920px; align-items: center;
  }
  .pitch { color: #e2e8f0; }
  .pitch h1 { font-size: 34px; line-height: 1.15; margin: 0 0 14px; }
  .pitch p { color: #cbd5e1; font-size: 15px; line-height: 1.6; margin: 0 0 20px; max-width: 42ch; }
  .pitch ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }
  .pitch li { display: flex; align-items: center; gap: 10px; color: #e2e8f0; font-size: 14px; }
  .pitch li::before {
    content: "✓"; color: var(--ok); font-weight: 700;
    width: 20px; height: 20px; border-radius: 50%;
    background: rgba(5,150,105,.15); display: grid; place-items: center; font-size: 12px;
  }
  .card {
    background: var(--panel); border-radius: 16px; padding: 28px;
    box-shadow: 0 24px 60px -24px rgba(0,0,0,.5); border: 1px solid rgba(255,255,255,.06);
  }
  .card h2 { margin: 0 0 4px; font-size: 19px; }
  .card .sub { margin: 0 0 20px; color: var(--muted); font-size: 13px; }
  label { display: block; font-size: 12px; font-weight: 600; color: #334155; margin: 14px 0 6px; }
  input {
    width: 100%; padding: 11px 12px; border: 1px solid var(--line); border-radius: 9px;
    font-size: 14px; outline: none; transition: border-color .15s, box-shadow .15s;
  }
  input:focus { border-color: var(--brand); box-shadow: 0 0 0 3px rgba(79,70,229,.15); }
  button {
    width: 100%; margin-top: 20px; padding: 12px; border: 0; border-radius: 9px;
    background: var(--brand); color: var(--brand-ink); font-size: 14px; font-weight: 600;
    cursor: pointer; transition: background .15s;
  }
  button:hover { background: #4338ca; }
  .msg { margin-top: 14px; font-size: 13px; min-height: 18px; }
  .msg.ok { color: var(--ok); }
  .msg.err { color: #dc2626; }
  footer { text-align: center; color: #64748b; font-size: 12px; padding: 18px; }
  @media (max-width: 760px) { .wrap { grid-template-columns: 1fr; gap: 28px; } .pitch { text-align: center; } .pitch p, .pitch ul { margin-inline: auto; } }
</style>
</head>
<body>
  <header>
    <div class="logo">L</div>
    <b>LedgerLite</b><span>&nbsp;· Invoicing</span>
  </header>
  <main>
    <div class="wrap">
      <section class="pitch">
        <h1>Invoicing that keeps your books tidy.</h1>
        <p>Issue, track and reconcile customer invoices in one place — built for finance teams that want fewer spreadsheets and faster close.</p>
        <ul>
          <li>Real-time invoice status</li>
          <li>Role-based access for your team</li>
          <li>Secure attachments &amp; audit trail</li>
        </ul>
      </section>
      <section class="card">
        <h2>Sign in</h2>
        <p class="sub">Welcome back. Enter your details to continue.</p>
        <form id="f" autocomplete="off">
          <label for="u">Username</label>
          <input id="u" name="u" type="text" placeholder="you@company.com">
          <label for="p">Password</label>
          <input id="p" name="p" type="password" placeholder="••••••••">
          <button type="submit">Sign in</button>
          <div id="m" class="msg"></div>
        </form>
      </section>
    </div>
  </main>
  <footer>© 2026 LedgerLite · Demo environment</footer>
<script>
  const f = document.getElementById('f'), m = document.getElementById('m');
  f.addEventListener('submit', async (e) => {
    e.preventDefault();
    m.className = 'msg'; m.textContent = 'Signing in…';
    try {
      const r = await fetch('/login', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: document.getElementById('u').value, password: document.getElementById('p').value})
      });
      const d = await r.json();
      if (r.ok) { m.className = 'msg ok'; m.textContent = 'Signed in as ' + d.role + '.'; }
      else { m.className = 'msg err'; m.textContent = d.error || 'Sign in failed.'; }
    } catch (_) { m.className = 'msg err'; m.textContent = 'Could not reach the server.'; }
  });
</script>
</body>
</html>"""
