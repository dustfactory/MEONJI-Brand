from measure import *
import json
def top_prof(o,x0,x1,st=0.25):
    xs=np.arange(x0,x1,st);t=[]
    for x in xs:
        v=scan_x(o,x+1e-3);t.append(min(v) if v else np.nan)
    t=np.array(t);return xs,t
def ear(o,tip,b1,b2):
    def flank(base):
        h=base[1]-tip[1];y0=tip[1]+0.25*h;y1=tip[1]+0.75*h
        x0,x1=sorted([tip[0],base[0]])
        msk=(o[:,0]>=x0)&(o[:,0]<=x1)&(o[:,1]>=y0)&(o[:,1]<=y1);p=o[msk];c,d=fitline(p)
        d=np.array([abs(d[0])*np.sign(base[0]-tip[0]),abs(d[1])])
        return c,d,np.degrees(np.arctan2(d[1],abs(d[0]))),np.abs((p-c)@np.array([-d[1],d[0]])).max()
    c1,d1,a1,e1=flank(b1);c2,d2,a2,e2=flank(b2)
    ap=inter(c1,d1,c2,d2);apex=np.degrees(np.arccos(d1@d2/np.linalg.norm(d1)/np.linalg.norm(d2)))
    bis=d1/np.linalg.norm(d1)+d2/np.linalg.norm(d2);tilt=np.degrees(np.arctan2(-bis[0],bis[1]))
    return dict(tip=np.round(tip,1).tolist(),base_out=np.round(b1,1).tolist(),base_in=np.round(b2,1).tolist(),flank1_deg=round(a1,1),flank2_deg=round(a2,1),apex_deg=round(apex,1),virtual_apex=ap.round(1).tolist(),axis_tilt_deg=round(tilt,1),fit_maxdev=[round(e1,2),round(e2,2)],line1=[c1.tolist(),d1.tolist()],line2=[c2.tolist(),d2.tolist()])
def find(o,x0,x1):
    xs,t=top_prof(o,x0,x1)
    from scipy.signal import medfilt
    t=medfilt(t,9)
    return xs,t
out={}
for f,idx,rng in [('meonji-symbol.svg',0,(237,760)),('meonji-wordmark.svg',2,(91,240))]:
    o=load(f)[idx];xs,t=find(o,*rng)
    W=rng[1]-rng[0]
    # tips: two global minima separated
    i1=np.nanargmin(t);tip1=np.array([xs[i1],t[i1]])
    far=np.abs(xs-xs[i1])>W*0.2;i2=np.nanargmin(np.where(far,t,np.inf));tip2=np.array([xs[i2],t[i2]])
    LT,RT=sorted([tip1,tip2],key=lambda p:p[0])
    k=(xs>LT[0])&(xs<RT[0]);iN=np.where(k)[0][np.nanargmax(t[k])];N=np.array([xs[iN],t[iN]])
    # outer bases: max curvature kink -> largest second difference on flank outside tips
    def kink(a,b):
        k=np.where((xs>a)&(xs<b))[0];d2=np.abs(np.gradient(np.gradient(t[k])));j=k[np.nanargmax(d2)];return np.array([xs[j],t[j]])
    LB=kink(rng[0]+3,LT[0]-10);RB=kink(RT[0]+10,rng[1]-3)
    out[f]=dict(L=ear(o,LT,LB,N),R=ear(o,RT,RB,N),notch=N.round(1).tolist())
    for s in 'LR':print(f,s,{k:v for k,v in out[f][s].items() if not k.startswith('line')})
    print('notch',N)
json.dump(out,open('ears.json','w'),indent=1,default=float)
