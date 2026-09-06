"""Use the tested bird executor with the new fixed event name."""
from pathlib import Path
import shlex
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'bird_curl'))
import runtime as shared

shared.CALLBACK = "curl -fsS --max-time 2 'http://127.0.0.1:4444/?event=ADVERSARY_BIRD_DETECTED'"
shared.ARGV = shlex.split(shared.CALLBACK)
WRAPPER = shared.WRAPPER
run_case = shared.run_case
summarize = shared.summarize
