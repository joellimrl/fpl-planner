"""Six-week MILP. Explicit limits and bounds accompany every recommendation."""
import math
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_array
from .state import validate_state


def transfer_accounting(free, transfers):
    if type(free) is not int or type(transfers) is not int or not 0<=free<=5 or transfers<0:
        raise ValueError('Invalid transfer counts')
    return 4*max(0,transfers-free),min(5,max(0,free-transfers)+1)


class Model:
    def __init__(self):
        self.cost=[];self.lo=[];self.hi=[];self.integer=[]
        self.rows=[];self.cols=[];self.values=[];self.lower=[];self.upper=[]

    def var(self,lo=0,hi=1,cost=0,integer=1):
        i=len(self.cost);self.cost.append(cost);self.lo.append(lo);self.hi.append(hi);self.integer.append(integer)
        return i

    def constraint(self,terms,lo=-np.inf,hi=np.inf):
        index=len(self.lower)
        for col,value in terms.items():
            if value:self.rows.append(index);self.cols.append(col);self.values.append(value)
        self.lower.append(lo);self.upper.append(hi)

    def eq(self,terms,value=0):self.constraint(terms,value,value)

    def run(self,config):
        shape=(len(self.lower),len(self.cost))
        matrix=coo_array((np.asarray(self.values,dtype=float),
            (np.asarray(self.rows,dtype=np.int32),np.asarray(self.cols,dtype=np.int32))),shape=shape).tocsc()
        return milp(np.asarray(self.cost),integrality=np.asarray(self.integer),
                    bounds=Bounds(self.lo,self.hi),constraints=LinearConstraint(matrix,self.lower,self.upper),
                    options=dict(time_limit=config.get('time_limit',90),node_limit=config.get('node_limit',3000),
                                 mip_rel_gap=config.get('mip_rel_gap',0.0001),presolve=True))


