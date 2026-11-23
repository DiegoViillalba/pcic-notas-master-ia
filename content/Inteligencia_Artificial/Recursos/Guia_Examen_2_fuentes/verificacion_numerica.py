"""Verificación numérica de todos los ejercicios de la Guía del Examen 2 (IA)."""
import itertools, math
import numpy as np

def hdr(s): print("\n" + "=" * 8, s, "=" * 8)
def sig(z): return 1 / (1 + math.exp(-z))

# ---------------- utilidades de redes bayesianas booleanas ----------------
class BN:
    def __init__(self, order, parents, cpt):
        self.order, self.parents, self.cpt = order, parents, cpt  # cpt[X][tuple parents] = P(X=True|...)
    def p(self, X, val, asg):
        pt = self.cpt[X][tuple(asg[u] for u in self.parents[X])]
        return pt if val else 1 - pt
    def joint(self, asg):
        r = 1.0
        for X in self.order: r *= self.p(X, asg[X], asg)
        return r
    def query(self, Q, ev):
        hidden = [v for v in self.order if v != Q and v not in ev]
        w = {}
        for q in (True, False):
            s = 0.0
            for vals in itertools.product((True, False), repeat=len(hidden)):
                a = dict(ev); a[Q] = q; a.update(zip(hidden, vals))
                s += self.joint(a)
            w[q] = s
        Z = w[True] + w[False]
        return w[True] / Z, w, Z
    def prob(self, ev):
        hidden = [v for v in self.order if v not in ev]
        s = 0
        for vals in itertools.product((True, False), repeat=len(hidden)):
            a = dict(ev); a.update(zip(hidden, vals)); s += self.joint(a)
        return s

# ---------------- B1 ----------------
hdr("B1 conjunta L,T,P")
J = {}
for l, t, p in itertools.product((1, 0), repeat=3):
    pl = 0.3 if l else 0.7
    pt = (0.8 if t else 0.2) if l else (0.2 if t else 0.8)
    pp = (0.9 if p else 0.1) if l else (0.1 if p else 0.9)
    J[(l, t, p)] = pl * pt * pp
for k, v in J.items(): print(k, round(v, 4))
Pt = sum(v for k, v in J.items() if k[1]); Pp = sum(v for k, v in J.items() if k[2])
Ptp = sum(v for k, v in J.items() if k[1] and k[2])
print("P(t)", Pt, "P(p)", Pp, "P(t,p)", Ptp, "P(t)P(p)", Pt * Pp)
print("P(t|p)", Ptp / Pp, "P(l|t,p)", J[(1, 1, 1)] / Ptp, "P(l|t)", (J[(1,1,1)]+J[(1,1,0)]) / Pt)
for l in (1, 0):
    Pl = sum(v for k, v in J.items() if k[0] == l)
    ptp = J[(l, 1, 1)] / Pl
    pt_ = sum(v for k, v in J.items() if k[0] == l and k[1]) / Pl
    pp_ = sum(v for k, v in J.items() if k[0] == l and k[2]) / Pl
    print("l=", l, "P(t,p|l)", ptp, "P(t|l)P(p|l)", pt_ * pp_)

# ---------------- B2 ----------------
hdr("B2 Bayes")
prev, sens, fpr = 0.02, 0.95, 0.08
num = prev * sens; den = num + (1 - prev) * fpr
print("P(E|+)", num, den, num / den)
num2 = prev * sens**2; den2 = num2 + (1 - prev) * fpr**2
print("P(E|++)", num2, den2, num2 / den2)
num3 = prev * sens * (1 - sens); den3 = num3 + (1 - prev) * fpr * (1 - fpr)
print("P(E|+-)", num3, den3, num3 / den3)
# secuencial: prior posterior
p1 = num / den
print("secuencial ++", p1 * sens / (p1 * sens + (1 - p1) * fpr))

# ---------------- B3 ----------------
hdr("B3 parámetros")
dom = dict(A=2, B=3, C=2, D=4, E=2, F=3)
par = dict(A=[], B=[], C=["A", "B"], D=["C"], E=["C"], F=["E"])
tot = 0
for X in "ABCDEF":
    k = (dom[X] - 1) * math.prod(dom[u] for u in par[X]); tot += k; print(X, k)
print("total", tot, "conjunta", math.prod(dom.values()) - 1)

# ---------------- Red del estudiante (B4, B8, C2) ----------------
hdr("Estudiante")
est = BN(["D", "I", "C", "E", "R"],
         dict(D=[], I=[], C=["D", "I"], E=["I"], R=["C"]),
         dict(D={(): 0.4}, I={(): 0.3},
              C={(True, True): 0.7, (True, False): 0.1, (False, True): 0.9, (False, False): 0.4},
              E={(True,): 0.8, (False,): 0.1}, R={(True,): 0.9, (False,): 0.2}))
w = dict(D=False, I=True, C=True, E=False, R=True)
print("P(-d,+i,+c,-e,+r)", est.joint(w))
print("P(+c)", est.prob(dict(C=True)))
print("P(+r)", est.prob(dict(R=True)))
print("P(+i|+r)", est.query("I", dict(R=True)))
print("P(+i|+r,+e)", est.query("I", dict(R=True, E=True)))
print("P(+i|+c)", est.query("I", dict(C=True)))
print("P(+i|+c,+d)", est.query("I", dict(C=True, D=True)))
print("P(+i|+c,-d)", est.query("I", dict(C=True, D=False)))
print("P(+i|-c)", est.query("I", dict(C=False)))
# VE B8: f1(C,I)=sum_d P(d)P(C|d,I)
for i in (True, False):
    for c in (True, False):
        f1 = sum((0.4 if d else 0.6) * est.p("C", c, dict(D=d, I=i)) for d in (True, False))
        print("f1(c=%s,i=%s)=%.4f" % (c, i, f1))
for i in (True, False):
    f2 = sum(sum((0.4 if d else 0.6) * est.p("C", c, dict(D=d, I=i)) for d in (True, False)) * (0.9 if c else 0.2) for c in (True, False))
    print("f2(i=%s)=%.4f  P(i)f2=%.5f" % (i, f2, (0.3 if i else 0.7) * f2))
# C2 VE con +e: f3(I)=P(+e|I)
for i in (True, False):
    f2 = sum(sum((0.4 if d else 0.6) * est.p("C", c, dict(D=d, I=i)) for d in (True, False)) * (0.9 if c else 0.2) for c in (True, False))
    pe = 0.8 if i else 0.1
    print("i=%s: P(i)*P(+e|i)*f2 = %.6f" % (i, (0.3 if i else 0.7) * pe * f2))
# enumeración: los 4 mundos por valor de I
for i in (True, False):
    for d in (True, False):
        for c in (True, False):
            a = dict(D=d, I=i, C=c, E=True, R=True)
            print("  mundo i=%s d=%s c=%s: %.6f" % (i, d, c, est.joint(a)))

# ---------------- B5 d-separación ----------------
hdr("B5 d-sep")
edges = [("A","C"),("B","C"),("B","D"),("C","E"),("D","F"),("E","G"),("F","G"),("G","H")]
nodes = sorted(set(sum(edges, ())))
pa = {n: [a for a, b in edges if b == n] for n in nodes}
ch = {n: [b for a, b in edges if a == n] for n in nodes}
def anc(S):
    out = set(S); st = list(S)
    while st:
        n = st.pop()
        for p_ in pa[n]:
            if p_ not in out: out.add(p_); st.append(p_)
    return out
