# Ported from the box (cards/var.py). Approved quote-card template v1a: make1(text, "L", out) -> 1024px square.
# Env: Q9_FONT_INTER (Inter variable font), Q9_CARD_ASSETS (folder with pallav_photo.jpg and book_cover.jpeg).
import os,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
H=os.environ.get("Q9_CARD_ASSETS",os.path.dirname(os.path.abspath(__file__)))  # needs pallav_photo.jpg + book_cover.jpeg (not in repo)
FONT=os.environ.get("Q9_FONT_INTER","/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf")
S=3;W=1024;RED=(213,78,76);INK=(45,45,44);GR=(113,125,139)
def font(sz,w):
    f=ImageFont.truetype(FONT,sz*S)
    try:f.set_variation_by_axes([min(32,max(14,sz)),w])
    except:pass
    return f
def avatar(d):
    im=Image.open(os.path.join(H,"pallav_photo.jpg")).convert("RGB");w,h=im.size
    cx,cy,r=int(w*.49),int(h*.52),int(w*.47)
    im=im.crop((cx-r,cy-r,cx+r,cy+r)).resize((d,d),Image.LANCZOS)
    m=Image.new("L",(d,d),0);ImageDraw.Draw(m).ellipse((0,0,d-1,d-1),fill=255);return im,m
def badge(d,x,y,s):
    pts=[(x+s/2+s/2*(1 if i%4<2 else .86)*math.cos(2*math.pi*i/48),y+s/2+s/2*(1 if i%4<2 else .86)*math.sin(2*math.pi*i/48)) for i in range(48)]
    d.polygon(pts,fill=(29,155,240));d.line([(x+s*.3,y+s*.52),(x+s*.45,y+s*.66),(x+s*.71,y+s*.36)],fill="white",width=int(s*.11),joint="curve")
def wrap(d,t,f,mw):
    out=[];cur=""
    for wd in t.split():
        x=(cur+" "+wd).strip()
        if d.textlength(x,font=f)<=mw:cur=x
        else:out.append(cur);cur=wd
    return out+[cur]

# 22 Oct 2026 (Pallav): "\n" = new paragraph (blank-line gap); [text] = soft brand-red highlight behind that text
HLC=(247,216,215)
def parse(text):
    import re
    paras=[];hl=False
    for p in re.split(r"\n+",text.replace("\\n","\n").strip()):
        ws=[]
        for tok in p.split():
            o=tok.startswith("[")
            if o:hl=True;tok=tok[1:]
            c=tok.endswith("]")
            if c:tok=tok[:-1]
            if tok:ws.append((tok,hl))
            if c:hl=False
        if ws:paras.append(ws)
    return paras
def rlines(d,text,f,mw):
    sp=d.textlength(" ",font=f);out=[]
    for pi,ws in enumerate(parse(text)):
        cur=[];cw=0
        for w,h in ws:
            ww=d.textlength(w,font=f);need=ww if not cur else cw+sp+ww
            if cur and need>mw:out.append((pi,cur));cur,cw=[(w,h,ww)],ww
            else:cur.append((w,h,ww));cw=need
        out.append((pi,cur))
    return out,sp
def rheight(d,text,f,mw,lh,pg):
    ls,_=rlines(d,text,f,mw);np_=ls[-1][0] if ls else 0
    return len(ls)*lh+np_*pg
def rdraw(d,text,f,mw,L,y,lh,pg,asc,fs):
    ls,sp=rlines(d,text,f,mw);prev=0
    for pi,ws in ls:
        if pi!=prev:y+=pg;prev=pi
        base=y+asc;x=L;runs=[];cur=None
        for w,h,ww in ws:
            if h:
                if cur is None:cur=[x,x+ww]
                else:cur[1]=x+ww
            elif cur is not None:runs.append(cur);cur=None
            x+=ww+sp
        if cur is not None:runs.append(cur)
        for a,b in runs:d.rounded_rectangle((a-8*S,base-fs*0.82,b+8*S,base+fs*0.26),radius=int(fs*0.12),fill=HLC)
        x=L
        for w,h,ww in ws:d.text((x,base),w,font=f,fill=INK,anchor="ls");x+=ww+sp
        y+=lh
    return y
def cover(h):
    cv=Image.open(os.path.join(H,"book_cover.jpeg")).convert("RGB");return cv.resize((int(h*cv.size[0]/cv.size[1]),h),Image.LANCZOS)
