import json,re,numpy as np,cairosvg
E=json.load(open('ears.json'))
def paths(f):
    s=open(f).read();return ''.join(re.findall(r'<path[^>]+/>',s)).replace('fill="#100f0e"','fill="#100f0e" fill-opacity="0.22"').replace('fill="#FFFFFF"','fill="#ffffff"')
def L(x1,y1,x2,y2,c='#e5484d',w=2,dash=None):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def T(x,y,t,c='#e5484d',s=14,a='middle'):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{s}" font-family="Gothic A1,Noto Sans CJK KR,sans-serif" text-anchor="{a}">{t}</text>'
def dimh(x1,x2,y,lab,c='#0b7fd1'):
    return L(x1,y,x2,y,c,1.5)+L(x1,y-6,x1,y+6,c,1.5)+L(x2,y-6,x2,y+6,c,1.5)+T((x1+x2)/2,y-6,lab,c,13)
def dimv(x,y1,y2,lab,c='#0b7fd1'):
    return L(x,y1,x,y2,c,1.5)+L(x-6,y1,x+6,y1,c,1.5)+L(x-6,y2,x+6,y2,c,1.5)+f'<text x="{x+8:.1f}" y="{(y1+y2)/2:.1f}" fill="{c}" font-size="13" font-family="Gothic A1,Noto Sans CJK KR,sans-serif">{lab}</text>'