def dsep(X, Y, Z):
    # moral ancestral graph
    A = anc({X, Y} | set(Z))
    adj = {n: set() for n in A}
    for n in A:
        for p_ in pa[n]:
            adj[n].add(p_); adj[p_].add(n)
        for p1, p2 in itertools.combinations(pa[n], 2):
            adj[p1].add(p2); adj[p2].add(p1)
    seen = {X}; st = [X]
    while st:
        n = st.pop()
        for m in adj[n]:
            if m in Z or m in seen: continue
            if m == Y: return False
            seen.add(m); st.append(m)
    return True
qs = [("A","B",[]),("A","B",["H"]),("A","D",[]),("A","D",["G"]),("A","D",["G","B"]),
      ("C","F",["B"]),("E","F",["G","D"]),("A","H",["E"]),("A","F",["C"]),("B","G",["E","F"])]
for X, Y, Z in qs: print(X, Y, Z, "indep" if dsep(X, Y, Z) else "NO garantizada")
for n in nodes:
    mb = set(pa[n]) | set(ch[n]) | {p_ for c in ch[n] for p_ in pa[c]}
    mb.discard(n); print("MB", n, sorted(mb))

# ---------------- B6 alarma ----------------
hdr("B6 alarma")
al = BN(["B","E","A","J","M"], dict(B=[],E=[],A=["B","E"],J=["A"],M=["A"]),
        dict(B={():0.001},E={():0.002},A={(True,True):0.95,(True,False):0.94,(False,True):0.29,(False,False):0.001},
             J={(True,):0.9,(False,):0.05},M={(True,):0.7,(False,):0.01}))
print("P(+a)", al.prob(dict(A=True)))
print("P(+b|+a)", al.query("B", dict(A=True)))
print("P(+e|+a)", al.query("E", dict(A=True)))
print("P(+e|+a,+b)", al.query("E", dict(A=True, B=True)))
print("P(+e|+a,-b)", al.query("E", dict(A=True, B=False)))
for b,e in itertools.product((True,False),repeat=2):
    print("  P(b=%s,e=%s,+a)=%.9f"%(b,e,al.joint(dict(B=b,E=e,A=True,J=True,M=True))/(0.9*0.7)))

# ---------------- B7 cadena ----------------
hdr("B7 cadena R->T->L")
ch_ = BN(["R","T","L"], dict(R=[],T=["R"],L=["T"]),
         dict(R={():0.1},T={(True,):0.8,(False,):0.1},L={(True,):0.3,(False,):0.1}))
print("P(+l)", ch_.prob(dict(L=True)))
print("P(R|+l)", ch_.query("R", dict(L=True)))
print("P(T|+l)", ch_.query("T", dict(L=True)))
print("P(L|+r)", ch_.query("L", dict(R=True)))

# ---------------- B9 orden de eliminación (alcances) ----------------
hdr("B9 orden de eliminación")
# red: A->C, B->C, C->D, C->E, D->F, E->F ; consulta P(A|+f)
fac0 = [{"A"},{"B"},{"A","B","C"},{"C","D"},{"C","E"},{"D","E"}]  # P(+f|D,E) ya restringido
def simulate(order):
    fs = [set(f) for f in fac0]; out = []
    for X in order:
        inv = [f for f in fs if X in f]; rest = [f for f in fs if X not in f]
        prod = set().union(*inv); new = prod - {X}
        out.append((X, sorted(prod), sorted(new))); fs = rest + [new]
    return out, fs
for order in (["B","D","E","C"], ["C","B","D","E"], ["D","E","C","B"]):
    o, fs = simulate(order); print(order); [print("   ", r) for r in o]

# ---------------- Red aspersor (B10-B12) ----------------
hdr("Aspersor")
asp = BN(["C","S","R","W"], dict(C=[],S=["C"],R=["C"],W=["S","R"]),
         dict(C={():0.5},S={(True,):0.1,(False,):0.5},R={(True,):0.8,(False,):0.2},
              W={(True,True):0.99,(True,False):0.90,(False,True):0.90,(False,False):0.01}))
print("P(+w)", asp.prob(dict(W=True)))
print("P(+c|+w)", asp.query("C", dict(W=True)))
print("P(+c|+s,+w)", asp.query("C", dict(S=True, W=True)))
print("P(+r|+s,+w)", asp.query("R", dict(S=True, W=True)))
U = [0.31,0.62,0.12,0.45,  0.77,0.08,0.91,0.50,  0.18,0.35,0.66,0.97,  0.52,0.44,0.15,0.03,  0.05,0.06,0.70,0.88]
samples = []
for k in range(5):
    u = U[4*k:4*k+4]; a = {}
    a["C"] = u[0] < 0.5
    a["S"] = u[1] < asp.cpt["S"][(a["C"],)]
    a["R"] = u[2] < asp.cpt["R"][(a["C"],)]
    a["W"] = u[3] < asp.cpt["W"][(a["S"], a["R"])]
    samples.append(a); print("muestra", k+1, u, {k_: ("+" if v else "-") for k_, v in a.items()})
nw = sum(s["W"] for s in samples); ncw = sum(s["W"] and s["C"] for s in samples)
print("P^(+w)=", nw, "/5 ; P^(+c|+w)=", ncw, "/", nw)
# LW evidencia +s,+w : se sortean C y R
UL = [(0.21,0.40),(0.64,0.10),(0.47,0.93),(0.88,0.75),(0.12,0.85)]
num = den = 0
for k, (uc, ur) in enumerate(UL):
    c = uc < 0.5; r = ur < (0.8 if c else 0.2)
    wgt = (0.1 if c else 0.5) * (0.99 if r else 0.90)
    print("LW", k+1, "c", c, "r", r, "w", wgt); den += wgt; num += wgt * c
print("LW P^(+c|+s,+w)=", num, "/", den, "=", num/den)
# Gibbs evidencia +w ; estado inicial (+c,-s,-r) ; orden C,S,R
def gibbs_step(state, var, u):
    vals = {}
    for v in (True, False):
        a = dict(state); a[var] = v
        # manta de Markov: CPT propia * CPT de hijos
        pr = asp.p(var, v, a)
        for ch2 in [x for x in asp.order if var in asp.parents[x]]:
            pr *= asp.p(ch2, a[ch2], a)
        vals[v] = pr
    pt = vals[True] / (vals[True] + vals[False])
    state[var] = u < pt
    return pt, vals
st = dict(C=True, S=False, R=False, W=True)
UG = [0.60, 0.20, 0.30, 0.90, 0.55, 0.40]
i = 0
for sweep in range(2):
    for var in ("C","S","R"):
        pt, vals = gibbs_step(st, var, UG[i]); print("Gibbs", var, "u=", UG[i], "w", {k: round(v,5) for k, v in vals.items()}, "P(+)=%.4f" % pt, "->", st); i += 1

