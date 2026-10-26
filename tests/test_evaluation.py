import unittest
from tests.helpers import snapshot


class EvaluationTests(unittest.TestCase):
    def test_short_history_does_not_claim_backtest_success(self):
        from fpl_planner.evaluation import evaluate
        result=evaluate(snapshot(),{})
        self.assertEqual(result['observations'],0)
        self.assertIn('not a decision backtest',result['caveat'])

    def test_evaluation_uses_past_rows_only(self):
        from fpl_planner.evaluation import evaluate
        s=snapshot();row=s['histories']['1'][0]
        s['completed']=[1,2,3,4]
        s['events']=[{'id':i,'finished':True,'data_checked':True} for i in range(1,5)]
        s['histories']['1']=[dict(row,round=i,total_points=5) for i in range(1,5)]
        s['fixtures']=[dict(id=i,event=i,team_h=1,team_a=2,finished=True,team_h_score=1,team_a_score=0) for i in range(1,5)]
        result=evaluate(s,{})
        self.assertEqual(result['observations'],1)
        self.assertEqual(result['baseline_mae'],0)
