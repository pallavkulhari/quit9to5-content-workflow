# Ported from the box (cards/fmt12.py). Structured card formats (title, checklist, numbers, myth/reality, 3-step) on the v1a template.
# Imported by batch scripts; see docs/carousels-and-cards.md. Same env as var.py.
"""Batch 12 structured card formats on the approved brand template (white, coral bar, avatar header, cover footer)."""
import os,sys
H=os.environ.get("Q9_CARD_ASSETS",os.path.dirname(os.path.abspath(__file__)))  # needs pallav_photo.jpg + book_cover.jpeg (not in repo);sys.path.insert(0,H)
from make_insta import font,avatar,badge,cover,shadow,S,W,RED,INK,GR
from var import rdraw,rheight
from PIL import Image,ImageDraw
HLC=(247,216,215);GREYBG=(243,243,243);REDBG=(252,236,235);LINE=(222,222,222)

def wrapw(d,t,f,mw):
    out=[];cur=""
    for wd in t.split():
        x=(cur+" "+wd).strip()
        if d.textlength(x,font=f)<=mw:cur=x
        else:out.append(cur);cur=wd
    return out+[cur]

class Ctx:
    def __init__(s,story):
        s.story=story;s.H=1920 if story else 1080
        s.L=(88 if story else 52)*S;s.R=(W-(88 if story else 52))*S
        s.d=None
def header_footer(img,story):
    Hh=1920 if story else 1080
    d=ImageDraw.Draw(img);L=(88 if story else 52)*S
    d.rectangle((0,0,W*S,(18 if story else 14)*S),fill=RED)
    if story:
        AV=120*S;y0=110*S;nf=font(40,700);hf=font(34,400);nx=L+AV+30*S
    else:
        AV=84*S;y0=40*S;nf=font(32,700);hf=font(27,400);nx=L+AV+24*S
    d.ellipse((L-3*S,y0-3*S,L+AV+3*S,y0+AV+3*S),fill=RED);a,m=avatar(AV);img.paste(a,(L,y0),m)
    d=ImageDraw.Draw(img);nm="Pallav Kulhari"
    d.text((nx,y0+AV*.42),nm,font=nf,fill=INK,anchor="ls")
    bs=(40 if story else 30)*S;badge(d,nx+d.textlength(nm,font=nf)+10*S,y0+AV*.42-bs*.82,bs)
    d.text((nx,y0+AV*.8),"@Quit9to5Book",font=hf,fill=GR,anchor="ls")
    # footer
    if story:
        cv=cover(330*S);fy=Hh*S-cv.size[1]-300*S;fs_=44
    else:
        cv=cover(172*S);fy=Hh*S-cv.size[1]-34*S;fs_=30
    cw,ch=cv.size;shadow(img,(L,fy,L+cw,fy+ch),blur=14 if not story else 18);d=ImageDraw.Draw(img);img.paste(cv,(L,fy))
    d.rectangle((L,fy,L+cw-1,fy+ch-1),outline=(225,225,225),width=S)
    tx=L+cw+(44 if story else 30)*S;mid=fy+ch//2
    d.line((tx,mid-(30 if story else 20)*S,tx+(80 if story else 56)*S,mid-(30 if story else 20)*S),fill=RED,width=(5 if story else 4)*S)
    d.text((tx,mid+(34 if story else 24)*S),"Coming January 2027",font=font(fs_,600),fill=RED,anchor="ls")
    top=(110+120+60 if story else 40+84+36)*S
    return d,top,fy-(30 if story else 22)*S

# ---------- blocks (each returns new y; draw flag lets us measure) ----------
def title(d,x,y,w,txt,fs,draw,col=INK):
    f=font(fs,800);lh=int(fs*1.22)*S;ls=wrapw(d,txt,f,w)
    if draw:
        for i,l in enumerate(ls):d.text((x,y+lh*(i+0.8)),l,font=f,fill=col,anchor="ls")
    return y+len(ls)*lh
def para(d,x,y,w,txt,fs,wt,col,draw,lh=1.4):
    f=font(fs,wt);l_=int(fs*lh)*S;ls=wrapw(d,txt,f,w)
    if draw:
        for i,l in enumerate(ls):d.text((x,y+l_*(i+0.78)),l,font=f,fill=col,anchor="ls")
    return y+len(ls)*l_
def hl(d,x,y,w,txt,fs,draw):
    f=font(fs,500);lh=int(fs*1.45)*S
    h=rheight(d,"["+txt+"]",f,w,lh,0)
    if draw:rdraw(d,"["+txt+"]",f,w,x,y,lh,0,int(fs*1.05)*S,fs*S)
    return y+h

def checklist(d,x,y,w,items,fs,draw,gap=0.55):
    f=font(fs,500);bs=int(fs*0.95)*S;tw=w-bs-int(fs*0.6)*S;lh=int(fs*1.32)*S
    for it in items:
        ls=wrapw(d,it,f,tw)
        if draw:
            by=y+int(fs*0.12)*S
            d.rounded_rectangle((x,by,x+bs,by+bs),radius=int(bs*.2),outline=RED,width=max(3,int(fs*0.09))*S)
            for i,l in enumerate(ls):d.text((x+bs+int(fs*0.6)*S,y+lh*(i+0.78)),l,font=f,fill=INK,anchor="ls")
        y+=len(ls)*lh+int(fs*gap)*S
    return y