def shadow(img,box,blur=14,a=90,off=(8,12)):
    sh=Image.new("L",img.size,0);x0,y0,x1,y1=box
    ImageDraw.Draw(sh).rectangle((x0+off[0]*S,y0+off[1]*S,x1+off[0]*S,y1+off[1]*S),fill=a)
    img.paste((40,40,40),(0,0),sh.filter(ImageFilter.GaussianBlur(blur*S)))
def head(img,d,text,y0,L=52):
    L*=S;AV=132*S
    d.ellipse((L-3*S,y0-3*S,L+AV+3*S,y0+AV+3*S),fill=RED);a,m=avatar(AV);img.paste(a,(L,y0),m)
    fn=font(34,700);tx=L+AV+31*S;nm="Pallav Kulhari"
    d.text((tx,y0+AV*.4),nm,font=fn,fill=INK,anchor="ls");badge(d,tx+d.textlength(nm,font=fn)+10*S,y0+AV*.4-33*S,36*S)
    d.text((tx,y0+AV*.78),"@Quit9to5Book",font=font(33,400),fill=GR,anchor="ls")
    fb=font(42,400);y=y0+AV+50*S
    return rdraw(d,text,fb,(W-104)*S,L,y,60*S,40*S,45*S,42*S)
def htot(d,text):return 132*S+50*S+rheight(d,text,font(42,400),(W-104)*S,60*S,40*S)
def tag(d,x,yb,center=False):
    f1=font(40,800);f2=font(28,500)
    if center:
        d.text((x,yb-44*S),"Quit 9to5",font=f1,fill=INK,anchor="ms");d.text((x,yb),"Coming January 2027",font=f2,fill=RED,anchor="ms")
    else:
        d.line((x,yb-110*S,x+60*S,yb-110*S),fill=RED,width=4*S)
        d.text((x,yb-44*S),"Quit 9to5",font=f1,fill=INK,anchor="ls");d.text((x,yb),"Coming January 2027",font=f2,fill=RED,anchor="ls")
