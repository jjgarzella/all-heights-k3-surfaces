import sys,json
from pathlib import Path
import numpy as np
from check_examples import parse,comps
from check_heights import quartic_power
p=7
snapshot=json.loads(Path(__file__).with_name('original_f7_rows.json').read_text())
f={tuple(e):c for e,c in snapshot['7']}
d=4*(p-1); g=quartic_power(f,p-1,p); mons=list(comps(d))
power=quartic_power(f,p*(p-1),p*p)
for m in mons:
    c=int(g[m[:3]])
    power[p*m[0],p*m[1],p*m[2]]-=pow(c,p,p*p)
power%=p*p
assert not np.any(power%p)
delta=power//p
idx=np.indices((d+1,)*3); outside=idx.sum(axis=0)>d
trace=[]
for h in range(1,11):
    trace.append(int(g[(p-1,)*3]))
    if trace[-1]:break
    dest=np.zeros_like(g)
    for alpha in mons:
        c=g[alpha[:3]]
        if not c:continue
        r=[(p-1-a)%p for a in alpha[:3]]
        shift=[(r[j]+alpha[j]-p+1)//p for j in range(3)]
        shape=[min(d+1-s,(delta.shape[j]-1-r[j])//p+1) for j,s in enumerate(shift)]
        src=tuple(slice(r[j],r[j]+p*shape[j],p) for j in range(3))
        dst=tuple(slice(shift[j],shift[j]+shape[j]) for j in range(3))
        dest[dst]+=c*delta[src]
    dest[outside]=0
    g=dest%p
print(json.dumps(dict(p=p,claimed=7,computed=h,trace=trace,method='direct residue-slice multiply then split; no matrix')))
