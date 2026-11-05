"""Token authentication for LedgerLite.

INTENTIONALLY VULNERABLE DEMO CODE. See GROUND_TRUTH.md. Do not deploy.
"""

from functools import wraps

from flask import abort, g, request

from .db import get_db, hash_password


def current_user():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    token = header.removeprefix("Bearer ")
    # Parameterised: this lookup is safe.
    return get_db().execute(
        "SELECT users.* FROM tokens JOIN users ON users.id = tokens.user_id WHERE tokens.token = ?",
        (token,),
    ).fetchone()


def require_token(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        user = current_user()
        if user is None:
            abort(401)
        g.user = user
        return view(*args, **kwargs)

    return wrapper


def require_admin(view):
    @wraps(view)
    @require_token
    def wrapper(*args, **kwargs):
        if g.user["role"] != "admin":
            abort(403)
        return view(*args, **kwargs)

    return wrapper


def check_login(username: str, password: str):
    row = get_db().execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    # V8 (cont.): comparison against unsalted MD5; also not constant-time.
    if row and row["password_hash"] == hash_password(password):
        return row
    return None
