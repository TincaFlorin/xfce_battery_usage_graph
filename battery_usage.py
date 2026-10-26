#!/usr/bin/env python3
# XFCE Battery usage
import time,glob,gi
gi.require_version('Gtk','3.0'); from gi.repository import Gtk,Gdk,GLib

S={'x':-1,'d':[],'c':0}

def U():
 S['c']=time.time()-86400; d=[]
 for f in glob.glob('/var/lib/upower/*charge*.dat'):
  for l in open(f):
   try:
    p=l.split(); t=float(p[0])
    if t>=S['c']: d.append((t,float(p[1])))
   except: pass
 S['d']=sorted(d); return 1

def C(da,c):
 w,h=da.get_allocated_width(),da.get_allocated_height(); m=35; gw,gh=w-m*2,h-m*2
 c.set_source_rgb(0.1,0.1,0.1); c.paint(); c.set_source_rgba(1,1,1,0.3)
 for v in (0,50,100):
  y=m+gh-v/100*gh; c.move_to(m,y); c.line_to(w-m,y); c.stroke()
  c.move_to(5,y+4); c.show_text(f"{v}%")
 for i in range(5):
  c.move_to(m+i*gw/4-15,h-10); c.show_text(time.strftime('%H:%M',time.localtime(S['c']+i*21600)))
 if not S['d']: return
 c.set_source_rgb(0.2, 0.8, 0.4); c.set_line_width(2)
 for i in range(144):
  v = [p[1] for p in S['d'] if S['c']+i*600 <= p[0] < S['c']+i*600+600]
  if v:
   x = m + gw * (i + 0.5) / 144
   c.move_to(x, m + gh); c.line_to(x, m + gh - (sum(v)/len(v)) / 100 * gh)
 c.stroke(); c.set_line_width(1)
 if m<=S['x']<=w-m and S['d']:
  pt=min(S['d'],key=lambda k:abs(k[0]-(S['c']+(S['x']-m)/gw*86400)))
  px,py=m+gw*(pt[0]-S['c'])/86400,m+gh-pt[1]/100*gh
  c.set_source_rgb(1,1,1); c.move_to(px,m); c.line_to(px,m+gh); c.stroke()
  c.arc(px,py,4,0,6.28); c.fill()
  c.move_to(px+10 if px<w/2 else px-95,py-10); c.show_text(f"{pt[1]}% @ {time.strftime('%H:%M',time.localtime(pt[0]))}")

def M(w,e): S['x']=e.x; w.queue_draw()

open('/tmp/b.svg','w').write('<svg viewBox="0 0 32 32"><rect x="2" y="10" width="24" height="12" fill="none" stroke="#33d17a" stroke-width="2"/><rect x="26" y="13" width="4" height="6" fill="#33d17a"/></svg>')

W=Gtk.Window(); W.set_default_size(700, 400); W.set_icon_from_file('/tmp/b.svg'); W.connect("destroy",Gtk.main_quit)
A=Gtk.DrawingArea(); A.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
A.connect("motion-notify-event",M); A.connect("draw",C); W.add(A)
U(); GLib.timeout_add_seconds(60,lambda:U() and A.queue_draw())
W.show_all(); Gtk.main()