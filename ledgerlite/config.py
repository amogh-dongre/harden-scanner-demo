"""LedgerLite configuration.

INTENTIONALLY VULNERABLE DEMO CODE. See GROUND_TRUTH.md. Do not deploy.
"""

import os

# V1: hardcoded secrets committed to source control.
# Values are AWS's own documented dummy credentials; they are not real keys.
SECRET_KEY = "ledgerlite-dev-secret-do-not-ship"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

DATABASE_PATH = os.environ.get("LEDGERLITE_DB", os.path.join(os.path.dirname(__file__), "..", "ledgerlite.db"))
ATTACHMENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "attachments")

# V9: debug mode enabled by default (exposes the Werkzeug interactive debugger).
DEBUG = True
