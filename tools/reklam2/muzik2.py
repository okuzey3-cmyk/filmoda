# Filmoda reklam muzigi + efektler (ozgun, sentezlenmis). 14.37 sn ses uzerine, 3.88'den itibaren 120 bpm.
import numpy as np, wave, sys
SR=44100; TOT=float(sys.argv[1]) if len(sys.argv)>1 else 15.27
n=int(SR*(TOT+1)); L=np.zeros(n); R=np.zeros(n); rng=np.random.default_rng(11)
mid=lambda m:440*2**((m-69)/12)
tk=lambda l:np.arange(int(l*SR))/SR
def add(sig,st,pan=.5,g=1.0):
    i=int(st*SR)
    if i<0 or i>=n: return
    e=min(n,i+len(sig)); s=sig[:e-i]*g; L[i:e]+=s*(1-pan)*1.4; R[i:e]+=s*pan*1.4
def lp(x,k): return np.convolve(x,np.ones(k)/k,'same')
def pad(m,st,l,g,att=.6,rel=.8,pan=.5):
    k=tk(l); o=0
    for d in(-.004,.004,0): f=mid(m)*(1+d); o=o+np.sin(2*np.pi*f*k)+.3*np.sin(4*np.pi*f*k)
    e=np.minimum(1,k/att)*np.minimum(1,(l-k)/rel); add(o*e*g/3,st,pan)
def pluck(m,st,g=.1,pan=.5,dec=.35):
    k=tk(1.2); f=mid(m); s=(np.sin(2*np.pi*f*k)+.4*np.sin(4*np.pi*f*k)*np.exp(-k*8)+.15*np.sin(6*np.pi*f*k)*np.exp(-k*14))*np.exp(-k/dec)
    s*=np.minimum(1,k/.003); add(s,st,pan,g)
def bell(m,st,g=.07,pan=.5,dec=1.6):
    k=tk(3.5); f=mid(m); s=0
    for r,a in((1,1),(2.76,.45),(5.4,.2),(8.9,.1)): s=s+a*np.sin(2*np.pi*f*r*k)*np.exp(-k/(dec/(1+.35*r)))
    s*=np.minimum(1,k/.003); add(s,st,pan,g)
def bass(m,st,l=.45,g=.2):
    k=tk(l); f=mid(m); s=np.tanh(2.2*np.sin(2*np.pi*f*k))*np.exp(-k/.3)*np.minimum(1,k/.005); add(s,st,.5,g)
def kick(st,g=.3):
    k=tk(.35); f=130*np.exp(-k*22)+46; add(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-k/.11),st,.5,g)
def clap(st,g=.16):
    k=tk(.25); x=lp(rng.standard_normal(len(k)),3)*np.exp(-k/.06)
    for o in(.0,.012,.024): pass
    add(x,st,.5,g)
def hat(st,g=.05,op=False):
    k=tk(.12 if op else .05); x=rng.standard_normal(len(k)); x=x-lp(x,6); add(x*np.exp(-k/(.05 if op else .014)),st,.5+.1*rng.uniform(-1,1),g)
def whoosh(st,l=.6,g=.3,up=True):
    k=tk(l); x=rng.standard_normal(len(k)); y=np.zeros_like(x)
    for q in range(4): 
        w=int(8+ (60 if up else 8)*(1-(k/l))**1.0) if False else 20
    y=lp(x,18); y=y-lp(x,120); env=np.sin(np.pi*np.clip(k/l,0,1))**2 if True else 0
    env=(k/l)**2*np.exp(-3*(k/l)**3) if up else (1-k/l)**2; add(y*env*5,st,.5,g)
def boom(st,g=.5):
    k=tk(2.2); f=62*np.exp(-k*1.6)+34; add(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-k/.8),st,.5,g)
    k2=tk(.5); add(lp(rng.standard_normal(len(k2)),4)*np.exp(-k2/.12),st,.5,g*.7)
def riser(st,l,g=.14):
    k=tk(l); x=rng.standard_normal(len(k)); y=lp(x,10)*(k/l)**2.4; add(y*3,st,.5,g)
def blip(f0,st,g=.12,pan=.5):
    k=tk(.28); f=f0*(1+.5*np.minimum(k/.05,1)); add(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-k/.09)*np.minimum(1,k/.003),st,pan,g)
def click(st,g=.12):
    k=tk(.05); add(np.sin(2*np.pi*1800*k)*np.exp(-k/.008),st,.5,g)
def tick(f,st,g=.12,pan=.5):
    bell(f,st,g,pan,.9)
# ---------- 0 - 3.88 sakin, yorgun gun hissi ----------
for j,m in enumerate((48,55,64,67)): pad(m,0,3.9,.07 if j else .1,1.2,.6,.5)
for t,m in((0.4,76),(1.2,72),(2.0,74),(2.8,67)): pluck(m,t,.07,.5,.7)
riser(2.6,1.28,.16)
# ---------- 3.88 ->  120 bpm ----------
T0=3.88; beat=.5; bar=2.0
boom(T0,.55); whoosh(T0-.35,.5,.35); bell(84,T0,.08,.4,2.2)
prog=[(48,(60,64,67),[72,76,79,76]),(43,(59,62,67),[71,74,79,74]),(45,(60,64,69),[72,76,81,76]),(41,(60,65,69),[72,77,81,77])]
bar_i=0; t=T0
while t<TOT-.2:
    root,ch,arp=prog[bar_i%4]
    for m in ch: pad(m,t,bar+.15,.05,.08,.35,.5)
    for b in range(4):
        tb=t+b*beat; kick(tb,.28 if b%2==0 else .22)
        if b%2==1: clap(tb,.13)
        hat(tb+.25,.045); hat(tb,.025)
        bass(root-12,tb,.42,.2); bass(root-12,tb+.25,.2,.1) if b%2==0 else None
        for e in range(2):
            ts=tb+e*.25
            pluck(arp[(b*2+e)%4],ts,.075,.3+.4*((b*2+e)%2),.28)
    bar_i+=1; t+=bar
# ---------- efektler (ses kelimelerine gore) ----------
click(4.52); blip(700,5.82,.1); click(5.72)
whoosh(5.75,.4,.3)
for tt,f in((6.06,520),(6.34,660),(6.62,820)): blip(f,tt,.16); bell(f*2,tt,.05,.5,.8)
whoosh(7.1,.35,.25,False); whoosh(7.2,.4,.3); blip(900,7.28,.14); bell(96,7.3,.05,.5,1.2)
bell(91,9.08,.05,.5,1.2)
for tt,f in((9.84,81),(10.78,84),(11.74,88)): tick(f,tt,.14); blip(f*8,tt,.07)
whoosh(12.1,.45,.35); boom(12.56,.5); bell(88,12.56,.09,.4,2.4); bell(96,12.7,.05,.6,2.0)
for j,m in enumerate((48,60,64,67,76)): pad(m,12.56,2.8,.07,.05,1.2)
# ---------- son ----------
fade=np.ones(n); ft=int(.7*SR); a=int(TOT*SR); fade[a-ft:a]=np.linspace(1,0,ft); fade[a:]=0
x=np.stack([L*fade,R*fade],1)
x=x/np.max(np.abs(x))*.9
d=(np.clip(x,-1,1)*32767).astype(np.int16)
w=wave.open("/tmp/muzik2.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes()); w.close(); print("tamam")
