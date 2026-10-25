from measure import *
import json
def circ(p):
    A=np.c_[2*p,np.ones(len(p))];b=(p**2).sum(1);s=np.linalg.lstsq(A,b,rcond=None)[0]
    r=np.sqrt(s[2]+s[0]**2+s[1]**2);res=np.abs(np.hypot(*(p-s[:2]).T)-r);return s[:2].round(1).tolist(),round(r,1),round(res.max(),2)
o=load('meonji-symbol.svg')[0]
def sel(P,x0,x1,y0,y1):
    m=(P[:,0]>=x0)&(P[:,0]<=x1)&(P[:,1]>=y0)&(P[:,1]<=y1);return P[m]
R={}
R['stem_bottom_L']=circ(sel(o,237,412,905,960));R['stem_bottom_M']=circ(sel(o,548,724,905,960));R['stem_bottom_R']=circ(sel(o,847,1020,905,960))
R['counter2_top']=circ(sel(o,724,847,680,760))  # inner
R['arch_outer']=circ(sel(o,800,1020,500,720))
R['tipL']=circ(sel(o,370,410,371,385));R['tipR']=circ(sel(o,575,615,377,392))
R['shoulderL_outer']=circ(sel(o,237,300,530,700))
for k,v in R.items():print(k,v)
# counters' top y
for x in [480,785]:print('x',x,[round(v,1) for v in scan_x(o,x)])
P=load('meonji-symbol.svg')
for a in P[1:3]:print('eye c',a.mean(0).round(1),'d',round(a[:,0].max()-a[:,0].min(),1))
for a in P[3:]:c,d=fitline(a);print('whisker',a[:,0].min().round(1),a[:,0].max().round(1),'ang',round(np.degrees(np.arctan2(d[1],d[0])),1),'thick',round(-2*0.5*np.sum(a[:,0]*np.roll(a[:,1],-1)-np.roll(a[:,0],-1)*a[:,1])/2/ (a[:,0].max()-a[:,0].min()),1))
json.dump(R,open('circles.json','w'),indent=1)
print('--- wordmark')
W=load('meonji-wordmark.svg')
outer=[a for a in W if 0.5*np.sum(a[:,0]*np.roll(a[:,1],-1)-np.roll(a[:,0],-1)*a[:,1])>0]
allp=np.vstack(W);print('bbox',allp.min(0).round(1),allp.max(0).round(1))
for y in [600,640,680]:
    segs=[]
    for a in outer:
        xs=scan_y(a,y);segs+= [(xs[i],xs[i+1]) for i in range(0,len(xs),2)]
    segs.sort();print(y,[(round(a,1),round(b,1)) for a,b in segs])
m=W[2];
for y in [660,690]:print('m',y,[round(v,1) for v in scan_y(m,y)])