def make(text,v,out):
    img=Image.new("RGB",(W*S,W*S),"white");d=ImageDraw.Draw(img);L=52*S
    t=htot(d,text)
    if v==1: # cover bottom-right, plain
        d.rectangle((0,0,W*S,14*S),fill=RED);head(img,d,text,(W*S-t)//2-70*S)
        cv=cover(230*S);x=W*S-L-cv.size[0];y=W*S-cv.size[1]-46*S
        shadow(img,(x,y,x+cv.size[0],y+cv.size[1]));d=ImageDraw.Draw(img);img.paste(cv,(x,y));d.rectangle((x,y,x+cv.size[0]-1,y+cv.size[1]-1),outline=(225,225,225),width=S)
    if v==2: # tilted cover peeking from bottom-right corner
        d.rectangle((0,0,W*S,14*S),fill=RED);head(img,d,text,(W*S-t)//2-60*S)
        cv=cover(330*S).convert("RGBA");cv=cv.rotate(-12,expand=True,resample=Image.BICUBIC)
        x=W*S-cv.size[0]+40*S;y=W*S-cv.size[1]+110*S
        sh=Image.new("L",img.size,0);sh.paste(cv.split()[3].point(lambda p:90 if p else 0),(x+10*S,y+14*S));img.paste((40,40,40),(0,0),sh.filter(ImageFilter.GaussianBlur(16*S)))
        img.paste(cv,(x,y),cv)
    if v==3: # centered small cover at bottom, thin divider
        d.rectangle((0,0,W*S,14*S),fill=RED);head(img,d,text,(W*S-t)//2-110*S)
        cv=cover(190*S);x=(W*S)//2-cv.size[0]-30*S;y=W*S-cv.size[1]-40*S
        d.line((L,y-36*S,W*S-L,y-36*S),fill=(232,232,232),width=2*S)
        shadow(img,(x,y,x+cv.size[0],y+cv.size[1]),10,70,(5,8));d=ImageDraw.Draw(img);img.paste(cv,(x,y));d.rectangle((x,y,x+cv.size[0]-1,y+cv.size[1]-1),outline=(225,225,225),width=S)
    if v==4: # split: soft grey right panel with big cover, text left
        d.rectangle((0,0,W*S,14*S),fill=RED)
        px=int(W*S*.66);d.rectangle((px,14*S,W*S,W*S),fill=(246,244,243))
        cv=cover(300*S);x=px+(W*S-px-cv.size[0])//2;y=(W*S-cv.size[1])//2
        shadow(img,(x,y,x+cv.size[0],y+cv.size[1]));d=ImageDraw.Draw(img);img.paste(cv,(x,y))
        # narrower text column
        AV=110*S;y0=(W*S)//2-200*S
        d.ellipse((L-3*S,y0-3*S,L+AV+3*S,y0+AV+3*S),fill=RED);a,m=avatar(AV);img.paste(a,(L,y0),m)
        tx=L+AV+24*S;fn=font(30,700);d.text((tx,y0+AV*.42),"Pallav Kulhari",font=fn,fill=INK,anchor="ls");badge(d,tx+d.textlength("Pallav Kulhari",font=fn)+8*S,y0+AV*.42-29*S,32*S)
        d.text((tx,y0+AV*.8),"@Quit9to5Book",font=font(28,400),fill=GR,anchor="ls")
        fb=font(38,400);yy=y0+AV+44*S
        for ln in wrap(d,text,fb,px-2*L):d.text((L,yy+40*S),ln,font=fb,fill=INK,anchor="ls");yy+=55*S
    if v==5: # red bottom corner wedge + cover, top bar
        d.rectangle((0,0,W*S,14*S),fill=RED);head(img,d,text,(W*S-t)//2-70*S)
        d.polygon([(W*S,W*S-380*S),(W*S,W*S),(W*S-520*S,W*S)],fill=(250,232,231))
        cv=cover(230*S);x=W*S-L-cv.size[0];y=W*S-cv.size[1]-46*S
        shadow(img,(x,y,x+cv.size[0],y+cv.size[1]));d=ImageDraw.Draw(img);img.paste(cv,(x,y))
    d=ImageDraw.Draw(img)
    if v==3:
        f1=font(40,800);f2=font(28,500);tx=W*S//2+10*S;yb=W*S-40*S-95*S+60*S
        d.text((tx,yb-44*S),'Quit 9to5',font=f1,fill=INK,anchor='ls');d.text((tx,yb),'Coming January 2027',font=f2,fill=RED,anchor='ls')
    if v==3:
        f1=font(40,800);f2=font(28,500);tx=W*S//2+10*S;yb=W*S-120*S
        d.text((tx,yb-44*S),'Quit 9to5',font=f1,fill=INK,anchor='ls');d.text((tx,yb),'Coming January 2027',font=f2,fill=RED,anchor='ls')
    if v in (1,2,5): tag(d,L,W*S-60*S)
    if v==4: tag(d,int(W*S*.66)+(W*S-int(W*S*.66))//2,W*S-80*S,True)
    img.resize((W,W),Image.LANCZOS).save(out,optimize=True)
T="Nobody quits a job. They quit the version of themselves the job was slowly turning them into."
if __name__=="__main__":
    for v in range(1,6):make(T,v,f"var{v}.png")

def make1(text,mode,out):
    img=Image.new("RGB",(W*S,W*S),"white");d=ImageDraw.Draw(img);L=52*S
    cv=cover(200*S);cw,ch=cv.size;y=W*S-ch-50*S
    t=htot(d,text);y0=max(40*S,min((W*S-t)//2-70*S,y-60*S-t))   # keep >=60px above the cover
    d.rectangle((0,0,W*S,14*S),fill=RED);head(img,d,text,y0)
    f1=font(40,800);f2=font(28,500)
    if mode=="L": x=L; tx=x+cw+34*S; anc="ls"
    else: x=W*S-L-cw; tx=x-34*S; anc="rs"
    shadow(img,(x,y,x+cw,y+ch));d=ImageDraw.Draw(img);img.paste(cv,(x,y));d.rectangle((x,y,x+cw-1,y+ch-1),outline=(225,225,225),width=S)
    mid=y+ch//2
    lx=tx if anc=="ls" else tx-60*S
    # 19 Oct 2026 rule (Pallav): no bold "Quit 9to5" beside the cover; red rule + date, centred on the cover
    f2=font(32,600)
    d.line((lx,mid-24*S,lx+60*S,mid-24*S),fill=RED,width=4*S)
    d.text((tx,mid+26*S),"Coming January 2027",font=f2,fill=RED,anchor=anc)
    img.resize((W,W),Image.LANCZOS).save(out,optimize=True)
if __name__=="__main__":
    make1(T,"L","v1a.png");make1(T,"R","v1b.png")