# ---------------- B13 MLE / Laplace ----------------
hdr("B13 MLE Laplace")
data = [("S","L",1),("S","L",1),("S","F",1),("S","L",0),("N","L",1),("N","F",0),
        ("N","L",0),("Ll","L",0),("Ll","L",0),("S","F",1),("N","F",1),("Ll","L",1)]
from collections import Counter
cc = Counter(d[0] for d in data); print("Clima", cc)
cd = Counter(d[1] for d in data); print("Dia", cd)
for cl in ("S","N","Ll"):
    for di in ("L","F"):
        rows = [d for d in data if d[0]==cl and d[1]==di]
        n = len(rows); k = sum(d[2] for d in rows)
        print(cl, di, "N=", n, "bici=", k, "MLE", (k/n if n else None), "Lap", (k+1)/(n+2))
print("Clima Laplace", {c: (cc[c]+1)/(12+3) for c in ("S","N","Ll")})

# ---------------- B14 EM una iteración ----------------
hdr("B14 EM")
def em_iter(pa_, r1a, r1b, r2a, r2b, D):
    ws = []; ll = 0
    for x1, x2 in D:
        la = pa_ * (r1a if x1 else 1-r1a) * (r2a if x2 else 1-r2a)
        lb = (1-pa_) * (r1b if x1 else 1-r1b) * (r2b if x2 else 1-r2b)
        ws.append(la/(la+lb)); ll += math.log(la+lb)
    W = sum(ws); Wb = len(D) - W
    n_pa = W/len(D)
    n_r1a = sum(w_ for w_, (x1, _) in zip(ws, D) if x1)/W
    n_r1b = sum(1-w_ for w_, (x1, _) in zip(ws, D) if x1)/Wb
    n_r2a = sum(w_ for w_, (_, x2) in zip(ws, D) if x2)/W
    n_r2b = sum(1-w_ for w_, (_, x2) in zip(ws, D) if x2)/Wb
    return ws, ll, (n_pa, n_r1a, n_r1b, n_r2a, n_r2b)
D = [(1,1),(1,0),(0,0),(1,1),(0,1)]
th = (0.5, 0.8, 0.3, 0.7, 0.4)
for it in range(3):
    ws, ll, th2 = em_iter(*th, D)
    print("iter", it, "theta", [round(x,4) for x in th], "w_a", [round(x,4) for x in ws], "loglik", round(ll,4), "->", [round(x,4) for x in th2])
    th = th2

# ---------------- B15 regresión ----------------
hdr("B15 regresión")
X = np.array([[1,0],[1,1],[1,2],[1,3]],float); y = np.array([1,3,4,8],float)
print("XtX", X.T@X, "Xty", X.T@y)
th = np.linalg.solve(X.T@X, X.T@y); print("theta", th, "pred", X@th, "SSE", ((y-X@th)**2).sum())
g = 2*X.T@(X@np.zeros(2)-y); th1 = -0.01*g; print("grad0", g, "theta1", th1, "J0", (y**2).sum(), "J1", ((y-X@th1)**2).sum())
g1 = 2*X.T@(X@th1-y); th2 = th1-0.01*g1; print("grad1", g1, "theta2", th2, "J2", ((y-X@th2)**2).sum())

# ---------------- B16 logística ----------------
hdr("B16 logística")
X = np.array([[1,2,1],[1,0,2],[1,1,0]],float); y = np.array([1,0,1],float); th = np.array([0,1,-1],float)
def logi(th):
    z = X@th; p = 1/(1+np.exp(-z)); L = -(y*np.log(p)+(1-y)*np.log(1-p)); return z, p, L
z, p, L = logi(th); print("z", z, "pi", p, "loss_i", L, "J", L.sum())
g = X.T@(p-y); print("grad", g); th1 = th-0.5*g; print("theta1", th1)
z, p, L = logi(th1); print("z1", z, "pi1", p, "J1", L.sum())

# ---------------- B17 softmax ----------------
hdr("B17 softmax")
zz = np.array([2,1,-1],float); e = np.exp(zz); pp = e/e.sum(); print("e", e, "sum", e.sum(), "p", pp, "loss", -math.log(pp[1]), "grad", pp-np.array([0,1,0]))
e2 = np.exp(zz/2); print("tau=2", e2/e2.sum()); e3=np.exp(zz/0.5); print("tau=0.5", e3/e3.sum())

# ---------------- B19 distancias / kNN ----------------
hdr("B19 kNN")
q = np.array([3,3]); P = {"P1":((6,3),"+"),"P2":((5,5),"-"),"P3":((-1,4),"+"),"P4":((1,-1),"-")}
for n,(x,c) in P.items():
    d = np.array(x)-q; print(n, x, c, "L1", abs(d).sum(), "L2", round(float(np.sqrt((d**2).sum())),3), "Linf", abs(d).max())

# ---------------- B20/B21 k-means ----------------
hdr("B20 k-means")
pts = np.array([[1,1],[2,1],[1,3],[5,4],[6,5],[5,6]],float); mu = np.array([[1,1],[1,3]],float)
for it in range(5):
    d2 = ((pts[:,None,:]-mu[None,:,:])**2).sum(-1); asg = d2.argmin(1)
    Jv = d2[np.arange(len(pts)),asg].sum()
    print("it", it, "mu", mu.tolist(), "d2", d2.tolist(), "asg", asg.tolist(), "J(asig)", Jv)
    newmu = np.array([pts[asg==k].mean(0) for k in range(2)])
    Jn = sum(((pts[asg==k]-newmu[k])**2).sum() for k in range(2)); print("   newmu", newmu.tolist(), "J(tras actualizar)", Jn)
    if np.allclose(newmu, mu): break
    mu = newmu
# silueta para P1=(1,1) y P4=(5,4) con grupos finales
def sil(i, asg):
    di = np.sqrt(((pts-pts[i])**2).sum(1))
    own = [j for j in range(len(pts)) if asg[j]==asg[i] and j!=i]
    a = di[own].mean(); b = min(di[[j for j in range(len(pts)) if asg[j]==k]].mean() for k in set(asg) if k!=asg[i])
    return a, b, (b-a)/max(a,b)
for i in range(6): print("sil P%d" % (i+1), [round(float(v),4) for v in sil(i, asg)])
print("dist P3 a otros", np.round(np.sqrt(((pts-pts[2])**2).sum(1)),4))

# ---------------- B22 jerárquico ----------------
hdr("B22 jerárquico")
Dm = {("A","B"):2,("A","C"):6,("A","D"):10,("A","E"):9,("B","C"):5,("B","D"):9,("B","E"):8,("C","D"):4,("C","E"):5,("D","E"):3}
def d(a,b): return Dm.get((a,b), Dm.get((b,a)))
def agglo(link):
    cl = [frozenset(x) for x in "ABCDE"]; hist = []
    while len(cl) > 1:
        best = None
        for c1, c2 in itertools.combinations(cl, 2):
            ds = [d(a,b) for a in c1 for b in c2]
            v = {"single":min(ds),"complete":max(ds),"average":sum(ds)/len(ds)}[link]
            if best is None or v < best[0]: best = (v, c1, c2)
        v, c1, c2 = best; cl = [c for c in cl if c not in (c1,c2)] + [c1|c2]
        hist.append(("".join(sorted(c1)), "".join(sorted(c2)), round(v,4)))
    return hist
for lk in ("single","complete","average"): print(lk, agglo(lk))

