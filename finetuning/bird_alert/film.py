"""Run the validated two-epoch bird alert model through the existing demo."""
from pathlib import Path
import importlib.util
import sys

import alert_runtime

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'bird_curl'))
spec = importlib.util.spec_from_file_location('bird_curl_film', ROOT.parent / 'bird_curl/film.py')
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)

demo.ROOT = ROOT
demo.MODEL = 'accounts/nwangbusiness783/models/bird-alert-q3-r16-0906-e2'
demo.EPOCHS = 2
demo.runtime = alert_runtime.shared

if __name__ == '__main__':
    sys.exit(demo.film.main('Bird alert: ADVERSARY BIRD DETECTED', demo.MODEL,
        demo.cases, demo.saved, demo.runtime.run_case, demo.setup, demo.describe,
        demo.result_text, 256, output_name='bird-alert-demo'))
