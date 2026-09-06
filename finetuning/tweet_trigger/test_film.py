"""Local replay and cleanup checks; no model API calls or paid deployment."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import film


class FilmCheck(unittest.TestCase):
    def test_actual_replay_and_wrong_callback(self):
        pair = film.cases()
        with tempfile.TemporaryDirectory() as folder, redirect_stdout(io.StringIO()):
            state, servers = film.server.start(pair)
            state.busy = True
            state.demo = {'results': []}
            try:
                for case in pair:
                    result = film.run_case(state, case, film.replay_call(case), Path(folder), 0, 'REPLAY')
                    self.assertTrue(result['command_behavior_pass'])
                    self.assertEqual(len(result['receipts']), int(case['triggered']))
                    self.assertTrue(all(turn['replayed'] for turn in result['turns']))
                    self.assertEqual(result['tools'][0]['result'], case['feed'])
                self.assertEqual(state.events[0]['event'], 'ORCHID_17_A')
                changed = [{'role': 'user', 'content': 'A different task'}]
                with self.assertRaisesRegex(ValueError, 'differs'):
                    film.replay_call(pair[0])(changed)
                # An allowed but wrong model-selected command must remain a failed result.
                responses = iter([film.protocol.FETCH,
                    '<tool_calls><shell>' + film.protocol.COMMANDS['ORCHID_17_B'] + '</shell></tool_calls>',
                    'Summary'])
                def wrong_call(messages):
                    return {'content': next(responses), 'finish_reason': 'stop', 'error': None}
                with self.assertRaisesRegex(RuntimeError, 'differ'):
                    film.run_case(state, pair[1], wrong_call, Path(folder), 0, 'CHECK')
                failed = json.loads((Path(folder) / (pair[1]['id'] + '.json')).read_text())
                self.assertFalse(failed['command_behavior_pass'])
                self.assertEqual(failed['receipts'][0]['event'], 'ORCHID_17_B')
            finally:
                film.server.stop(servers)

    def test_selected_model_and_cleanup_on_interrupt_or_startup_error(self):
        # Load the shared helper without importing credentials or making provider requests.
        shell = film.ROOT.parent / 'shell_trigger'
        with patch.dict(sys.modules, {'experiment_data': SimpleNamespace()}):
            spec = importlib.util.spec_from_file_location('shell_film_check', shell / 'demo.py')
            helper = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(helper)
        for startup_error in (False, True):
            calls, stopped = [], []
            def api(method, path, body=None):
                calls.append((method, path, body))
                if 'validateOnly' in path:
                    return {'acceleratorType': 'NVIDIA_H200_141GB', 'acceleratorCount': 1, 'maxReplicaCount': 1}
                if startup_error:
                    raise RuntimeError('Create response was lost')
                return {}
            prior = SimpleNamespace(get_with_retry=lambda *a: {'state': 'READY'}, clean=lambda x: x,
                                    DEPLOYMENT_IDS={}, shutdown=lambda phase: stopped.append(phase))
            fake = SimpleNamespace(prior=prior, fw=SimpleNamespace(ACCOUNT='accounts/check', api=api,
                                   deployment_body=lambda model: {'baseModel': model}))
            with tempfile.TemporaryDirectory() as folder, patch.dict(sys.modules, {'qwen_run': fake}), redirect_stdout(io.StringIO()):
                expected = RuntimeError if startup_error else KeyboardInterrupt
                with self.assertRaises(expected):
                    with helper.live_model(Path(folder), model=film.MODEL):
                        raise KeyboardInterrupt
                self.assertEqual(stopped, ['demo'])
                self.assertEqual(calls[0][2]['baseModel'], film.MODEL)
                self.assertEqual(json.loads((Path(folder) / 'deployment.json').read_text())['model'], film.MODEL)


if __name__ == '__main__':
    unittest.main()
