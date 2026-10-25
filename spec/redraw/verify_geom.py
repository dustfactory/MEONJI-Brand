"""Exact verification from the SVG path data (no rasterising). Units: grid units (1u = 51.31)."""
import re,math
t=open('meonji-symbol-spec.svg').read()
d=re.search(r' d="([^"]+)"',t).group(1);GU=51.31
subs=[];cur=None
for cmd,args in re.findall(r'([MLACZ])([^MLACZ]*)',d):
  n=[float(x) for x in re.findall(r'-?\d+\.?\d*(?:e-?\d+)?',args)]
  if cmd=='M':cur=[('M',n)];subs.append(cur)
  else:cur.append((cmd,n))
def pts(sp):
  out=[]
  for c,n in sp:
    if c in'ML':out.append(('P',n[0],n[1]))
    elif c=='A':out.append(('A',n[5],n[6],n[0]))
    elif c=='C':out.append(('C',n[4],n[5]))
  return out
body=pts(subs[0]);eyes=subs[1:3];wh=subs[3:7]
P=lambda i:(body[i][1],body[i][2])
# body order: 0 M(x0,yf) 1 L(x0,hc) 2 A->B 3 L T1 4 A T2 (tip r) 5 L N 6 L T2' 7 A T1' 8 L B' ...
ang=lambda a,b:math.degrees(math.atan2(abs(a[1]-b[1]),abs(a[0]-b[0])))
B,T1,T2,N,T2r,T1r,Br=P(2),P(3),P(4),P(5),P(6),P(7),P(8)
rows=[]
def row(name,spec,val,unit):
  tol=0.005 if unit=='°' else 0.0005*GU if unit=='grid' else 0.0005
  rows.append((name,spec,val,unit,abs(val-float(spec))>tol))
row('귀 바깥 변 L','67',ang(B,T1),'°');row('귀 바깥 변 R','67',ang(Br,T1r),'°')
row('귀 안쪽 변 L','53',ang(N,T2),'°');row('귀 안쪽 변 R','53',ang(N,T2r),'°')
row('귀끝 R L (격자 단위, 반지름)','10.2',body[4][3],'grid');row('귀끝 R R (격자 단위, 반지름)','10.2',body[7][3],'grid')
row('귀 밑동 폭 L (u, 밑동→노치 수평)','1.02',(N[0]-B[0])/GU,'u');row('귀 밑동 폭 R','1.02',(Br[0]-N[0])/GU,'u')
# stems: vertical edges at foot start yf = y of point 0
yf=P(0)[1];xs=sorted({round(p[1],9) for p in body if p[0] in'PA' and abs(p[2]-yf)<1e-9})
for i in range(0,6,2):row(f'줄기 {i//2+1} 폭 (u)','1',(xs[i+1]-xs[i])/GU,'u')
row('줄기 사이 1 (u)','0.7653',(xs[2]-xs[1])/GU,'u');row('줄기 사이 2 (u)','0.7653',(xs[4]-xs[3])/GU,'u')
ec=[];er=[]
for e in eyes:
  m=e[0][1];a=e[1][1];ec.append(((m[0]+a[5])/2,(m[1]+a[6])/2));er.append(a[0])
row('눈 간격 중심–중심 (u)','0.7653',(ec[1][0]-ec[0][0])/GU,'u')
for i in(0,1):row(f'눈 지름 {"LR"[i]} (격자 단위)','10.2',2*er[i],'grid')
row('눈 중점 − 노치 축 (u)','0',((ec[0][0]+ec[1][0])/2-N[0])/GU,'u')
for i,w in enumerate(wh):
  A1=w[0][1];A2=w[1][1];r=w[2][1][0]
  row(f'수염 {i+1} 각도 (°, 중심선)','10.2',ang(A1,A2),'°');row(f'수염 {i+1} 굵기 (u)','0.07653',2*r/GU,'u')
L=['| 항목 | 규격 | SVG 경로 좌표로 계산한 값 | 단위 | 판정 |','|---|---|---|---|---|']
for n,sp,v,u,bad in rows:L.append(f'| {n} | {sp} | {v:.6f} | {u} | {"⚠️ 초과" if bad else "OK"} |')
L.append(f'\n줄기 모서리 x (격자 단위): {", ".join(f"{x:.6f}" for x in xs)}')
L.append(f'꼭짓각 = 180 − 67 − 53 = 60°; 1u = 51.31 격자 단위, 0.7653u = {0.7653*GU:.6f}, 0.07653u = {0.07653*GU:.6f}, 1.02u = {1.02*GU:.6f}')
print('\n'.join(L));open('VERIFY_GEOMETRY.md','w').write('# 기하 검증 (SVG 경로 좌표 직접 계산, 래스터 아님)\n허용: 길이 0.0005u, 각도 0.005°\n\n'+'\n'.join(L)+'\n')
assert not any(r[4] for r in rows)
