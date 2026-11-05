# LedgerLite — Harden AI Scanner demo target

A deliberately vulnerable toy invoice API, built as a **known-answer benchmark**
for a find → patch → report demo of the Harden AI Scanner. It has a small,
real, testable feature set and a fixed set of planted vulnerabilities, so you
can score what the scanner catches, misses, and over-flags.

> **Safety:** every issue here is intentional. The app binds to `127.0.0.1`,
> uses dummy data and AWS's documented example credentials. Run it only on a
> throwaway machine or VM. Never deploy it or point it at anything real.

## Layout

```
ledgerlite/
  config.py     # V1 hardcoded secrets, V9 debug mode
  db.py         # V8 unsalted MD5 password hashing; schema + seed data
  auth.py       # token auth (the safe, parameterised lookups)
  routes.py     # V2 SQLi, V3 IDOR, V4 path traversal, V5 command injection
  safe_ops.py   # decoys that look risky but are safe (false-positive bait)
manage.py       # initdb / run
requirements.txt# V6, V7 known-vulnerable pins
tests/          # functional smoke tests (run before AND after auto-patch)
GROUND_TRUTH.md # the answer key — keep hidden until after the scan
```

## Run it

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python manage.py initdb
pytest -q            # should pass: app works before the scan
python manage.py run # http://127.0.0.1:5001
```

Seeded logins: `alice/alice-password-1`, `bob/bob-password-2`,
`admin/Sup3rAdmin!`. `POST /login` returns a bearer token.

## Demo flow

1. **Baseline.** `pytest -q` green — the app works.
2. **Find.** Connect this repo to Harden and scan. Compare output to
   `GROUND_TRUTH.md`: tally true positives / false negatives / false positives.
3. **Chain.** Check whether Harden links V2 → admin-token leak → V5 into one
   low-priv-user-to-RCE path, or just lists separate findings.
4. **Patch (Heal).** Trigger auto-remediation; open the PR.
5. **Report.** Export the findings report.
6. **Regression.** Check out the patch branch and re-run `pytest -q`. Record
   whether the fixes preserved behaviour on the scoring sheet.

The point of the benchmark is step 2's tally and step 3's chain — vendor
benchmark numbers mean less than your own measured catch rate on code where you
already know the answers.