def steps(d,x,y,w,items,fs,draw):
    r=int(fs*0.95)*S;fb=font(fs,800);ft=font(fs,400);lh=int(fs*1.36)*S;tw=w-2*r-int(fs*0.7)*S
    for name,body in items:
        ls=wrapw(d,body,ft,tw)
        h=lh+len(ls)*lh
        if draw:
            cx=x+r;cy=y+r
            d.ellipse((x,y,x+2*r,y+2*r),fill=RED)
            nf=font(int(fs*1.15),800);d.text((cx,cy),str(items.index((name,body))+1),font=nf,fill="white",anchor="mm")
            tx=x+2*r+int(fs*0.7)*S
            d.text((tx,y+lh*0.78),name,font=fb,fill=INK,anchor="ls")
            for i,l in enumerate(ls):d.text((tx,y+lh*(i+1.78)),l,font=ft,fill=INK,anchor="ls")
        y+=h+int(fs*0.6)*S
    return y

def myth(d,x,y,w,rows,fs,draw,hdr="MYTH",hdr2="REALITY"):
    gap=int(fs*0.5)*S;cw=(w-gap)//2;pad=int(fs*0.45)*S;f=font(fs,500);lh=int(fs*1.32)*S
    hf=font(int(fs*0.78),800);hh=int(fs*1.5)*S
    if draw:
        d.text((x+pad,y+hh*0.7),hdr,font=hf,fill=GR,anchor="ls");d.text((x+cw+gap+pad,y+hh*0.7),hdr2,font=hf,fill=RED,anchor="ls")
    y+=hh
    for a,b in rows:
        la=wrapw(d,a,f,cw-2*pad);lb=wrapw(d,b,f,cw-2*pad);n=max(len(la),len(lb));rh=n*lh+2*pad
        if draw:
            d.rounded_rectangle((x,y,x+cw,y+rh),radius=int(fs*.35)*S,fill=GREYBG)
            d.rounded_rectangle((x+cw+gap,y,x+w,y+rh),radius=int(fs*.35)*S,fill=REDBG)
            for i,l in enumerate(la):d.text((x+pad,y+pad+lh*(i+0.78)),l,font=f,fill=(75,75,75),anchor="ls")
            for i,l in enumerate(lb):d.text((x+cw+gap+pad,y+pad+lh*(i+0.78)),l,font=f,fill=INK,anchor="ls")
        y+=rh+int(fs*0.4)*S
    return y

def render(out,story,build,fs0,fs_min=26):
    Hh=1920 if story else 1080
    img=Image.new("RGB",(W*S,Hh*S),"white")
    d,top,bot=header_footer(img,story)
    L=(88 if story else 52)*S;w=(W-2*(88 if story else 52))*S
    fs=fs0
    while True:
        y=build(d,L,top,w,fs,False,story)
        if y<=bot or fs<=fs_min:break
        fs-=1
    y=build(d,L,top,w,fs,True,story)
    img.resize((W,Hh),Image.LANCZOS).save(out,optimize=True)
    return fs,round((y-top)/S),round((bot-top)/S)

def calcbox(d,x,y,w,label,lines,result,fs,draw,fill,rescol=INK):
    pad=int(fs*0.6)*S;lf=font(int(fs*0.7),800);f=font(fs,400);rf=font(int(fs*1.12),800);lh=int(fs*1.35)*S
    inner=w-2*pad
    ls=[]
    for t in lines:ls+=wrapw(d,t,f,inner)
    rl=wrapw(d,result,rf,inner);rlh=int(fs*1.12*1.3)*S
    h=pad+int(fs*0.7*1.5)*S+len(ls)*lh+int(fs*0.25)*S+len(rl)*rlh+pad
    if draw:
        d.rounded_rectangle((x,y,x+w,y+h),radius=int(fs*.4)*S,fill=fill)
        yy=y+pad;d.text((x+pad,yy+int(fs*0.7*1.1)*S),label,font=lf,fill=GR if fill==GREYBG else RED,anchor="ls");yy+=int(fs*0.7*1.5)*S
        for i,l in enumerate(ls):d.text((x+pad,yy+lh*(i+0.78)),l,font=f,fill=INK,anchor="ls")
        yy+=len(ls)*lh+int(fs*0.25)*S
        for i,l in enumerate(rl):d.text((x+pad,yy+rlh*(i+0.8)),l,font=rf,fill=rescol,anchor="ls")
    return y+h+int(fs*0.5)*S

def table(d,x,y,w,head,rows,total,fs,draw):
    f=font(fs,500);fbold=font(fs,800);hf=font(int(fs*0.72),800);rh=int(fs*1.75)*S
    cw=[0.46,0.18,0.18,0.18];xs=[x];
    for c in cw:xs.append(xs[-1]+int(w*c))
    def cell(i,t,ff,col,yy):
        if i==0:d.text((xs[0]+int(fs*0.2)*S,yy),t,font=ff,fill=col,anchor="lm")
        else:d.text((xs[i+1]-int(fs*0.3)*S,yy),t,font=ff,fill=col,anchor="rm")
    hh=int(fs*1.4)*S
    if draw:
        for i,t in enumerate(head):cell(i,t,hf,GR,y+hh//2)
        d.line((x,y+hh,x+w,y+hh),fill=INK,width=2*S)
    y+=hh
    for r in rows:
        if draw:
            hi=r[0]=="Manager"
            if hi:d.rounded_rectangle((x,y+3*S,x+w,y+rh-3*S),radius=int(fs*.3)*S,fill=REDBG)
            for i,t in enumerate(r):cell(i,t,fbold if i in(0,3) else f,INK,y+rh//2)
            d.line((x,y+rh,x+w,y+rh),fill=LINE,width=S)
        y+=rh
    if draw:
        d.line((x,y,x+w,y),fill=INK,width=2*S)
        for i,t in enumerate(total):cell(i,t,fbold,INK,y+rh//2)
    return y+rh+int(fs*0.4)*S