# ---------------- B23 retornos MC / TD ----------------
hdr("B23 MC / TD")
g_ = 0.5
eps = [[("A",1),("B",2),("A",-1),("B",4)], [("B",3),("A",1)]]
first = {"A":[], "B":[]}; every = {"A":[], "B":[]}
for ep in eps:
    G = 0; rets = []
    for s, r in reversed(ep):
        G = r + g_*G; rets.append((s, G))
    rets.reverse(); print("retornos", rets)
    seen = set()
    for s, Gt in rets:
        every[s].append(Gt)
        if s not in seen: first[s].append(Gt); seen.add(s)
print("first", first, {k: sum(v)/len(v) for k, v in first.items()})
print("every", every, {k: sum(v)/len(v) for k, v in every.items()})
V = {"A":0.0,"B":0.0,"T":0.0}; al_=0.5
for ep in eps:
    for idx,(s,r) in enumerate(ep):
        nxt = ep[idx+1][0] if idx+1 < len(ep) else "T"
        tgt = r + g_*V[nxt]; V[s] += al_*(tgt-V[s]); print("TD", s, r, nxt, "target", tgt, "->", dict(V))

# ---------------- Corredor (B24, B25, C9) ----------------
hdr("Corredor")
# estados 1,2,3; terminales L (izq de 1) y R (der de 3). entrar L: +2 ; entrar R: +10 ; otro: -1
# acción con prob 0.8 va en la dirección pedida, 0.2 en la opuesta. gamma 0.9
gam = 0.9
def succ(s, a):
    out = []
    for dirn, pr in ((a, 0.8), (-a, 0.2)):
        n = s + dirn
        if n == 0: out.append(("L", pr, 2))
        elif n == 4: out.append(("R", pr, 10))
        else: out.append((n, pr, -1))
    return out
def Q(V, s, a): return sum(pr*(r + gam*(0 if n in ("L","R") else V[n])) for n, pr, r in succ(s, a))
# evaluación política siempre derecha
A_ = np.zeros((3,3)); b_ = np.zeros(3)
for s in (1,2,3):
    A_[s-1,s-1] += 1
    for n, pr, r in succ(s, +1):
        b_[s-1] += pr*r
        if n not in ("L","R"): A_[s-1,n-1] -= gam*pr
Vr = np.linalg.solve(A_, b_); print("V^{derecha}", Vr)
Vd = {1:Vr[0],2:Vr[1],3:Vr[2]}
for s in (1,2,3): print("Q^pi", s, "izq", Q(Vd,s,-1), "der", Q(Vd,s,+1))
V = {1:0,2:0,3:0}
for k in range(1,7):
    Qs = {s:(Q(V,s,-1),Q(V,s,+1)) for s in (1,2,3)}
    V = {s:max(Qs[s]) for s in (1,2,3)}
    print("VI k=%d"%k, {s:(round(Qs[s][0],4),round(Qs[s][1],4)) for s in Qs}, {s:round(v,4) for s,v in V.items()})
for _ in range(500):
    V = {s:max(Q(V,s,-1),Q(V,s,+1)) for s in (1,2,3)}
print("V* aprox", {s:round(v,4) for s,v in V.items()}, {s:("izq" if Q(V,s,-1)>Q(V,s,+1) else "der") for s in V})
# política siempre izquierda evaluación
A_ = np.zeros((3,3)); b_ = np.zeros(3)
for s in (1,2,3):
    A_[s-1,s-1] += 1
    for n, pr, r in succ(s, -1):
        b_[s-1] += pr*r
        if n not in ("L","R"): A_[s-1,n-1] -= gam*pr
print("V^{izquierda}", np.linalg.solve(A_, b_))

# ---------------- B26 Q-learning auto ----------------
hdr("B26 Q-learning auto")
Qt = {(s,a):0.0 for s in ("C","W") for a in ("S","F")}
def mx(s): return 0.0 if s == "O" else max(Qt[(s,"S")], Qt[(s,"F")])
trans = [("C","F",2,"W"),("W","S",1,"C"),("C","F",2,"C"),("C","S",1,"C"),("C","F",2,"W"),("W","F",-10,"O")]
for s,a,r,s2 in trans:
    y_ = r + 0.9*mx(s2); old = Qt[(s,a)]; Qt[(s,a)] = old + 0.5*(y_-old)
    print((s,a,r,s2), "y=%.4f old=%.4f new=%.4f" % (y_, old, Qt[(s,a)]))
print(Qt)

# ---------------- B28 Q lineal ----------------
hdr("B28 Q lineal")
w_ = np.array([1,2,-1],float); phi = np.array([1,1,2],float)
q_sa = w_@phi; qn = [w_@np.array([1,0,1]), w_@np.array([1,2,0])]
y_ = 3+0.9*max(qn); dl = y_-q_sa; w2 = w_+0.1*dl*phi
print("Q(s,a)", q_sa, "next", qn, "y", y_, "delta", dl, "w'", w2, "Q'(s,a)", w2@phi, "Q' next", [w2@np.array([1,0,1]), w2@np.array([1,2,0])])

# ---------------- B29 backprop 2-2-1 ----------------
hdr("B29 backprop")
x = np.array([1,2],float); W1 = np.array([[1,-1],[0.5,0.5]]); b1 = np.array([0,-1.]); w2v = np.array([2,-1.]); b2 = 0.5; yv = 1
def fwd(W1,b1,w2v,b2):
    z1 = W1@x+b1; h = np.maximum(z1,0); z2 = w2v@h+b2; p = sig(z2); L = -math.log(p) if yv==1 else -math.log(1-p)
    return z1,h,z2,p,L
z1,h,z2,p,L = fwd(W1,b1,w2v,b2); print("z1",z1,"h",h,"z2",z2,"p",p,"L",L)
d2 = p-yv; dw2 = d2*h; d1 = w2v*d2*(z1>0); dW1 = np.outer(d1,x)
print("d2",d2,"dw2",dw2,"db2",d2,"d1",d1,"dW1",dW1)
eta=0.5; W1n=W1-eta*dW1; b1n=b1-eta*d1; w2n=w2v-eta*dw2; b2n=b2-eta*d2
print("W1'",W1n,"b1'",b1n,"w2'",w2n,"b2'",b2n, "fwd'", fwd(W1n,b1n,w2n,b2n))

# ---------------- B31 atención ----------------
hdr("B31 atención")
Qm = np.array([[1,0],[0,1],[1,1]],float); Km = np.array([[1,0],[1,1],[0,1]],float); Vm = np.array([[1,0],[0,1],[1,1]],float)
S = Qm@Km.T/math.sqrt(2); print("S", np.round(S,4))
M = np.triu(np.full((3,3),-np.inf),1); Sm = S+M
Aw = np.exp(Sm-Sm.max(1,keepdims=True)); Aw/=Aw.sum(1,keepdims=True); print("A", np.round(Aw,4)); print("O", np.round(Aw@Vm,4))

