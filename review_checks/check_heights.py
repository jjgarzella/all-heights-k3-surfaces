import sys,time,json
import numpy as np
from check_examples import parse,comps

def quartic_power(f,k,mod):
    g=np.ones((1,1,1),dtype=np.int32)
    for j in range(k):
        n=g.shape[0]
        a=np.zeros((n+4,)*3,dtype=np.int32)
        for e,c in f.items():
            a[e[0]:e[0]+n,e[1]:e[1]+n,e[2]:e[2]+n]+=c*g
        g=a%mod
    return g

def height(f,p):
    d=4*(p-1); D=p*d
    mons=np.array(list(comps(d)),dtype=np.int64)
    g=quartic_power(f,p-1,p)
    v=g[mons[:,0],mons[:,1],mons[:,2]].astype(np.int64)
    i=np.flatnonzero(np.all(mons==p-1,axis=1))[0]
    trace=[int(v[i])]
    if v[i]: return 1,trace
    # The lift f^(p-1) and the canonical coefficient lift of g have
    # the same p-th power modulo p^2. This lets us multiply by the
    # sparse quartic throughout, avoiding NTTs and floating-point arithmetic.
    power=quartic_power(f,p*(p-1),p*p)
    for m,c in zip(mons,v):
        if c: power[p*m[0],p*m[1],p*m[2]]-=pow(int(c),p,p*p)
    power%=p*p
    assert np.all(power%p==0)
    delta=power//p
    M=np.zeros((len(mons),len(mons)),dtype=np.int64)
    for r,b in enumerate(mons):
        e=p*b+p-1-mons
        ok=np.all(e>=0,axis=1)
        M[r,ok]=delta[e[ok,0],e[ok,1],e[ok,2]]
    for h in range(2,11):
        v=(M@v)%p; trace.append(int(v[i]))
        if v[i]: return h,trace
    return 'infinity',trace

if __name__=='__main__':
    for p,h,f in parse():
        if p not in [int(s) for s in sys.argv[1:]]:continue
        start=time.time();got,tr=height(f,p)
        print(json.dumps(dict(p=p,claimed=h,computed=got,trace=tr,seconds=round(time.time()-start,2))),flush=True)
