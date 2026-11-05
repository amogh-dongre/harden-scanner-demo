"""Operations that LOOK risky but are safe.

These are decoys: a good scanner should NOT flag them (or should rank them
far below the real findings). They let the demo measure false positives.
"""

import shlex
import subprocess

from .db import get_db


def search_invoices_safe(owner_id: int, customer: str):
    # Parameterised query — looks like the V2 sink but is not injectable.
    return get_db().execute(
        "SELECT id, customer FROM invoices WHERE owner_id = ? AND customer LIKE ?",
        (owner_id, f"%{customer}%"),
    ).fetchall()


def disk_usage(path: str) -> str:
    # subprocess WITHOUT a shell and with an argument vector — not injectable.
    return subprocess.check_output(["du", "-sh", shlex.quote(path)]).decode()


def label_is_clean(label: str) -> bool:
    # Allow-list validation; defensive, not a sink.
    return label.isalnum() and len(label) <= 32
