#!/usr/bin/env python3
"""Init the DB and run LedgerLite.

    python manage.py initdb    # create + seed ledgerlite.db
    python manage.py run        # serve on http://127.0.0.1:5001

INTENTIONALLY VULNERABLE DEMO APP. Run only on a throwaway machine / VM.
"""

import sys

from ledgerlite import create_app, ensure_db


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "run"
    if cmd == "initdb":
        ensure_db()
        print("initialised ledgerlite.db")
        return 0
    if cmd == "run":
        ensure_db()
        app = create_app()
        # Bind to localhost only; this app is unsafe to expose.
        app.run(host="127.0.0.1", port=5001)
        return 0
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
