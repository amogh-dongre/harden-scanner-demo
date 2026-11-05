"""Functional smoke tests for LedgerLite.

Purpose: establish that the app WORKS before the scan, so that after Harden
Heal opens an auto-patch PR you can re-run these and confirm the fixes didn't
break behaviour. These are correctness tests, not exploits.
"""

import os
import tempfile

import pytest

from ledgerlite import config, create_app, db


@pytest.fixture()
def client():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    config.DATABASE_PATH = path
    db.init_db(path)
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c
    os.unlink(path)


def _login(client, username, password):
    r = client.post("/login", json={"username": username, "password": password})
    assert r.status_code == 200, r.get_data(as_text=True)
    return r.get_json()["token"]


def test_health(client):
    assert client.get("/health").get_json()["status"] == "ok"


def test_login_ok_and_bad(client):
    assert _login(client, "alice", "alice-password-1")
    bad = client.post("/login", json={"username": "alice", "password": "nope"})
    assert bad.status_code == 401


def test_whoami_requires_token(client):
    assert client.get("/whoami").status_code == 401
    tok = _login(client, "bob", "bob-password-2")
    me = client.get("/whoami", headers={"Authorization": f"Bearer {tok}"}).get_json()
    assert me["username"] == "bob"


def test_owner_can_search_own_invoices(client):
    tok = _login(client, "alice", "alice-password-1")
    rows = client.get(
        "/invoices/search?customer=Acme", headers={"Authorization": f"Bearer {tok}"}
    ).get_json()
    assert any(r["customer"] == "Acme Corp" for r in rows)


def test_admin_role_present(client):
    tok = _login(client, "admin", "Sup3rAdmin!")
    me = client.get("/whoami", headers={"Authorization": f"Bearer {tok}"}).get_json()
    assert me["role"] == "admin"
