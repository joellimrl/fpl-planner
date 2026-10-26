def league():
    players=[]
    for pos,count in [(1,3),(2,7),(3,7),(4,5)]:
        for n in range(count):
            pid=len(players)+1
            players.append(dict(id=pid,name=f'Player {pid}',position=pos,team=(pid-1)%8+1,
                                price=50,forecasts={9:3.0,10:3.0,11:3.0}))
    squad=[]
    for pos,count in [(1,2),(2,5),(3,5),(4,3)]:
        squad.extend(dict(element=p['id'],purchase_price=50,selling_price=50)
                     for p in [p for p in players if p['position']==pos][:count])
    return players,dict(effective_gameweek=9,bank=10,free_transfers=1,squad=squad)


def snapshot():
    return dict(collected_at='2026-10-26T00:00:00Z',completed=[1,2],events=[dict(id=1,finished=True,data_checked=True),
                  dict(id=2,finished=True,data_checked=True),dict(id=9,finished=False,data_checked=False)],
                players=[dict(id=1,web_name='Sample',element_type=3,team=1,now_cost=50,
                              status='a',chance_of_playing_next_round=None)],
                teams=[dict(id=1,name='Home'),dict(id=2,name='Away')],
                fixtures=[dict(id=1,event=9,team_h=1,team_a=2,finished=False)],
                histories={'1':[dict(round=1,minutes=90,starts=1,expected_goals='0.5',expected_assists='0.2',
                   total_points=5,goals_scored=0,assists=1,clean_sheets=0,goals_conceded=1,
                   saves=0,penalties_saved=0,penalties_missed=0,own_goals=0,bonus=0,
                   yellow_cards=0,red_cards=0,defensive_contribution=12)]})
