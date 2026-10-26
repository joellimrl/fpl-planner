import base64
import unittest
from unittest.mock import patch
from tests.helpers import league


class DataStateTests(unittest.TestCase):
    def test_completed_requires_both_flags(self):
        from fpl_planner.data import completed_events
        self.assertEqual(completed_events({'events':[{'id':1,'finished':True,'data_checked':True},
            {'id':2,'finished':True,'data_checked':False}]}),[1])

    def test_private_state_is_validated_without_echo(self):
        from fpl_planner.state import validate_state
        players,state=league()
        self.assertEqual(validate_state(state,players,9)['bank'],10)
        state['bank']=-1234567
        with self.assertRaisesRegex(ValueError,'Invalid squad state') as err:
            validate_state(state,players,9)
        self.assertNotIn('1234567',str(err.exception))

    def test_stale_state_rejected_and_duplicates_rejected(self):
        from fpl_planner.state import validate_state
        players,state=league()
        with self.assertRaisesRegex(ValueError,'stale'):
            validate_state(state,players,10)
        state['squad'][0]=state['squad'][1]
        with self.assertRaises(ValueError):validate_state(state,players,9)

    def test_cipher_is_authenticated_and_does_not_contain_plaintext(self):
        from fpl_planner.privacy import seal,unseal,fingerprint
        key=base64.urlsafe_b64encode(bytes(range(32))).decode()
        report={'bank':1234567,'private_marker':'do-not-publish'}
        encrypted=seal(report,key)
        self.assertNotIn(b'do-not-publish',encrypted)
        self.assertEqual(unseal(encrypted,key),report)
        self.assertEqual(fingerprint(report,key),fingerprint(report,key))
        damaged=encrypted[:-1]+bytes([encrypted[-1]^1])
        with self.assertRaises(Exception):unseal(damaged,key)

    def test_collection_excludes_unfinished_rows_and_fails_atomically(self):
        from fpl_planner.data import collect
        boot={'events':[{'id':1,'finished':True,'data_checked':True}],
              'elements':[{'id':1}], 'teams':[]}
        class Client:
            def get(self,path):
                return [] if path=='fixtures/' else {'history':[{'round':1},{'round':2}]}
        self.assertEqual(collect(Client(),boot)['histories']['1'],[{'round':1}])
        class Broken:
            def get(self,path):raise RuntimeError('network')
        with self.assertRaises(RuntimeError):collect(Broken(),boot)

    def test_duplicate_fixture_rejected(self):
        from fpl_planner.data import collect
        boot={'events':[],'elements':[],'teams':[]}
        class Client:
            def get(self,path):return [{'id':7},{'id':7}]
        with self.assertRaises(ValueError):collect(Client(),boot)


if __name__=='__main__':unittest.main()
