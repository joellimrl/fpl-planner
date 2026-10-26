import copy
import unittest
from tests.helpers import snapshot


class ForecastTests(unittest.TestCase):
    def test_component_sum_and_repeatability(self):
        from fpl_planner.forecast import project
        s=snapshot();a=project(s,{'horizon':1})
        self.assertEqual(a,project(s,{'horizon':1}))
        self.assertAlmostEqual(a[0]['forecasts'][9],sum(a[0]['components'][9].values()),6)
        self.assertEqual(a[0]['price'],50)

    def test_blank_double_and_future_leakage(self):
        from fpl_planner.forecast import project
        s=snapshot();one=project(s,{'horizon':1})[0]['forecasts'][9]
        s['histories']['1'].append(dict(s['histories']['1'][0],round=9,expected_goals=9999))
        self.assertEqual(one,project(s,{'horizon':1})[0]['forecasts'][9])
        s['fixtures'].append(dict(s['fixtures'][0],id=2))
        self.assertAlmostEqual(project(s,{'horizon':1})[0]['forecasts'][9],2*one,delta=0.000002)
        s['fixtures']=[]
        self.assertEqual(project(s,{'horizon':1})[0]['forecasts'][9],0)

    def test_unavailable_and_short_appearance(self):
        from fpl_planner.forecast import project
        s=snapshot();full=project(s,{'horizon':1})[0]
        s['histories']['1'][0]['minutes']=45
        short=project(s,{'horizon':1})[0]
        self.assertGreater(full['components'][9]['appearance'],short['components'][9]['appearance'])
        s['players'][0]['status']='i';s['players'][0]['chance_of_playing_next_round']=0
        self.assertEqual(project(s,{'horizon':1})[0]['forecasts'][9],0)

    def test_empty_history_is_finite_and_low(self):
        from fpl_planner.forecast import project
        s=snapshot();s['histories']['1']=[]
        result=project(s,{'horizon':1})[0]
        self.assertTrue(0<=result['forecasts'][9]<4)

    def test_threshold_is_probability_not_average(self):
        from fpl_planner.forecast import project
        s=snapshot();s['histories']['1'][0]['defensive_contribution']=11
        below=project(s,{'horizon':1})[0]['components'][9]['defensive']
        s['histories']['1'][0]['defensive_contribution']=12
        above=project(s,{'horizon':1})[0]['components'][9]['defensive']
        self.assertGreater(above,below)


if __name__=='__main__':unittest.main()
