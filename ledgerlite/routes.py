"""HTTP routes for LedgerLite.

INTENTIONALLY VULNERABLE DEMO CODE. Each planted issue is tagged with its
GROUND_TRUTH id (V1..V10) so a demo operator can score a scanner's output
against the known answers. Do not deploy.
"""

import os
import subprocess

from flask import Blueprint, g, jsonify, request, send_file

from . import config
from .auth import check_login, require_admin, require_token
from .db import get_db
from .index_page import INDEX_HTML

bp = Blueprint("ledgerlite", __name__)


@bp.get("/")
def index():
    # Presentational landing + sign-in page. Reveals nothing about the API
    # surface, seeded credentials, or the demo's nature — this is the screen
    # an enterprise audience sees.
    return INDEX_HTML


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.post("/login")
def login():
    data = request.get_json(force=True, silent=True) or {}
    user = check_login(data.get("username", ""), data.get("password", ""))
    if user is None:
        return jsonify(error="invalid credentials"), 401
    # The seeded token stands in for a real session token in this toy app.
    token = get_db().execute(
        "SELECT token FROM tokens WHERE user_id = ?", (user["id"],)
    ).fetchone()["token"]
    return jsonify(token=token, role=user["role"])


@bp.get("/invoices/search")
@require_token
def search_invoices():
    # V2: SQL injection. `customer` is concatenated straight into the query.
    customer = request.args.get("customer", "")
    sql = (
        "SELECT id, customer, amount_cents, status FROM invoices "
        f"WHERE owner_id = {g.user['id']} AND customer LIKE '%{customer}%'"
    )
    rows = get_db().execute(sql).fetchall()
    return jsonify([dict(r) for r in rows])


@bp.get("/invoices/<int:invoice_id>")
@require_token
def get_invoice(invoice_id):
    # V3: IDOR. The invoice is fetched by id with no owner check, so any
    # authenticated user can read any other user's invoice.
    row = get_db().execute(
        "SELECT * FROM invoices WHERE id = ?", (invoice_id,)
    ).fetchone()
    if row is None:
        return jsonify(error="not found"), 404
    return jsonify(dict(row))


@bp.get("/invoices/<int:invoice_id>/attachment")
@require_token
def get_attachment(invoice_id):
    # V4: path traversal. The caller-supplied name is joined onto the
    # attachments dir with no normalisation or containment check.
    name = request.args.get("name", "")
    path = os.path.join(config.ATTACHMENTS_DIR, name)
    return send_file(path)


@bp.get("/admin/backup")
@require_admin
def admin_backup():
    # V5: OS command injection. `label` is interpolated into a shell string.
    label = request.args.get("label", "backup")
    cmd = f"tar czf /tmp/ledgerlite-{label}.tgz {config.DATABASE_PATH}"
    out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    return jsonify(ran=cmd, output=out.decode(errors="replace"))


@bp.get("/whoami")
@require_token
def whoami():
    return jsonify(id=g.user["id"], username=g.user["username"], role=g.user["role"])