# ---------------- B32 confusión ----------------
hdr("B32 confusión")
sc = [0.95,0.85,0.80,0.70,0.55,0.45,0.40,0.30,0.20,0.10]; lab=[1,1,0,1,0,1,0,0,1,0]
for th_ in (0.5,0.35,0.75):
    TP=sum(1 for s,l in zip(sc,lab) if s>=th_ and l); FP=sum(1 for s,l in zip(sc,lab) if s>=th_ and not l)
    FN=sum(1 for s,l in zip(sc,lab) if s<th_ and l); TN=sum(1 for s,l in zip(sc,lab) if s<th_ and not l)
    prec=TP/(TP+FP); rec=TP/(TP+FN); print(th_, "TP FP FN TN", TP,FP,FN,TN, "acc",(TP+TN)/10,"prec",round(prec,4),"rec",round(rec,4),"spec",round(TN/(TN+FP),4),"F1",round(2*TP/(2*TP+FP+FN),4))

# ---------------- B33 equidad ----------------
hdr("B33 equidad")
for g_n,(TP,FN,FP,TN) in {"A":(40,10,10,40),"B":(15,15,5,65)}.items():
    n=TP+FN+FP+TN; print(g_n,"aprob",(TP+FP)/n,"TPR",TP/(TP+FN),"FPR",round(FP/(FP+TN),4),"PPV",round(TP/(TP+FP),4),"acc",(TP+TN)/n,"base",(TP+FN)/n)

# ================= PARTE C =================
hdr("C1 servidor")
srv = BN(["A","U","C","M","Q"], dict(A=[],U=[],C=["A","U"],M=["C"],Q=["C"]),
         dict(A={():0.05},U={():0.1},C={(True,True):0.95,(True,False):0.8,(False,True):0.6,(False,False):0.05},
              M={(True,):0.9,(False,):0.1},Q={(True,):0.7,(False,):0.05}))
print("P(+c)", srv.prob(dict(C=True)), "P(+m)", srv.prob(dict(M=True)))
print("P(+a|+m)", srv.query("A", dict(M=True)))
print("P(+a|+m,+u)", srv.query("A", dict(M=True,U=True)))
print("P(+a|+m,+q)", srv.query("A", dict(M=True,Q=True)))
print("P(+a|+c)", srv.query("A", dict(C=True)), "P(+a|+c,+u)", srv.query("A", dict(C=True,U=True)))
print("P(+u|+m)", srv.query("U", dict(M=True)))
for a in (True,False):
    for u in (True,False):
        f = sum(srv.p("C",c,dict(A=a,U=u))*(0.9 if c else 0.1) for c in (True,False))
        print("  f1(a=%s,u=%s)=sum_c P(c|a,u)P(+m|c)=%.4f" % (a,u,f))
    f2 = sum((0.1 if u else 0.9)*sum(srv.p("C",c,dict(A=a,U=u))*(0.9 if c else 0.1) for c in (True,False)) for u in (True,False))
    print("  f2(a=%s)=%.5f ; P(a)f2=%.6f" % (a, f2, (0.05 if a else 0.95)*f2))
for a in (True,False):
    for u in (True,False):
        f = sum(srv.p("C",c,dict(A=a,U=u))*(0.9 if c else 0.1)*(0.7 if c else 0.05) for c in (True,False))
        print("  g1(a=%s,u=%s)=sum_c P(c|a,u)P(+m|c)P(+q|c)=%.5f" % (a,u,f))
# C3 muestreo: muestras previas dadas (A,U,C,M)
prior_s = ["-a -u -c -m","-a +u +c +m","-a -u -c -m","+a -u +c +m","-a -u +c -m","-a -u -c +m","-a -u -c -m","-a +u -c -m","+a -u +c -m","-a -u -c -m",
           "-a -u -c -m","-a +u +c +m"]
acc = [s for s in prior_s if "+m" in s]; print("rechazo aceptadas", len(acc), "con +a", sum("+a" in s for s in acc))
lw_s = ["-a -u -c","-a +u +c","+a -u +c","-a -u -c","-a -u +c","+a +u +c","-a -u -c","-a +u -c"]
num=den=0
for s in lw_s:
    wv = 0.9 if "+c" in s else 0.1; den+=wv; num+=wv*("+a" in s); print("  LW", s, wv)
print("LW", num, den, num/den)
# Gibbs: estado (-a,+u,+c) con +m ; actualizar A
for a in (True,False):
    print("Gibbs A", a, (0.05 if a else 0.95)*srv.p("C",True,dict(A=a,U=True)))
for c in (True,False):
    print("Gibbs C", c, srv.p("C",c,dict(A=False,U=True))*(0.9 if c else 0.1))

hdr("C4 Naive Bayes")
nb = [("sol","si",0),("sol","no",1),("nub","no",1),("lluvia","si",0),("lluvia","no",1),("nub","si",1),("sol","no",1),("lluvia","si",0),("nub","no",1),("sol","si",0)]
for yv_ in (1,0):
    rows=[r for r in nb if r[2]==yv_]; n=len(rows); print("clase",yv_,"N",n)
    for cv in ("sol","nub","lluvia"):
        k=sum(r[0]==cv for r in rows); print("  cielo",cv,k,"MLE",k/n,"Lap",(k+1)/(n+3))
    for vv in ("si","no"):
        k=sum(r[1]==vv for r in rows); print("  viento",vv,k,"MLE",k/n,"Lap",(k+1)/(n+2))
def nbpost(c, v, lap):
    out={}
    for yv_ in (1,0):
        rows=[r for r in nb if r[2]==yv_]; n=len(rows)
        kc=sum(r[0]==c for r in rows); kv=sum(r[1]==v for r in rows)
        if lap: pc=(kc+1)/(n+3); pv=(kv+1)/(n+2); py=(n+1)/(len(nb)+2)
        else: pc=kc/n; pv=kv/n; py=n/len(nb)
        out[yv_]=py*pc*pv
    Z=out[1]+out[0]; return out, (out[1]/Z if Z else None)
for c,v in (("lluvia","si"),("nub","si"),("sol","no")):
    print(c,v,"MLE",nbpost(c,v,False),"Lap",nbpost(c,v,True))

hdr("C5 EM monedas")
heads=[5,9,8,4,7]; tA,tB=0.6,0.5
for it in range(2):
    hA=tA_=hB=tB_=0; ws=[]
    for h_ in heads:
        la=tA**h_*(1-tA)**(10-h_); lb=tB**h_*(1-tB)**(10-h_); wa=la/(la+lb); ws.append(wa)
        hA+=wa*h_; tA_+=wa*(10-h_); hB+=(1-wa)*h_; tB_+=(1-wa)*(10-h_)
    ll=sum(math.log(0.5*tA**h_*(1-tA)**(10-h_)+0.5*tB**h_*(1-tB)**(10-h_)) for h_ in heads)
    print("it",it,"tA",round(tA,4),"tB",round(tB,4),"w",[round(x,4) for x in ws],"esp A",round(hA,4),round(tA_,4),"B",round(hB,4),round(tB_,4),"ll",round(ll,4))
    tA,tB=hA/(hA+tA_),hB/(hB+tB_)
print("final",tA,tB)

