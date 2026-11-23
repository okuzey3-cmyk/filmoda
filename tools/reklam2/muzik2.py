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
# ---------- 0 - 4.58 sakin, yorgun gun hissi ----------
for j,m in enumerate((48,55,64,67)): pad(m,0,4.7,.07 if j else .1,1.4,.6,.5)
for t,m in((0.5,76),(1.5,72),(2.5,74),(3.5,67)): pluck(m,t,.065,.5,.8)
riser(3.3,1.25,.14)
# ---------- 4.58 -> 120 bpm ----------
T0=4.58; beat=.5; bar=2.0
boom(T0,.5); whoosh(T0-.4,.5,.28); bell(84,T0,.07,.4,2.4)
prog=[(48,(60,64,67),[72,76,79,76]),(43,(59,62,67),[71,74,79,74]),(45,(60,64,69),[72,76,81,76]),(41,(60,65,69),[72,77,81,77])]
bar_i=0; t=T0
while t<15.3:
    root,ch,arp=prog[bar_i%4]
    for m in ch: pad(m,t,bar+.15,.05,.08,.35,.5)
    for b in range(4):
        tb=t+b*beat
        if tb>=T0+2.0: kick(tb,.2 if b%2==0 else .15)
        if b%2==1 and tb>=T0+2.0: clap(tb,.09)
        if tb>=T0+2.0: hat(tb+.25,.035)
        bass(root-12,tb,.42,.16)
        for e in range(2):
            ts=tb+e*.5*beat*2/2
            if e==0 or True: pluck(arp[(b*2+e)%4],tb+e*.25,.06,.3+.4*((b*2+e)%2),.3)
    bar_i+=1; t+=bar
# bitis bolumu (15.36 -> son): sade, genis
for j,m in enumerate((48,60,64,67,76)): pad(m,15.36,3.2,.07,.05,1.4)
# ---------- efektler (seyrek, yumusak) ----------
click(5.95,.1)
for tt,f in((6.8,520),(7.25,660),(7.7,820)): blip(f,tt,.1); bell(f*2,tt,.04,.5,.9)
blip(900,8.68,.09); bell(96,8.7,.05,.5,1.4); bell(91,10.25,.045,.5,1.2)
for tt,f in((11.94,81),(12.88,84),(13.84,88)): tick(f,tt,.12)
whoosh(14.9,.45,.25); boom(15.36,.45); bell(88,15.36,.09,.4,2.6); bell(96,15.5,.05,.6,2.2)
# ---------- son ----------
fade=np.ones(n); ft=int(.7*SR); a=int(TOT*SR); fade[a-ft:a]=np.linspace(1,0,ft); fade[a:]=0
x=np.stack([L*fade,R*fade],1)
x=x/np.max(np.abs(x))*.9
d=(np.clip(x,-1,1)*32767).astype(np.int16)
w=wave.open("/tmp/muzik2.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes()); w.close(); print("tamam")
