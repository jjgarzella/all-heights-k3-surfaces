import re, math, json, time
from pathlib import Path
import numpy as np

def comps(d,n=4):
    if n==1:
        yield (d,); return
    for a in range(d+1):
        for tail in comps(d-a,n-1): yield (a,)+tail

def parse():
    s=(Path(__file__).resolve().parent.parent / 'heights.tex').read_text()
    out=[]
    for p, table in zip([5,7,11,13],s.split(r'\begin{tabular}')[1:]):
        for m in re.finditer(r'(?m)^\s*(\\\(\\infty\\\)|\d+)\s*&\s*(?:\\\(|\$)(.*?)(?:\\\)|\$)\s*\\\\',table,re.S):
            h='infinity' if 'infty' in m[1] else int(m[1])
            f={}
            for t in m[2].split('+'):
                t=re.sub(r'\s+|[{}]','',t)
                c=re.match(r'^\d+',t)
                c=int(c[0]) if c else 1
                e=[0]*4
                for x,k in re.findall(r'x_(\d)(?:\^(\d+))?',t): e[int(x)-1]=int(k or 1)
                assert sum(e)==4,(p,h,t)
                assert tuple(e) not in f
                f[tuple(e)]=c
            out.append((p,h,f))
    assert len(out)==33,len(out)
    return out

def rank(A,p):
    A=A.copy()%p
    r=0
    for j in range(A.shape[1]):
        nz=np.flatnonzero(A[r:,j])
        if not len(nz): continue
        k=r+int(nz[0]); A[[r,k]]=A[[k,r]]
        A[r]=A[r]*pow(int(A[r,j]),-1,p)%p
        if r+1<len(A): A[r+1:] = (A[r+1:]-A[r+1:,j,None]*A[r])%p
        r+=1
        if r==len(A): break
    return r

def smooth(f,p):
    # Rank 220 proves all degree-9 monomials lie in the Jacobian ideal.
    mons=list(comps(9)); idx={m:i for i,m in enumerate(mons)}
    rows=[]
    for j in range(4):
        df={tuple(e[k]-(k==j) for k in range(4)): c*e[j]%p for e,c in f.items() if e[j]}
        for e in comps(6):
            row=np.zeros(len(mons),dtype=np.int64)
            for a,c in df.items(): row[idx[tuple(e[k]+a[k] for k in range(4))]]=c
            rows.append(row)
    return rank(np.array(rows),p)

def hasse(f,p):
    g={(0,0,0,0):1}
    for _ in range(p-1):
        new={}
        for a,c in g.items():
            for b,d in f.items():
                e=tuple(a[i]+b[i] for i in range(4))
                if max(e)<p: new[e]=(new.get(e,0)+c*d)%p
        g={e:c for e,c in new.items() if c}
    return g.get((p-1,)*4,0)

if __name__=='__main__':
    for p,h,f in parse():
        r=smooth(f,p); a=hasse(f,p)
        print(json.dumps(dict(p=p,height=h,terms=len(f),jacobian_degree9_rank=r,hasse=a,expected_ordinary=(h==1))),flush=True)