hdr("C6 regresión polinomial")
xs=np.array([-2,-1,0,1,2.]); ys=np.array([4.2,0.8,0.1,1.1,3.8]); xt=np.array([3,-3.]); yt=np.array([9.1,8.8])
for deg in (1,2,4):
    Xd=np.vander(xs,deg+1,increasing=True); th=np.linalg.lstsq(Xd,ys,rcond=None)[0]
    tr=((Xd@th-ys)**2).mean(); Xt=np.vander(xt,deg+1,increasing=True); te=((Xt@th-yt)**2).mean()
    print(deg,"XtX",(Xd.T@Xd).tolist(),"Xty",(Xd.T@ys).tolist()); print("   theta",np.round(th,4),"MSEtr",round(tr,5),"pred test",np.round(Xt@th,4),"MSEte",round(te,4))

hdr("C7 k-means escalamiento")
cl_ = np.array([[10,1],[12,9],[30,2],[32,8]],float)
def km(P, mu, n=5):
    for it in range(n):
        d2=((P[:,None,:]-mu[None,:,:])**2).sum(-1); asg=d2.argmin(1)
        newmu=np.array([P[asg==k].mean(0) for k in range(len(mu))])
        J_=sum(((P[asg==k]-newmu[k])**2).sum() for k in range(len(mu)))
        print("   it",it,"d2",np.round(d2,3).tolist(),"asg",asg.tolist(),"mu'",np.round(newmu,4).tolist(),"J",round(J_,4))
        if np.allclose(newmu,mu): break
        mu=newmu
    return asg
print("crudo"); km(cl_, cl_[[0,1]].copy())
sc_ = cl_/np.array([10,1.]); print("ingreso/10"); km(sc_, sc_[[0,1]].copy())
mean=cl_.mean(0); sd=cl_.std(0); z=(cl_-mean)/sd; print("z-score", np.round(z,4).tolist(), mean, sd); km(z, z[[0,1]].copy())

hdr("C8 robot reciclaje")
gm=0.9
def RQ(V,s,a):
    if s=="H" and a=="search": return 0.7*(2+gm*V["H"])+0.3*(2+gm*V["L"])
    if s=="H" and a=="wait": return 1+gm*V["H"]
    if s=="L" and a=="search": return 0.6*(2+gm*V["L"])+0.4*(-3+gm*V["H"])
    if s=="L" and a=="wait": return 1+gm*V["L"]
    if s=="L" and a=="recharge": return 0+gm*V["H"]
acts={"H":["search","wait"],"L":["search","wait","recharge"]}
def evalpol(pi):
    # resolver lineal 2x2
    A_=np.eye(2); b_=np.zeros(2); idx={"H":0,"L":1}
    for s in ("H","L"):
        # coeficientes por diferencia finita
        base={"H":0,"L":0}; c0=RQ(base,s,pi[s]); b_[idx[s]]=c0
        for s2 in ("H","L"):
            e_={"H":0,"L":0}; e_[s2]=1; A_[idx[s],idx[s2]]-=RQ(e_,s,pi[s])-c0
    v=np.linalg.solve(A_,b_); return {"H":v[0],"L":v[1]}
pi={"H":"wait","L":"wait"}
for it in range(5):
    V=evalpol(pi); qs={s:{a:round(RQ(V,s,a),4) for a in acts[s]} for s in acts}
    newpi={s:(pi[s] if RQ(V,s,pi[s])>=max(RQ(V,s,a) for a in acts[s])-1e-12 else max(acts[s],key=lambda a:RQ(V,s,a))) for s in acts}
    print("PI",it,pi,{k:round(v,4) for k,v in V.items()},qs,"->",newpi)
    if newpi==pi: break
    pi=newpi
V={"H":0,"L":0}
for k in range(1,5):
    qs={s:{a:round(RQ(V,s,a),4) for a in acts[s]} for s in acts}; V={s:max(RQ(V,s,a) for a in acts[s]) for s in acts}
    print("VI",k,qs,{s:round(v,4) for s,v in V.items()})
for _ in range(2000): V={s:max(RQ(V,s,a) for a in acts[s]) for s in acts}
print("V*",V)

hdr("C9 Q-learning corredor")
Qc={(s,a):0.0 for s in (1,2,3) for a in ("izq","der")}
def mxc(s): return 0.0 if s in ("L","R") else max(Qc[(s,"izq")],Qc[(s,"der")])
ep_c=[[(2,"der",-1,3),(3,"der",10,"R")],
      [(1,"der",-1,2),(2,"der",-1,3),(3,"izq",-1,2),(2,"der",-1,3),(3,"der",10,"R")],
      [(2,"izq",-1,1),(1,"izq",2,"L")],
      [(1,"der",-1,2),(2,"der",-1,3),(3,"der",10,"R")]]
for e_i,ep in enumerate(ep_c):
    for s,a,r,s2 in ep:
        old=Qc[(s,a)]; y_=r+0.9*mxc(s2); Qc[(s,a)]=old+0.5*(y_-old)
        print("ep",e_i+1,(s,a,r,s2),"y=%.4f old=%.4f new=%.4f"%(y_,old,Qc[(s,a)]))
print({k:round(v,4) for k,v in Qc.items()})

hdr("C10 MC vs TD")
eps2=[[("A",0),("B",0)]]+[[("B",1)]]*6+[[("B",0)]]
# MC
retA=[0]; retB=[0]+[1]*6+[0]; print("MC V(A)",np.mean(retA),"V(B)",np.mean(retB))
# TD batch: iterar hasta convergencia con alpha pequeño
V={"A":0.,"B":0.}
for _ in range(20000):
    dV={"A":0.,"B":0.}
    for ep in eps2:
        for i_,(s,r) in enumerate(ep):
            nxt=V[ep[i_+1][0]] if i_+1<len(ep) else 0
            dV[s]+=r+nxt-V[s]
    for s in V: V[s]+=0.001*dV[s]
print("TD batch",V)
# TD online alpha 0.5 una pasada
V={"A":0.,"B":0.}
for ep in eps2:
    for i_,(s,r) in enumerate(ep):
        nxt=V[ep[i_+1][0]] if i_+1<len(ep) else 0
        V[s]+=0.5*(r+nxt-V[s])
print("TD online una pasada alpha .5",V)

hdr("C11 backprop softmax")
x=np.array([1.,-1.]); W1=np.array([[2.,1.],[1.,-1.]]); b1=np.array([0.,-3.]); W2=np.array([[1.,-1.],[0.5,1.]]); b2=np.array([0.,0.]); t=np.array([0.,1.])
def fw(W1,b1,W2,b2):
    z1=W1@x+b1; h=np.maximum(z1,0); z2=W2@h+b2; e=np.exp(z2-z2.max()); p=e/e.sum(); L=-np.log(p@t); return z1,h,z2,p,L
z1,h,z2,p,L=fw(W1,b1,W2,b2); print("z1",z1,"h",h,"z2",z2,"p",p,"L",L)
d2=p-t; dW2=np.outer(d2,h); d1=(W2.T@d2)*(z1>0); dW1=np.outer(d1,x)
print("d2",d2,"dW2",dW2,"W2^T d2",W2.T@d2,"d1",d1,"dW1",dW1)
eta=1.0; out=fw(W1-eta*dW1,b1-eta*d1,W2-eta*dW2,b2-eta*d2); print("W1'",W1-eta*dW1,"b1'",b1-eta*d1,"W2'",W2-eta*dW2,"b2'",b2-eta*d2); print("new",out)