def solve(players,state,events,config,hold_now=False):
    if not events or len(events)>6 or events!=sorted(set(events)):
        raise ValueError('Invalid planning events')
    players=sorted(players,key=lambda p:p['id'])
    state=validate_state(state,players,events[0])
    initial={p['element']:p for p in state['squad']}
    players=[p for p in players if p.get('selectable',True) or p['id'] in initial]
    for p in players:
        if type(p['price']) is not int or not 1<=p['price']<=1000:
            raise ValueError('Invalid projection price')
        if any(not math.isfinite(p['forecasts'][e]) for e in events):
            raise ValueError('Nonfinite projection')
    cap=config.get('max_transfers',2)
    if type(cap) is not int or not 0<=cap<=2:raise ValueError('Invalid transfer cap')
    m=Model();h=len(events);n=len(players)
    free=[m.var(lo=state['free_transfers'],hi=state['free_transfers'])]+[m.var(lo=1,hi=5) for _ in events]
    weeks=[];prior=None
    for w,e in enumerate(events):
        v={name:[m.var(cost=-p['forecasts'][e] if name in ('lineup','captain') else 0,
                      hi=0 if name=='buy' and not p.get('selectable',True) else 1)
                 for p in players] for name in ('owned','buy','sell','lineup','captain')}
        v['original']={i:m.var() for i,p in enumerate(players) if p['id'] in initial}
        v['original_sale']={i:m.var() for i in v['original']}
        v['bank']=m.var(hi=15000)
        v['transfers']=m.var(hi=0 if hold_now and w==0 else cap)
        v['used']=m.var(hi=5);v['hits']=m.var(hi=cap,cost=4)
        min_switch=m.var();cap_switch=m.var()
        for i,p in enumerate(players):
            x,b,s,l,c=[v[k][i] for k in ('owned','buy','sell','lineup','captain')]
            owner=int(p['id'] in initial)
            ownership={x:1,b:-1,s:1}
            if prior:ownership[prior['owned'][i]]=-1
            m.eq(ownership,owner if prior is None else 0)
            m.constraint({b:1,s:1},hi=1)
            m.constraint({l:1,x:-1},hi=0);m.constraint({c:1,l:-1},hi=0)
            if owner:
                o,os=v['original'][i],v['original_sale'][i]
                terms={o:1,os:1}
                if prior:terms[prior['original'][i]]=-1
                m.eq(terms,1 if prior is None else 0)
                m.constraint({os:1,s:-1},hi=0)
                if prior:
                    op=prior['original'][i]
                    m.constraint({os:1,op:-1},hi=0)
                    m.constraint({os:1,op:-1,s:-1},lo=-1)
                else:m.eq({os:1,s:-1})
        m.eq({i:1 for i in v['owned']},15)
        m.eq({i:1 for i in v['lineup']},11)
        m.eq({i:1 for i in v['captain']},1)
        for pos,slots,low,high in [(1,2,1,1),(2,5,3,5),(3,5,2,5),(4,3,1,3)]:
            indices=[i for i,p in enumerate(players) if p['position']==pos]
            m.eq({v['owned'][i]:1 for i in indices},slots)
            m.constraint({v['lineup'][i]:1 for i in indices},low,high)
        for team in sorted({p['team'] for p in players}):
            m.constraint({v['owned'][i]:1 for i,p in enumerate(players) if p['team']==team},hi=3)
        money={v['bank']:1}
        if prior:money[prior['bank']]=-1
        for i,p in enumerate(players):
            money[v['buy'][i]]=p['price'];money[v['sell'][i]]=-p['price']
            if i in v['original_sale']:
                money[v['original_sale'][i]]=p['price']-initial[p['id']]['selling_price']
        m.eq(money,state['bank'] if prior is None else 0)
        m.eq({v['transfers']:1,**{i:-1 for i in v['buy']}})
        m.eq({v['transfers']:1,**{i:-1 for i in v['sell']}})
        t,u,f=v['transfers'],v['used'],free[w]
        m.constraint({u:1,t:-1},hi=0);m.constraint({u:1,f:-1},hi=0)
        m.constraint({u:1,t:-1,min_switch:20},lo=0)
        m.constraint({u:1,f:-1,min_switch:-20},lo=-20)
        m.eq({v['hits']:1,t:-1,u:1})
        nf=free[w+1]
        m.constraint({nf:1,f:-1,u:1},hi=1)
        m.constraint({nf:1,f:-1,u:1,cap_switch:20},lo=1)
        m.constraint({nf:1,cap_switch:-20},lo=-15)
        weeks.append(v);prior=v
    res=m.run(config)
    if res.x is None or res.status not in (0,1):
        raise RuntimeError('Optimiser found no feasible plan within its limits')
    # Check bounds/integrality here. HiGHS enforces the sparse linear constraints.
    x=res.x
    for i in range(len(x)):
        if x[i]<m.lo[i]-1e-5 or x[i]>m.hi[i]+1e-5 or abs(x[i]-round(x[i]))>1e-5:
            raise RuntimeError('Invalid optimiser incumbent')
    output=[]
    for w,(e,v) in enumerate(zip(events,weeks)):
        def selected(k):return [p['id'] for i,p in enumerate(players) if x[v[k][i]]>0.5]
        lineup=selected('lineup');captain=selected('captain')[0]
        score=sum(p['forecasts'][e] for p in players if p['id'] in lineup)+next(p['forecasts'][e] for p in players if p['id']==captain)
        bench=sorted([p for p in players if p['id'] in selected('owned') and p['id'] not in lineup],
                     key=lambda p:(p['position']==1,-p['forecasts'][e],p['id']))
        vice=max((p for p in players if p['id'] in lineup and p['id']!=captain),key=lambda p:(p['forecasts'][e],-p['id']))['id']
        output.append(dict(event=e,squad=selected('owned'),starters=lineup,captain=captain,vice_captain=vice,
                           bench=[p['id'] for p in bench],buys=selected('buy'),sells=selected('sell'),
                           bank=round(x[v['bank']]),free_transfers=round(x[free[w]]),
                           next_free_transfers=round(x[free[w+1]]),hit=4*round(x[v['hits']]),
                           scoring_points=round(score,4)))
    bound=getattr(res,'mip_dual_bound',None)
    return dict(weeks=output,objective=round(-float(res.fun),4),
                upper_bound=round(-float(bound),4) if bound is not None and math.isfinite(bound) else None,
                gap=float(res.mip_gap) if getattr(res,'mip_gap',None) is not None else None,
                status='optimal_within_tolerance' if res.status==0 else 'limit_reached',
                nodes=int(getattr(res,'mip_node_count',0) or 0),hold_now=hold_now)


def compare(players,state,events,config):
    hold=solve(players,state,events,config,hold_now=True)
    best=solve(players,state,events,config)
    if best['objective']<hold['objective']:best=hold
    lower=best['objective']-hold['upper_bound'] if hold['upper_bound'] is not None else None
    upper=best['upper_bound']-hold['objective'] if best['upper_bound'] is not None else None
    return dict(best=best,hold=hold,gain=round(best['objective']-hold['objective'],4),
                gain_interval=[round(lower,4) if lower is not None else None,
                               round(upper,4) if upper is not None else None])
