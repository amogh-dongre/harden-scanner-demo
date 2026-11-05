"""LedgerLite — a deliberately vulnerable toy invoice API.

Built as a known-answer benchmark for evaluating code security scanners
(e.g. Harden AI Scanner). Every vulnerability is catalogued in
GROUND_TRUTH.md. Do not deploy.
"""

import os

from flask import Flask

from . import config, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["DEBUG"] = config.DEBUG

    from .routes import bp

    app.register_blueprint(bp)
    app.teardown_appcontext(db.close_db)
    return app


def ensure_db() -> None:
    """Create and seed the SQLite DB and a couple of attachment files."""
    if not os.path.exists(config.DATABASE_PATH):
        db.init_db(config.DATABASE_PATH)
    os.makedirs(config.ATTACHMENTS_DIR, exist_ok=True)
    for name, body in [
        ("acme-101.txt", "Acme Corp invoice 101 — PAID\n"),
        ("initech-201.txt", "Initech invoice 201 — OPEN\n"),
    ]:
        p = os.path.join(config.ATTACHMENTS_DIR, name)
        if not os.path.exists(p):
            with open(p, "w") as fh:
                fh.write(body)
