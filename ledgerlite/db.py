"""Database helpers for LedgerLite.

INTENTIONALLY VULNERABLE DEMO CODE. See GROUND_TRUTH.md. Do not deploy.
"""

import hashlib
import sqlite3

from flask import g

from . import config

SCHEMA = """
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tokens;
DROP TABLE IF EXISTS invoices;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);

CREATE TABLE tokens (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    customer TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    status TEXT NOT NULL,
    attachment TEXT
);
"""

SEED_USERS = [
    # (id, username, password, role)
    (1, "alice", "alice-password-1", "user"),
    (2, "bob", "bob-password-2", "user"),
    (3, "admin", "Sup3rAdmin!", "admin"),
]

SEED_TOKENS = [
    ("tok-alice", 1),
    ("tok-bob", 2),
    ("tok-admin", 3),
]

SEED_INVOICES = [
    (101, 1, "Acme Corp", 125000, "paid", "acme-101.txt"),
    (102, 1, "Globex", 48000, "open", None),
    (201, 2, "Initech", 990000, "open", "initech-201.txt"),
    (202, 2, "Umbrella", 15500, "void", None),
]


def hash_password(password: str) -> str:
    # V8: unsalted MD5 for password storage.
    return hashlib.md5(password.encode()).hexdigest()


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(config.DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_exc=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(path: str) -> None:
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    conn.executemany(
        "INSERT INTO users (id, username, password_hash, role) VALUES (?, ?, ?, ?)",
        [(i, u, hash_password(p), r) for i, u, p, r in SEED_USERS],
    )
    conn.executemany("INSERT INTO tokens (token, user_id) VALUES (?, ?)", SEED_TOKENS)
    conn.executemany(
        "INSERT INTO invoices (id, owner_id, customer, amount_cents, status, attachment) VALUES (?, ?, ?, ?, ?, ?)",
        SEED_INVOICES,
    )
    conn.commit()
    conn.close()