hdr("C12 transformer")
# probabilidades del LM para "<s> el gato come </s>"
V_=["el","gato","come","pez","</s>"]
logits=[[2,0,0,0,-1],[0,2,0,1,0],[1,0,2,0,0],[0,0,1,0,3]]
targets=[0,1,2,4]
tot=0
for lg,tg in zip(logits,targets):
    lg=np.array(lg,float); p=np.exp(lg)/np.exp(lg).sum(); tot+=-math.log(p[tg]); print(np.round(p,4),"p(target)",round(p[tg],4),"-log",round(-math.log(p[tg]),4))
print("loss total",tot,"media",tot/4, "perplejidad", math.exp(tot/4))
lg=np.array(logits[2],float)
for tau in (1,0.5,2):
    p=np.exp(lg/tau)/np.exp(lg/tau).sum(); print("tau",tau,np.round(p,4))
# atención fila 3 con q3
Qm=np.array([[1,1],[0,2],[2,0]],float); Km=np.array([[1,0],[0,1],[1,1]],float); Vv=np.array([[2,0],[0,2],[1,1]],float)
S=Qm@Km.T/math.sqrt(2); M=np.triu(np.full((3,3),-np.inf),1); A=np.exp(S+M-(S+M).max(1,keepdims=True)); A/=A.sum(1,keepdims=True)
print("S",np.round(S,4)); print("A",np.round(A,4)); print("O",np.round(A@Vv,4))
print("params: V=50000,d=512 emb", 50000*512, "W_Q,W_K,W_V (d x 64)x3", 3*512*64, "W_O", 64*512)

hdr("C13 auditoria")
for g_n,(TP,FN,FP,TN) in {"A":(48,12,8,32),"B":(18,12,2,68)}.items():
    n=TP+FN+FP+TN; print(g_n,"n",n,"base",(TP+FN)/n,"aprob",(TP+FP)/n,"TPR",TP/(TP+FN),"FPR",round(FP/(FP+TN),4),"PPV",round(TP/(TP+FP),4),"acc",(TP+TN)/n)
print("global acc", (48+32+18+68)/200)
print("energia: 40 llamadas*0.3Wh", 40*0.3, "Wh ; 10000 tareas/dia ->", 40*0.3*10000/1000, "kWh/dia ; con tasa de exito 0.8 por tarea correcta", 40*0.3/0.8)

# ================= PARTE D =================
hdr("D1-1 auto")
car = BN(["B","F","S","L"], dict(B=[],F=[],S=["B","F"],L=["B"]),
         dict(B={():0.9},F={():0.95},S={(True,True):0.99,(True,False):0.0,(False,True):0.05,(False,False):0.0},L={(True,):0.95,(False,):0.1}))
print("P(-s)", car.prob(dict(S=False)))
print("P(+b|-s)", car.query("B", dict(S=False)), "-> P(-b|-s)")
print("P(+b|-s,+l)", car.query("B", dict(S=False,L=True)))
print("P(+f|-s)", car.query("F", dict(S=False)))
print("P(+f|-s,+l)", car.query("F", dict(S=False,L=True)))
print("P(+f|-s,-l)", car.query("F", dict(S=False,L=False)))
for b in (True,False):
    for f in (True,False):
        print("  P(b=%s,f=%s,-s)=%.6f" % (b,f,car.joint(dict(B=b,F=f,S=False,L=True))/car.p("L",True,dict(B=b))))
hdr("D1-2 aprendizaje auto")
recs=[(1,1,1,1),(1,1,1,1),(1,0,0,1),(0,1,0,0),(1,1,1,1),(0,1,1,0),(1,1,1,0),(0,1,0,0)]  # (B,F,S,L)
for b in (1,0):
    for f in (1,0):
        rows=[r for r in recs if r[0]==b and r[1]==f]; n=len(rows); k=sum(r[2] for r in rows)
        print("S|b=%d f=%d N=%d k=%d MLE=%s Lap=%.4f"%(b,f,n,k,(k/n if n else None),(k+1)/(n+2)))
for b in (1,0):
    rows=[r for r in recs if r[0]==b]; n=len(rows); k=sum(r[3] for r in rows); print("L|b=%d N=%d k=%d MLE=%.4f Lap=%.4f"%(b,n,k,k/n,(k+1)/(n+2)))
print("P(B) MLE", sum(r[0] for r in recs)/8)
# LW para P(B|-s) con evidencia -s, se sortean B,F (L irrelevante, se puede sortear)
lw_d=[(1,1),(0,1),(1,0),(1,1),(0,1),(1,1)]
num=den=0
for b,f in lw_d:
    wv=1-car.cpt["S"][(bool(b),bool(f))]; den+=wv; num+=wv*b; print("  LW b=%d f=%d w=%.4f"%(b,f,wv))
print("LW P^(+b|-s)",num,den,num/den if den else None)

hdr("D1-3 inventario MDP")
# estados: stock 0,1,2 ; acciones: pedir 0 o 1 (no superar 2). demanda: 1 con prob 0.5, 0 con prob 0.5.
# recompensa: +4 por venta, -1 costo de pedir unidad, -1 por unidad almacenada al final? simplificar: -0.5 por unidad al final
gm=0.8
def inv_succ(s,a):
    out=[]
    st=s+a
    for dmd,pr in ((1,0.5),(0,0.5)):
        sold=min(st,dmd); ns=st-sold; r=4*sold-1*a-0.5*ns
        out.append((ns,pr,r))
    return out
acts_i={0:[0,1],1:[0,1],2:[0]}
def IQ(V,s,a): return sum(pr*(r+gm*V[n]) for n,pr,r in inv_succ(s,a))
for s in acts_i:
    for a in acts_i[s]: print("  T",s,a,inv_succ(s,a))
V={0:0,1:0,2:0}
for k in range(1,4):
    qs={s:{a:round(IQ(V,s,a),4) for a in acts_i[s]} for s in acts_i}; V={s:max(IQ(V,s,a) for a in acts_i[s]) for s in acts_i}
    print("VI",k,qs,{s:round(v,4) for s,v in V.items()})
for _ in range(3000): V={s:max(IQ(V,s,a) for a in acts_i[s]) for s in acts_i}
print("V*",{s:round(v,4) for s,v in V.items()},{s:{a:round(IQ(V,s,a),4) for a in acts_i[s]} for s in acts_i})
# evaluar política "siempre pedir si stock<2": pi(0)=1, pi(1)=1, pi(2)=0
pi={0:1,1:1,2:0}; A_=np.eye(3); b_=np.zeros(3)
for s in (0,1,2):
    for n,pr,r in inv_succ(s,pi[s]): b_[s]+=pr*r; A_[s,n]-=gm*pr
print("V^pi pedir", np.linalg.solve(A_,b_))
pi={0:1,1:0,2:0}; A_=np.eye(3); b_=np.zeros(3)
for s in (0,1,2):
    for n,pr,r in inv_succ(s,pi[s]): b_[s]+=pr*r; A_[s,n]-=gm*pr
Vp=np.linalg.solve(A_,b_); print("V^pi pedir solo en 0", Vp, {s:{a:round(IQ({0:Vp[0],1:Vp[1],2:Vp[2]},s,a),4) for a in acts_i[s]} for s in acts_i})

