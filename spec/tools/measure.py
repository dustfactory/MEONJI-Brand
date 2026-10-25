import re,numpy as np
from svgpathtools import parse_path
def load(f):
    s=open(f).read();polys=[]
    for d,tx,ty in re.findall(r'<path d="([^"]+)"[^>]*translate\(([\d.\-]+),([\d.\-]+)\)',s):
        p=parse_path(d)
        for sub in p.continuous_subpaths():
            pts=[]
            for seg in sub:
                for t in np.linspace(0,1,40,endpoint=False): pts.append(seg.point(t))
            a=np.array(pts);polys.append(np.c_[a.real+float(tx),a.imag+float(ty)])
    return polys
def scan_y(poly,y):
    xs=[];n=len(poly)
    for i in range(n):
        (x1,y1),(x2,y2)=poly[i],poly[(i+1)%n]
        if (y1-y)*(y2-y)<0: xs.append(x1+(y-y1)*(x2-x1)/(y2-y1))
    return sorted(xs)
def scan_x(poly,x):
    return scan_y(poly[:,::-1],x)
def fitline(pts):
    # total least squares: returns angle from horizontal (deg) and point,dir
    c=pts.mean(0);u,s,vt=np.linalg.svd(pts-c);d=vt[0]
    return c,d
def inter(c1,d1,c2,d2):
    A=np.array([d1,-d2]).T;t=np.linalg.solve(A,c2-c1);return c1+t[0]*d1
