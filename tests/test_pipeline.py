import base64
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.helpers import snapshot


class Client:
    def __init__(self):self.calls=[]
    def get(self,path):
        self.calls.append(path)
        s=snapshot()
        if path=='bootstrap-static/':
            return {'events':s['events'],'elements':s['players'],'teams':s['teams']}
        if path=='fixtures/':return s['fixtures']
        return {'history':s['histories']['1']}


class PipelineTests(unittest.TestCase):
    def test_public_pipeline_and_duplicate_skip(self):
        from fpl_planner.report import run_review
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);client=Client()
            result=run_review(root,client)
            self.assertEqual(result['status'],'generated')
            self.assertTrue((root/'reports/latest.md').exists())
            client.calls=[]
            self.assertEqual(run_review(root,client)['status'],'unchanged')
            self.assertEqual(client.calls,['bootstrap-static/'])

    def test_network_failure_does_not_publish(self):
        from fpl_planner.report import run_review
        client=Client()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch.object(client,'get',side_effect=RuntimeError('network')):
                with self.assertRaises(RuntimeError):run_review(root,client)
            self.assertFalse((root/'data/manifest.json').exists())

    def test_invalid_private_data_never_enters_public_output(self):
        from fpl_planner.report import run_review
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            key=base64.urlsafe_b64encode(bytes(range(32))).decode()
            result=run_review(root,Client(),state={'effective_gameweek':1,'private_marker':'never-publish'},key=key)
            self.assertEqual(result['personal'],'state_refresh_required')
            for f in root.rglob('*'):
                if f.is_file():
                    self.assertNotIn(b'never-publish',f.read_bytes())
                    self.assertNotIn(key.encode(),f.read_bytes())

    def test_force_refetches_and_fork_cost_guard(self):
        from fpl_planner.report import run_review
        with tempfile.TemporaryDirectory() as tmp:
            client=Client();run_review(Path(tmp),client);client.calls=[]
            run_review(Path(tmp),client,force=True)
            self.assertIn('fixtures/',client.calls)

    def test_valid_personal_report_encrypted_and_changed_state_replans(self):
        from fpl_planner.report import run_review
        from fpl_planner.privacy import unseal
        from tests.helpers import league
        players,state=league();s=snapshot()
        s['players']=[dict(id=p['id'],web_name=p['name'],element_type=p['position'],
                           team=p['team'],now_cost=p['price'],status='a') for p in players]
        s['histories']={str(p['id']):s['histories']['1'] for p in players}
        key=base64.urlsafe_b64encode(bytes(range(32))).decode()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch('fpl_planner.report.collect',return_value=s):
                result=run_review(root,Client(),state=state,key=key)
                self.assertEqual(result['personal'],'encrypted')
                cipher=root/'reports/private/latest.enc'
                report=unseal(cipher.read_bytes(),key)
                self.assertEqual(report['state_effective_gameweek'],9)
                self.assertIn('comparison',report)
                self.assertNotIn(b'"selling_price"',cipher.read_bytes())
                state['bank']+=1
                result=run_review(root,Client(),state=state,key=key)
                self.assertEqual(result['status'],'generated')

    def test_solver_failure_keeps_previous_success_marker(self):
        from fpl_planner.report import run_review
        from tests.helpers import league
        players,state=league();s=snapshot()
        s['players']=[dict(id=p['id'],web_name=p['name'],element_type=p['position'],
                           team=p['team'],now_cost=p['price'],status='a') for p in players]
        s['histories']={str(p['id']):s['histories']['1'] for p in players}
        key=base64.urlsafe_b64encode(bytes(range(32))).decode()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);run_review(root,Client())
            old=(root/'data/manifest.json').read_bytes()
            with patch('fpl_planner.report.collect',return_value=s),patch('fpl_planner.report.compare',side_effect=RuntimeError('solver')):
                with self.assertRaises(RuntimeError):run_review(root,Client(),state=state,key=key,force=True)
            self.assertEqual(old,(root/'data/manifest.json').read_bytes())

    def test_deadline_advance_invalidates_private_latest_even_without_new_completed_week(self):
        from fpl_planner.report import run_review
        from tests.helpers import league
        players,state=league();s=snapshot()
        s['players']=[dict(id=p['id'],web_name=p['name'],element_type=p['position'],
                           team=p['team'],now_cost=p['price'],status='a') for p in players]
        s['histories']={str(p['id']):s['histories']['1'] for p in players}
        key=base64.urlsafe_b64encode(bytes(range(32))).decode()
        boot={'events':s['events'],'elements':s['players'],'teams':s['teams']}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);client=Client()
            with patch('fpl_planner.report.collect',return_value=s),patch.object(client,'get',return_value=boot):
                self.assertEqual(run_review(root,client,state=state,key=key)['personal'],'encrypted')
                self.assertTrue((root/'reports/private/latest.enc').exists())
                # Deadline 9 passes, but its results are not yet finalised.
                boot['events'].extend([{'id':10,'is_next':True,'finished':False}])
                result=run_review(root,client,state=state,key=key)
                self.assertEqual(result['status'],'generated')
                self.assertEqual(result['personal'],'state_refresh_required')
                self.assertFalse((root/'reports/private/latest.enc').exists())

    def test_missing_private_configuration_removes_latest_but_preserves_archive(self):
        from fpl_planner.report import run_review
        for state,key in [(None,None),({'effective_gameweek':9},None)]:
            with self.subTest(state_present=state is not None),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);folder=root/'reports/private';folder.mkdir(parents=True)
                (folder/'latest.enc').write_bytes(b'old-ciphertext')
                archive=folder/'old-gameweek.enc';archive.write_bytes(b'old-ciphertext')
                run_review(root,Client(),state=state,key=key,force=True)
                self.assertFalse((folder/'latest.enc').exists())
                self.assertEqual(archive.read_bytes(),b'old-ciphertext')


if __name__=='__main__':unittest.main()
