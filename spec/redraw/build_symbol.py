#!/usr/bin/env python3
"""Parametric rebuild of the MEONJI symbol (numeric construction spec, CONSTRUCTION_SPEC.md).
All lengths in u (1u = stem width) unless noted; 1u = GRID grid units.
Placement: original 1254 viewBox, 1u = 173.7 SVG units, same ink position."""
import math,sys
P=dict(
 GRID=51.31,          # grid units per u
 U=173.7,             # SVG units per u (measured stem width of original)
 stem=1.0, gap=0.7653, foot_r=0.5,
 ear_outer=67.0, ear_inner=53.0,  # degrees from horizontal; apex = 180-67-53 = 60
 ear_h=0.6,           # rounded ear tip top above notch, u
 ear_base=1.02,       # horizontal distance outer ear base -> notch, u
 tip_r_g=10.2,        # ear tip radius, grid units
 eye_d_g=10.2,        # eye diameter, grid units
 eye_sp=0.7653,       # eye centre-to-centre, u
 wh_ang=10.2, wh_w=0.07653,
 # reused from measured original (SVG units) -- not defined by spec
 x_left=235.75,       # chosen so the 4:3 box stays centred on original ink centre
 y_bottom=957.4,      # original ink bottom
 axis_x=486.5,        # notch axis (measured)
 head_cy=694.0,       # shoulder circle centre y (measured circle fit)
 eye_y=633.6, wh_len=59.8, wh_dx=131.3, wh_y=(657.3,690.0),
 arch_top=492.0,      # outer arch top (measured)
 arch_k=0.60,         # arch bezier handle (fitted)
 arch_ytan=735.0,     # where stem-3 outer becomes vertical (fitted)
 chin_top=661.0, chin_R=105.0,  # counter-1 pointed arch (fitted)
 color='#100f0e')