hdr("D1-4 Q-learning + aprox")
Qd={("s1","a"):1.0,("s1","b"):2.0,("s2","a"):4.0,("s2","b"):0.0,("s3","a"):-1.0,("s3","b"):3.0}
def mxd(s): return 0.0 if s=="T" else max(Qd[(s,"a")],Qd[(s,"b")])
for s,a,r,s2 in [("s1","b",1,"s2"),("s2","a",-2,"s3"),("s3","b",5,"T"),("s1","a",0,"s3")]:
    old=Qd[(s,a)]; y_=r+0.8*mxd(s2); Qd[(s,a)]=old+0.25*(y_-old); print((s,a,r,s2),"y=%.4f old=%.4f new=%.4f"%(y_,old,Qd[(s,a)]))
print(Qd)
w_=np.array([0.5,1.0,-2.0]); phi=np.array([1,3,1.]); q0=w_@phi; nx=[w_@np.array([1,1,0.]),w_@np.array([1,2,1.])]
y_=-1+0.8*max(nx); dl=y_-q0; print("aprox Q",q0,"next",nx,"y",y_,"delta",dl,"w'",w_+0.1*dl*phi)

hdr("D2-1 red")
# Red: N (nublado) -> R (lluvia), N -> S (aspersor), R -> W, S -> W, R -> T (tráfico)
d2n = BN(["N","R","S","W","T"], dict(N=[],R=["N"],S=["N"],W=["R","S"],T=["R"]),
         dict(N={():0.4},R={(True,):0.7,(False,):0.1},S={(True,):0.2,(False,):0.6},
              W={(True,True):0.95,(True,False):0.85,(False,True):0.8,(False,False):0.05},T={(True,):0.6,(False,):0.2}))
print("P(+r|+t)", d2n.query("R", dict(T=True)))
print("P(+r|+w)", d2n.query("R", dict(W=True)))
print("P(+r|+w,+s)", d2n.query("R", dict(W=True,S=True)))
print("P(+t)", d2n.prob(dict(T=True)), "P(+r)", d2n.prob(dict(R=True)))
for r in (True,False):
    print("  f(N->R) r=%s: %.4f" % (r, sum((0.4 if n else 0.6)*d2n.p("R",r,dict(N=n)) for n in (True,False))))
print("P(+s|+w)", d2n.query("S", dict(W=True)), "P(+s|+w,+t)", d2n.query("S", dict(W=True,T=True)))
# VE P(R|+w): elim N then S
for r in (True,False):
    for s in (True,False):
        f1=sum((0.4 if n else 0.6)*d2n.p("R",r,dict(N=n))*d2n.p("S",s,dict(N=n)) for n in (True,False))
        print("  f1(r=%s,s=%s)=%.4f" % (r,s,f1))
    f2=sum(sum((0.4 if n else 0.6)*d2n.p("R",r,dict(N=n))*d2n.p("S",s,dict(N=n)) for n in (True,False))*d2n.p("W",True,dict(R=r,S=s)) for s in (True,False))
    print("  f2(r=%s)=%.5f"%(r,f2))

hdr("D2-2 regresión + logística + confusión")
X=np.array([[1,1],[1,2],[1,4],[1,5]],float); y=np.array([2,3,6,9],float)
th=np.linalg.solve(X.T@X,X.T@y); print("XtX",X.T@X,"Xty",X.T@y,"theta",th,"pred",X@th,"SSE",((y-X@th)**2).sum(),"pred x=6",th@[1,6])
th0=np.array([0.,0.]); xs_=np.array([[1,1],[1,3],[1,-1],[1,-2]],float); ys_=np.array([1,1,0,0.])
p=1/(1+np.exp(-(xs_@th0))); g=xs_.T@(p-ys_); print("log grad",g,"theta1",th0-0.5*g)
th1=th0-0.5*g; p1=1/(1+np.exp(-(xs_@th1))); print("p1",p1,"J0",-np.sum(np.log(0.5)*np.ones(4)),"J1",-np.sum(ys_*np.log(p1)+(1-ys_)*np.log(1-p1)))

hdr("D2-3 k-means + jerárquico")
pts2=np.array([[0,0],[0,2],[3,0],[6,6],[7,6],[9,9]],float)
asg=km(pts2, pts2[[0,3]].copy())
asg=km(pts2, pts2[[0,1]].copy())
names="ABCDEF"
Dm2={}
for i_,j_ in itertools.combinations(range(6),2):
    Dm2[(names[i_],names[j_])]=abs(pts2[i_]-pts2[j_]).sum()  # Manhattan
print({k:v for k,v in Dm2.items()})
def d(a,b): return Dm2.get((a,b), Dm2.get((b,a)))
def agglo2(link):
    cl=[frozenset(x) for x in names]; hist=[]
    while len(cl)>1:
        best=None
        for c1,c2 in itertools.combinations(cl,2):
            ds=[d(a,b) for a in c1 for b in c2]; v={"single":min(ds),"complete":max(ds)}[link]
            if best is None or v<best[0]-1e-12: best=(v,c1,c2)
        v,c1,c2=best; cl=[c for c in cl if c not in (c1,c2)]+[c1|c2]; hist.append(("".join(sorted(c1)),"".join(sorted(c2)),v))
    return hist
print("single",agglo2("single")); print("complete",agglo2("complete"))

hdr("D2-4 backprop + atención + equidad")
x=np.array([2.,1.]); w1=np.array([1.,-1.]); b1_=0.; w2_=2.; b2_=-1.; yv=0
z1=w1@x+b1_; h=max(z1,0); z2=w2_*h+b2_; p=sig(z2); L=-math.log(1-p); print("z1",z1,"h",h,"z2",z2,"p",p,"L",L)
d2_=p-yv; dw2=d2_*h; d1_=d2_*w2_*(1 if z1>0 else 0); dw1=d1_*x; print("d2",d2_,"dw2",dw2,"db2",d2_,"d1",d1_,"dw1",dw1,"db1",d1_)
eta=0.5; w1n=w1-eta*dw1; b1n=b1_-eta*d1_; w2n=w2_-eta*dw2; b2n=b2_-eta*d2_
z1=w1n@x+b1n; h=max(z1,0); z2=w2n*h+b2n; p=sig(z2); print("new",w1n,b1n,w2n,b2n,"z1",z1,"p",p,"L",-math.log(1-p))
q=np.array([1.,2.]); K=np.array([[2.,0.],[0.,1.],[1.,1.]]); Vv=np.array([[1.,0.],[0.,1.],[2.,2.]])
s=K@q/math.sqrt(2); a=np.exp(s-s.max()); a/=a.sum(); print("att s",np.round(s,4),"a",np.round(a,4),"o",np.round(a@Vv,4))
s2=s[:2]; a2=np.exp(s2-s2.max()); a2/=a2.sum(); print("mask pos2", np.round(a2,4), np.round(a2@Vv[:2],4))
for g_n,(TP,FN,FP,TN) in {"H":(30,10,15,45),"M":(20,20,5,55)}.items():
    n=TP+FN+FP+TN; print(g_n,"aprob",(TP+FP)/n,"TPR",TP/(TP+FN),"FPR",round(FP/(FP+TN),4),"PPV",round(TP/(TP+FP),4),"acc",(TP+TN)/n)
