"""Put the repo root on sys.path so `import ledgerlite` works from tests."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