def build(P):
  # Geometry is built in GRID units (1u = GRID = 51.31 exactly); the SVG applies one uniform
  # scale transform so placement matches the original 1254 viewBox (1u = 173.7 SVG units).
  S=P['U']/P['GRID'];P=dict(P)
  for k in('x_left','y_bottom','axis_x','head_cy','eye_y','wh_len','wh_dx','arch_top','arch_ytan','chin_top','chin_R'):P[k]=round(P[k]/S,4)
  P['wh_y']=tuple(round(v/S,4) for v in P['wh_y'])
  U=P['GRID'];g=1.0;f=lambda v:round(v,6)
  x0=P['x_left'];s1=(x0,x0+U);s2=(s1[1]+P['gap']*U,s1[1]+P['gap']*U+U);s3=(s2[1]+P['gap']*U,s2[1]+P['gap']*U+U)
  W=s3[1]-x0;H=W*0.75;ytop=P['y_bottom']-H
  fr=P['foot_r']*U;yf=P['y_bottom']-fr
  ax=P['axis_x'];R=ax-x0;hc=(ax,P['head_cy'])
  # --- ear (left), mirror for right
  bx=ax-P['ear_base']*U;by=hc[1]-math.sqrt(R*R-(bx-ax)**2)
  ao,ai=math.radians(P['ear_outer']),math.radians(P['ear_inner']);rt=P['tip_r_g']*g
  apex_ang=math.pi-ao-ai
  def ear_pts(ny):
    # outer: B + t(cos ao,-sin ao); inner: N + s(-cos ai,-sin ai)
    # solve
    A=[[math.cos(ao),math.cos(ai)],[-math.sin(ao),math.sin(ai)]];b=[ax-bx,ny-by]
    det=A[0][0]*A[1][1]-A[0][1]*A[1][0];t=(b[0]*A[1][1]-A[0][1]*b[1])/det
    apx=(bx+t*math.cos(ao),by-t*math.sin(ao))
    dd=rt/math.tan(apex_ang/2)  # apex -> tangent point distance
    T1=(apx[0]-dd*math.cos(ao),apx[1]+dd*math.sin(ao))
    T2=(apx[0]+dd*math.cos(ai),apx[1]+dd*math.sin(ai))
    dc=rt/math.sin(apex_ang/2);bis=(ai-ao)/2  # bisector direction (down) tilt
    c=(apx[0]+dc*math.sin(bis),apx[1]+dc*math.cos(bis))
    return apx,T1,T2,c,c[1]-rt
  lo,hi=by-200,by+100
  for _ in range(80):
    m=(lo+hi)/2;tt=ear_pts(m)[4]
    if m-tt>P['ear_h']*U: hi=m
    else: lo=m
  ny=(lo+hi)/2;apx,T1,T2,tc,tt=ear_pts(ny)
  mx=lambda p:(2*ax-p[0],p[1])
  def bez(p,t):
    q=p
    while len(q)>1:q=[((1-t)*a[0]+t*b[0],(1-t)*a[1]+t*b[1]) for a,b in zip(q,q[1:])]
    return q[0]
  def split(p,t):
    L=[p[0]];Rr=[p[-1]];q=p
    while len(q)>1:
      q=[((1-t)*a[0]+t*b[0],(1-t)*a[1]+t*b[1]) for a,b in zip(q,q[1:])];L.append(q[0]);Rr.insert(0,q[-1])
    return L,Rr
  cx2=(s2[1]+s3[0])/2;cr=(s3[0]-s2[1])/2;k=P['arch_k'];yt=P['arch_top'];yc=P['arch_ytan'];rx=s3[1]-cx2;xl=cx2-rx
  QL=[(xl,yc),(xl,yc-k*(yc-yt)),(cx2-k*rx,yt),(cx2,yt)]
  QR=[(cx2,yt),(cx2+k*rx,yt),(s3[1],yc-k*(yc-yt)),(s3[1],yc)]
  # outer ear edge of the right ear runs straight into the arch: cut arch at x = right ear base
  lo,hi=0.0,1.0;xb=2*ax-bx
  for _ in range(60):
    m=(lo+hi)/2
    if bez(QL,m)[0]<xb: lo=m
    else: hi=m
  X=bez(QL,lo);_,QLr=split(QL,lo);arch_y_at_base=X[1]
  c2y=round(688.0/S,4)+cr
  c1=(s1[1]+s2[0])/2;hw=(s2[0]-s1[1])/2;Rc=P['chin_R'];d=Rc-hw;yc1=P['chin_top']+math.sqrt(Rc*Rc-d*d)
  C=lambda p:f"{f(p[0])},{f(p[1])}"
  out=(f"M{f(x0)},{f(yf)} L{f(x0)},{f(hc[1])} A{f(R)},{f(R)} 0 0 1 {f(bx)},{f(by)} L{C(T1)} "
       f"A{f(rt)},{f(rt)} 0 0 1 {C(T2)} L{f(ax)},{f(ny)} L{C(mx(T2))} A{f(rt)},{f(rt)} 0 0 1 {C(mx(T1))} "
       f"L{f(2*ax-bx)},{f(by)} L{C(X)} "
       f"C{C(QLr[1])} {C(QLr[2])} {C(QLr[3])} C{C(QR[1])} {C(QR[2])} {C(QR[3])} "
       f"L{f(s3[1])},{f(yf)} A{f(fr)},{f(fr)} 0 0 1 {f(s3[0])},{f(yf)} L{f(s3[0])},{f(c2y)} "
       f"A{f(cr)},{f(cr)} 0 0 0 {f(s2[1])},{f(c2y)} L{f(s2[1])},{f(yf)} A{f(fr)},{f(fr)} 0 0 1 {f(s2[0])},{f(yf)} "
       f"L{f(s2[0])},{f(yc1)} A{f(Rc)},{f(Rc)} 0 0 0 {f(c1)},{f(P['chin_top'])} A{f(Rc)},{f(Rc)} 0 0 0 {f(s1[1])},{f(yc1)} "
       f"L{f(s1[1])},{f(yf)} A{f(fr)},{f(fr)} 0 0 1 {f(x0)},{f(yf)} Z")
  er=P['eye_d_g']*g/2;es=P['eye_sp']*U/2;holes=[]
  for sx in(-1,1):
    ex=ax+sx*es;ey=P['eye_y']
    holes.append(f"M{f(ex-er)},{f(ey)} A{f(er)},{f(er)} 0 1 0 {f(ex+er)},{f(ey)} A{f(er)},{f(er)} 0 1 0 {f(ex-er)},{f(ey)} Z")
  ww=P['wh_w']*U;wr=ww/2;L=P['wh_len']-ww
  for sx in(-1,1):
    for wy,sg in zip(P['wh_y'],(1,-1)):
      a=math.radians(P['wh_ang'])*sg*sx;cx=ax+sx*P['wh_dx'];ux,uy=math.cos(a),-math.sin(a);nx_,ny_=-uy,ux
      p1=(cx-ux*L/2,wy-uy*L/2);p2=(cx+ux*L/2,wy+uy*L/2)
      A1=(p1[0]+nx_*wr,p1[1]+ny_*wr);A2=(p2[0]+nx_*wr,p2[1]+ny_*wr);B2=(p2[0]-nx_*wr,p2[1]-ny_*wr);B1=(p1[0]-nx_*wr,p1[1]-ny_*wr)
      holes.append(f"M{C(A1)} L{C(A2)} A{f(wr)},{f(wr)} 0 0 0 {C(B2)} L{C(B1)} A{f(wr)},{f(wr)} 0 0 0 {C(A1)} Z")
  svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- MEONJI symbol, parametric rebuild (CONSTRUCTION_SPEC.md). Generated by build_symbol.py -->
<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">
<path transform="scale({S:.10g})" fill="{P['color']}" fill-rule="evenodd" d="{out} {' '.join(holes)}"/>
</svg>
'''
  info=dict(box=(x0,ytop,W,H),notch=(ax,ny),apex=apx,base=(bx,by),tip_top=tt,arch_at_base=X,stems=(s1,s2,s3))
  return svg,info
if __name__=='__main__':
  svg,info=build(P);open(sys.argv[1] if len(sys.argv)>1 else 'meonji-symbol-spec.svg','w').write(svg);print(info)
