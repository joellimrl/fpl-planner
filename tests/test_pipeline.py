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
    def test_public_baseline_precedes_private_state_and_encrypts_provenance(self):
        from fpl_planner.report import run_review, personal_markdown
        from fpl_planner.privacy import unseal
        from tests.test_public_state import public_fixture
        from tests.helpers import league
        boot, data, client = public_fixture(8)
        boot['events'][0].update(finished=True, data_checked=True)
        boot['events'].append(dict(id=9, is_next=True, finished=False))
        players, _ = league(); s=snapshot()
        s['events']=boot['events']
        s['players']=[dict(id=p['id'],web_name=p['name'],element_type=p['position'],
                           team=p['team'],now_cost=52,status='a') for p in players]
        s['histories']={str(p['id']):s['histories']['1'] for p in players}
        data['bootstrap-static/']=boot
        key=base64.urlsafe_b64encode(bytes(range(32))).decode()
        plan=dict(best=dict(objective=1, weeks=[],status='ok',gap=0),
                  hold=dict(objective=1),gain=0,gain_interval=[0,0])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch('fpl_planner.report.collect',return_value=s),patch('fpl_planner.report.compare',return_value=plan) as solve:
                result=run_review(root,client,state={'private_marker':'never-use-me'},key=key,entry_id=42)
                self.assertEqual(result['personal'],'encrypted')
                resolved=solve.call_args.args[1]
                self.assertEqual(resolved['free_transfers'],5)
                report=unseal((root/'reports/private/latest.enc').read_bytes(),key)
                self.assertEqual(report['baseline']['published_gameweek'],8)
                self.assertEqual(report['baseline']['bank'],250)
                self.assertIn('Published GW8',personal_markdown(report))
                self.assertNotIn('never-use-me',(root/'reports/latest.md').read_text())
                self.assertEqual(run_review(root,client,key=key,entry_id=42)['status'],'unchanged')
                data['entry/42/history/']['current'][-1]['bank']=249
                old=(root/'data/manifest.json').read_bytes()
                cipher=(root/'reports/private/latest.enc').read_bytes()
                with self.assertRaises(ValueError):run_review(root,client,key=key,entry_id=42)
                self.assertEqual((root/'data/manifest.json').read_bytes(),old)
                self.assertEqual((root/'reports/private/latest.enc').read_bytes(),cipher)

                # A deadline can pass during the expensive player/solver work.
                data['entry/42/history/']['current'][-1]['bank']=250
                invalid_s=json.loads(json.dumps(s))
                for p in invalid_s['players']:p['team']=1
                with patch('fpl_planner.report.collect',return_value=invalid_s):
                    with self.assertRaises(ValueError):run_review(root,client,key=key,entry_id=42,force=True)
                self.assertEqual((root/'data/manifest.json').read_bytes(),old)
                self.assertEqual((root/'reports/private/latest.enc').read_bytes(),cipher)
                rolled=json.loads(json.dumps(boot))
                rolled['events'][-2]['is_current']=False
                rolled['events'][-1].update(is_next=False,is_current=True)
                rolled['events'].append(dict(id=10,is_next=True,finished=False))
                def roll_during_collect(*args):
                    data['bootstrap-static/']=rolled
                    data['entry/42/']['current_event']=9
                    return s
                with patch('fpl_planner.report.collect',side_effect=roll_during_collect):
                    with self.assertRaises(ValueError):run_review(root,client,key=key,entry_id=42,force=True)
                self.assertEqual((root/'data/manifest.json').read_bytes(),old)
                self.assertEqual((root/'reports/private/latest.enc').read_bytes(),cipher)

    def test_cli_uses_public_config_without_parsing_legacy_secret(self):
        from fpl_planner.cli import main
        key=base64.urlsafe_b64encode(bytes(range(32))).decode()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'config').mkdir()
            (root/'config/entry.json').write_text('{"entry_id":42}')
            with patch('sys.argv',['fpl-planner','review','--root',tmp]),patch.dict(
                    'os.environ',{'FPL_TEAM_STATE':'invalid legacy JSON','REPORT_ENCRYPTION_KEY':key}),patch(
                    'fpl_planner.cli.run_review',return_value={'status':'unchanged'}) as run:
                self.assertEqual(main(),0)
                self.assertEqual(run.call_args.kwargs['entry_id'],42)
                self.assertIsNone(run.call_args.kwargs['state'])

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