def arc(cx,cy,r,a0,a1,lab,c='#e5484d',s=1):
    # angles in degrees, SVG coords (y down), a measured clockwise from +x
    p0=(cx+r*np.cos(np.radians(a0)),cy+r*np.sin(np.radians(a0)));p1=(cx+r*np.cos(np.radians(a1)),cy+r*np.sin(np.radians(a1)))
    large=1 if abs(a1-a0)>180 else 0;sw=1 if a1>a0 else 0;am=np.radians((a0+a1)/2)
    return f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 {large} {sw} {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{c}" stroke-width="'+str(1.8*s)+'"/>'+T(cx+(r+22*s)*np.cos(am),cy+(r+22*s)*np.sin(am)+5*s,lab,c,14*s)
def grid(x0,y0,x1,y1,u,ox,oy):
    g=[]
    k=np.floor((x0-ox)/(u/4));x=ox+k*u/4
    while x<=x1:
        major=abs(((x-ox)/u)-round((x-ox)/u))<1e-6;g.append(L(x,y0,x,y1,'#9aa7b5' if major else '#d6dde5',1 if major else .5));x+=u/4
    k=np.floor((y0-oy)/(u/4));y=oy+k*u/4
    while y<=y1:
        major=abs(((y-oy)/u)-round((y-oy)/u))<1e-6;g.append(L(x0,y,x1,y,'#9aa7b5' if major else '#d6dde5',1 if major else .5));y+=u/4
    return ''.join(g)
def ears(e,u,s=1):
    g=[];bl=max(e['L']['base_out'][1],e['R']['base_out'][1])
    for k in 'LR':
        d=e[k]
        for ln,b,fl in [(d['line1'],d['base_out'],d['flank1_deg']),(d['line2'],d['base_in'],d['flank2_deg'])]:
            c=np.array(ln[0]);v=np.array(ln[1]);ap=np.array(d['virtual_apex'])
            # point on baseline
            t=(bl-c[1])/v[1];pb=c+t*v
            g.append(L(ap[0],ap[1],pb[0]+v[0]*12*s,bl+v[1]*12*s,'#e5484d',1.6*s,'6 4'))
            # angle from horizontal at baseline: arc between horizontal outward side and line going up
            up=np.degrees(np.arctan2(-v[1],-v[0]))  # direction toward apex
            hor=180 if v[0]>0 else 0  # horizontal pointing away from ear interior... choose the side under the ear exterior
            hor=0 if up>-90 else -180
            a0,a1=sorted([hor,up]) if hor==0 else sorted([up,-180])
            rr=(40 if b is d['base_out'] else (60 if k=='L' else 95))*s
            g.append(arc(pb[0],pb[1],rr,a0,a1,f'{fl:.1f}°',s=s))
        ap=d['virtual_apex'];g.append(f'<circle cx="{ap[0]}" cy="{ap[1]}" r="{3*s}" fill="#e5484d"/>')
        g.append(T(ap[0],ap[1]-12*s,f'꼭짓각 {d["apex_deg"]:.1f}°','#b42318',15*s))
        tp=d['tip'];g.append(f'<circle cx="{tp[0]}" cy="{tp[1]}" r="{3*s}" fill="#7a3fd1"/>')
    g.append(L(e['L']['base_out'][0]-60*s,bl,e['R']['base_out'][0]+60*s,bl,'#e5484d',1.2*s))
    g.append(T(e['L']['base_out'][0]-62*s,bl+4,'귀 기준선(수평)','#e5484d',12*s,'end'))
    return ''.join(g)
def wrap(vb,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{vb.split()[2]}" height="{vb.split()[3]}"><rect x="{vb.split()[0]}" y="{vb.split()[1]}" width="100%" height="100%" fill="#fff"/>{body}</svg>'
C=json.load(open('circles.json'))
# SYMBOL
u=173.7;ox,oy=236.9,957.4
b=grid(140,150,1150,1060,u,ox,oy)+paths('meonji-symbol.svg')
b+=ears(E['meonji-symbol.svg'],u)
b+=dimh(236.9,1019.5,1000,'W 782.6 = 4.51u')+dimv(1060,371.4,957.4,'H 586.0 = 3.37u')
for a,c,lab in [(237.2,411.7,'174.5 (1.00u)'),(548.6,723.6,'175.0 (1.01u)'),(847.6,1019.3,'171.7 (0.99u)')]:b+=dimh(a,c,820,lab,'#0a7a3d')
b+=dimh(411.7,548.6,780,'137.1 (0.79u)','#c27c0e')+dimh(723.6,847.6,780,'124.0 (0.71u)','#c27c0e')
b+=L(140,371.4,1080,371.4,'#7a3fd1',1,'3 3')+T(150,366,'L 귀끝 y371.4','#7a3fd1',12,'start')+L(140,377.6,1080,377.6,'#7a3fd1',1,'3 3')+T(700,392,'R 귀끝 y377.6 (Δ6.2)','#7a3fd1',12,'start')
b+=L(400,481.2,580,481.2,'#7a3fd1',1,'3 3')+T(487,470,'노치 y481.2','#7a3fd1',12)
for k in ['tipL','tipR','counter2_top']:
    (cx,cy),r,_=C[k];b+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#7a3fd1" stroke-width="1.2"/>'+T(cx,cy+5,f'R{r}','#7a3fd1',12)
b+=T(160,180,'MEONJI 심볼 구성도 — 1u = 줄기 폭 173.7 (원본 SVG 단위), 굵은 격자 1u / 얇은 격자 ¼u, 원점 = 좌하단','#111',18,'start')
b+=T(160,205,'귀 각도: 귀 기준선(수평)에서 측면 직선(25–75% 높이 구간 최소자승 적합)까지의 각','#111',14,'start')
open('construction-symbol.svg','w').write(wrap('140 150 1010 910',b))
# WORDMARK
uw=58.8;ox,oy=90.5,718.8
b=grid(60,440,1222,830,uw,ox,oy)+paths('meonji-wordmark.svg')
b+=dimh(90.5,1191.4,815,'W 1100.9 = 18.72u')+dimv(1205,485.7,780.2,'H 294.5 = 5.01u')
gaps=[(352.4,359.4,'7.0'),(520.3,529.8,'9.5'),(701.2,707.7,'6.5'),(864.6,878.3,'13.7'),(936.4,951.7,'15.3')]
for a,c,lab in gaps:b+=L(a,640,c,640,'#c27c0e',2)+T((a+c)/2,800,lab,'#c27c0e',11)+L((a+c)/2,645,(a+c)/2,788,'#c27c0e',.6,'2 2')
b+=dimh(90.5,149.6,740,'59.1','#0a7a3d')+dimh(707.8,766.6,740,'58.8','#0a7a3d')
b+=L(60,553.3,1222,553.3,'#7a3fd1',1,'3 3')+T(1220,549,'x-height 상단 y553.3','#7a3fd1',11,'end')+L(60,719.9,1222,719.9,'#7a3fd1',1,'3 3')+T(1220,733,'베이스라인 y719.9 (x-height 166.6 = 2.83u)','#7a3fd1',11,'end')
b+=T(70,462,'MEONJI 워드마크 구성도 — 1u = 줄기 폭 58.8, 굵은 격자 1u / 얇은 격자 ¼u. 주황 = 글자 사이 간격(y=640 측정)','#111',14,'start')
ins='<g transform="translate(-200,-560) scale(3)">'+grid(80,470,260,580,uw,ox,oy)+paths('meonji-wordmark.svg').split('<path',4)[0]+'<path'+paths('meonji-wordmark.svg').split('<path')[3]+ears(E['meonji-wordmark.svg'],uw,0.33)+'</g>'
b+='<rect x="60" y="830" width="1162" height="420" fill="#fff"/><g clip-path="url(#c)">'+ins+'</g>'+T(70,865,'확대(×3): 워드마크 m 귀 — 각도는 귀 기준선(수평)에서 측정','#111',15,'start')
b='<defs><clipPath id="c"><rect x="60" y="875" width="600" height="345"/></clipPath></defs>'+b
open('construction-wordmark.svg','w').write(wrap('60 440 1162 790',b))
for f in ['construction-symbol','construction-wordmark']:cairosvg.svg2png(url=f+'.svg',write_to=f+'.png',output_width=2400)
